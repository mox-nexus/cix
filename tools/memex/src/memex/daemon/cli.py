"""memexd CLI — start, stop, status for the memex daemon."""

import logging
import os
import signal
import sys
from pathlib import Path

import click
from rich.console import Console

from memex.daemon.server import Server, default_pid_path, default_socket_path

console = Console()


def _read_pid(pid_path: Path) -> int | None:
    """Read PID from file, return None if missing or invalid."""
    if not pid_path.exists():
        return None
    try:
        pid = int(pid_path.read_text().strip())
        os.kill(pid, 0)  # Check if alive
        return pid
    except (ValueError, ProcessLookupError, PermissionError, OSError):
        pid_path.unlink(missing_ok=True)
        return None


@click.group()
def main():
    """memexd — memex daemon for concurrent access."""
    pass


@main.command()
@click.option("--foreground", "-f", is_flag=True, help="Run in foreground (don't daemonize)")
def start(foreground: bool):
    """Start the memex daemon."""
    pid_path = default_pid_path()
    existing = _read_pid(pid_path)
    if existing:
        console.print(f"[yellow]memexd already running (PID {existing})[/yellow]")
        sys.exit(1)

    if not foreground:
        _daemonize()

    # Set up logging
    level = logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )
    logger = logging.getLogger("memexd")

    # Wire up the service
    from memex.composition import create_service

    service = create_service(with_embedder=True, with_reranker=True)
    logger.info("Corpus: %s", service.corpus)
    logger.info("Embedder: %s", "enabled" if service.embedder else "disabled")
    logger.info("Reranker: %s", "enabled" if service.reranker else "disabled")

    from memex.daemon.protocol import Dispatcher

    dispatcher = Dispatcher(
        corpus=service.corpus,
        graph=service.graph,
        trails=service.trails,
    )

    server = Server(dispatcher)
    try:
        server.start()
    finally:
        service.close()


@main.command()
def stop():
    """Stop the memex daemon."""
    pid_path = default_pid_path()
    pid = _read_pid(pid_path)
    if not pid:
        console.print("[yellow]memexd is not running[/yellow]")
        return

    try:
        os.kill(pid, signal.SIGTERM)
        console.print(f"[green]Stopped memexd (PID {pid})[/green]")
    except ProcessLookupError:
        pid_path.unlink(missing_ok=True)
        console.print("[yellow]memexd was not running (cleaned up stale PID)[/yellow]")


@main.command()
def status():
    """Show daemon status."""
    pid_path = default_pid_path()
    sock_path = default_socket_path()
    pid = _read_pid(pid_path)

    if pid:
        console.print(f"[green]memexd running[/green] (PID {pid})")
        console.print(f"  Socket: {sock_path}")
    else:
        console.print("[dim]memexd not running[/dim]")
        if sock_path.exists():
            console.print(f"  [yellow]Stale socket at {sock_path}[/yellow]")


def _daemonize():
    """Double-fork to detach from terminal.

    The parent process writes the grandchild PID to a temp file so it can
    print the correct PID before exiting. The grandchild also prints on
    start, but only in foreground mode (handled by caller).
    """
    # Use a pipe so grandchild can send its PID to the original parent
    read_fd, write_fd = os.pipe()

    # First fork
    pid = os.fork()
    if pid > 0:
        # Parent: wait for grandchild PID via pipe
        os.close(write_fd)
        data = os.read(read_fd, 32)
        os.close(read_fd)
        grandchild_pid = int(data.decode().strip()) if data else pid
        console.print(f"[green]memexd started (PID {grandchild_pid})[/green]")
        sys.exit(0)

    os.close(read_fd)

    # Child becomes session leader
    os.setsid()

    # Second fork — prevent reacquiring terminal
    pid = os.fork()
    if pid > 0:
        # First child: send grandchild PID to parent, then exit
        os.write(write_fd, str(pid).encode())
        os.close(write_fd)
        sys.exit(0)

    os.close(write_fd)

    # Redirect stdio
    devnull = os.open(os.devnull, os.O_RDWR)
    os.dup2(devnull, 0)
    os.dup2(devnull, 1)
    # Keep stderr for logging
    os.close(devnull)
