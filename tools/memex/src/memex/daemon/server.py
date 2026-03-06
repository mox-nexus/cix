"""memexd server — Unix socket listener for concurrent agent access.

Single owner of DuckDB + ONNX. Clients connect via Unix socket,
send JSON-RPC requests, receive JSON-RPC responses.

Wire format: length-prefixed JSON (4-byte big-endian length + UTF-8 payload).
"""

import fcntl
import logging
import os
import signal
import socket
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from memex.config.settings import get_active_memex_dir
from memex.daemon.protocol import Dispatcher
from memex.daemon.wire import recv_message, send_message

MAX_CLIENTS = 16

logger = logging.getLogger("memexd")


def default_socket_path() -> Path:
    """Default Unix socket path: <active_memex_dir>/memexd.sock"""
    return get_active_memex_dir() / "memexd.sock"


def default_pid_path() -> Path:
    """Default PID file path: <active_memex_dir>/memexd.pid"""
    return get_active_memex_dir() / "memexd.pid"


def _check_stale_pid(pid_path: Path) -> bool:
    """Check if PID file points to a running process. Remove if stale."""
    if not pid_path.exists():
        return False
    try:
        pid = int(pid_path.read_text().strip())
        os.kill(pid, 0)  # Signal 0 = check if alive
        return True  # Process is running
    except (ValueError, ProcessLookupError, PermissionError):
        # Stale PID file — clean up
        pid_path.unlink(missing_ok=True)
        return False
    except OSError:
        pid_path.unlink(missing_ok=True)
        return False


def _write_pid(pid_path: Path) -> None:
    fd = os.open(str(pid_path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        os.close(fd)
        raise RuntimeError("Another memexd is starting (PID file locked)")
    os.write(fd, str(os.getpid()).encode())
    # Keep fd open to hold the lock for the daemon's lifetime
    return fd


def _cleanup(
    sock_path: Path,
    pid_path: Path,
    sock: socket.socket | None,
    pid_fd: int | None = None,
) -> None:
    if sock:
        try:
            sock.close()
        except OSError:
            pass
    sock_path.unlink(missing_ok=True)
    pid_path.unlink(missing_ok=True)
    if pid_fd is not None:
        try:
            os.close(pid_fd)
        except OSError:
            pass


class Server:
    """memexd Unix socket server.

    Accepts connections, dispatches JSON-RPC to ports, returns responses.
    One thread per client (DuckDB handles its own locking internally).
    """

    def __init__(
        self,
        dispatcher: Dispatcher,
        sock_path: Path | None = None,
        pid_path: Path | None = None,
    ):
        self._dispatcher = dispatcher
        self._sock_path = sock_path or default_socket_path()
        self._pid_path = pid_path or default_pid_path()
        self._server_sock: socket.socket | None = None
        self._shutdown = threading.Event()

    @property
    def socket_path(self) -> Path:
        return self._sock_path

    def start(self, register_signals: bool = True) -> None:
        """Start the server. Blocks until shutdown.

        Args:
            register_signals: Register SIGTERM/SIGINT handlers. Set False
                            when running in a thread (signals only work
                            on the main thread).
        """
        if _check_stale_pid(self._pid_path):
            pid = int(self._pid_path.read_text().strip())
            logger.error("memexd already running (PID %d)", pid)
            sys.exit(1)

        # Clean up stale socket
        self._sock_path.unlink(missing_ok=True)

        self._server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        old_umask = os.umask(0o077)
        try:
            self._server_sock.bind(str(self._sock_path))
        finally:
            os.umask(old_umask)
        self._server_sock.listen(16)
        self._server_sock.settimeout(1.0)  # Allow periodic shutdown check

        pid_fd = _write_pid(self._pid_path)

        if register_signals:
            signal.signal(signal.SIGTERM, lambda *_: self.stop())
            signal.signal(signal.SIGINT, lambda *_: self.stop())

        logger.info(
            "memexd listening on %s (PID %d)",
            self._sock_path,
            os.getpid(),
        )

        pool = ThreadPoolExecutor(max_workers=MAX_CLIENTS)
        try:
            while not self._shutdown.is_set():
                try:
                    conn, _ = self._server_sock.accept()
                    pool.submit(self._handle_client, conn)
                except TimeoutError:
                    continue
        finally:
            pool.shutdown(wait=False)
            _cleanup(self._sock_path, self._pid_path, self._server_sock, pid_fd)
            logger.info("memexd stopped")

    def stop(self) -> None:
        """Signal the server to shut down."""
        self._shutdown.set()

    def _handle_client(self, conn: socket.socket) -> None:
        """Handle a single client connection (runs in thread pool)."""
        conn.settimeout(30.0)
        try:
            while not self._shutdown.is_set():
                try:
                    request = recv_message(conn)
                except (TimeoutError, ConnectionError):
                    break
                response = self._dispatcher.dispatch(request)
                send_message(conn, response)
        except Exception:
            logger.exception("Client handler error")
        finally:
            conn.close()
