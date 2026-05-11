"""
Reverse Proxy (UDP) - Round-Robin Load Balancer
Name: Bishika Pokharel
EUID: bp0797

Usage:
    python proxy.py --port 8000 --upstream 8001 8002
"""

import argparse
import socket
import sys

UPSTREAM_TIMEOUT_SEC = 1.0
BUFFER_SIZE = 4096


def run_proxy(listen_port, upstream_ports):
    print(f"[proxy] Bishika Pokharel | EUID: bp0797")

    downstream_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    downstream_sock.bind(("0.0.0.0", listen_port))

    upstream_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    upstream_sock.settimeout(UPSTREAM_TIMEOUT_SEC)

    print("[proxy] : ready to proxy data...")

    rr_index = 0

    try:
        while True:
            data, client_addr = downstream_sock.recvfrom(BUFFER_SIZE)

            server_idx = rr_index % len(upstream_ports)
            server_port = upstream_ports[server_idx]
            rr_index += 1

            try:
                upstream_sock.sendto(data, ("127.0.0.1", server_port))
            except OSError as exc:
                print(f"[proxy] send to upstream failed: {exc}")
                continue

            try:
                reply, _ = upstream_sock.recvfrom(BUFFER_SIZE)
            except socket.timeout:
                continue

            tagged = reply + f" via {server_port} [{server_idx}]".encode()
            downstream_sock.sendto(tagged, client_addr)
    except KeyboardInterrupt:
        print("\n[proxy] shutting down")
    finally:
        downstream_sock.close()
        upstream_sock.close()


def main():
    parser = argparse.ArgumentParser(description="UDP reverse proxy with round-robin load balancing")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--upstream", type=int, nargs="+", default=[8001, 8002])
    args = parser.parse_args()

    if not args.upstream:
        print("error: at least one upstream port must be provided", file=sys.stderr)
        sys.exit(1)

    run_proxy(args.port, args.upstream)


if __name__ == "__main__":
    main()
