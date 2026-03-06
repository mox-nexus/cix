"""Wire format for memexd — length-prefixed messages over Unix socket.

Shared between server and client. Neither imports the other.
"""

import socket
import struct

# Length prefix: 4-byte big-endian unsigned int
HEADER_FMT = "!I"
HEADER_SIZE = struct.calcsize(HEADER_FMT)
MAX_MESSAGE_SIZE = 16 * 1024 * 1024  # 16MB cap


def _recv_exact(conn: socket.socket, n: int) -> bytes:
    """Read exactly n bytes from socket."""
    buf = bytearray()
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Client disconnected")
        buf.extend(chunk)
    return bytes(buf)


def recv_message(conn: socket.socket) -> str:
    """Read a length-prefixed message."""
    header = _recv_exact(conn, HEADER_SIZE)
    (length,) = struct.unpack(HEADER_FMT, header)
    if length > MAX_MESSAGE_SIZE:
        raise ValueError(f"Message too large: {length} bytes")
    payload = _recv_exact(conn, length)
    return payload.decode("utf-8")


def send_message(conn: socket.socket, data: str) -> None:
    """Write a length-prefixed message."""
    payload = data.encode("utf-8")
    header = struct.pack(HEADER_FMT, len(payload))
    conn.sendall(header + payload)
