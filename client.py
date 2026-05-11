"""
UDP Client - sends PING messages.
Name: Bishika Pokharel
EUID: bp0797
"""

import argparse
import socket

CLIENT_TIMEOUT_SEC = 2.0
NUM_PINGS = 10
BUFFER_SIZE = 4096


def run_client(port):
    print(f"[client] Bishika Pokharel | EUID: bp0797")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(CLIENT_TIMEOUT_SEC)
    target = ("127.0.0.1", port)

    try:
        for i in range(1, NUM_PINGS + 1):
            sock.sendto(b"PING", target)
            try:
                data, _ = sock.recvfrom(BUFFER_SIZE)
                print(f"{i:<3}: sent PING... received  {data!r}")
            except socket.timeout:
                print(f"{i:<3}: sent PING... Timed Out")
    finally:
        sock.close()


def main():
    parser = argparse.ArgumentParser(description="UDP PING client")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    run_client(args.port)


if __name__ == "__main__":
    main()
