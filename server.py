"""
UDP Echo Server with random packet dropping.
Name: Bishika Pokharel
EUID: bp0797
"""

import argparse
import random
import socket

DROP_PROBABILITY = 0.33
BUFFER_SIZE = 4096


def run_server(port):
    print(f"[server] Bishika Pokharel | EUID: bp0797")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))

    print("[server] : ready to accept data...")

    try:
        while True:
            data, sender_addr = sock.recvfrom(BUFFER_SIZE)
            message = data.decode(errors="replace")

            if random.random() < DROP_PROBABILITY:
                print("[server] : packet dropped")
                continue

            print(f"[client] : {message}")

            if message.strip() == "PING":
                reply = b"PONG"
            else:
                reply = data

            sock.sendto(reply, sender_addr)
    except KeyboardInterrupt:
        print("\n[server] shutting down")
    finally:
        sock.close()


def main():
    parser = argparse.ArgumentParser(description="UDP echo server with random packet drops")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    run_server(args.port)


if __name__ == "__main__":
    main()
