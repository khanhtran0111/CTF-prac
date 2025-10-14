import socket
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
TIMEOUT = 5

def probe_tcp(host, port):
    s = socket.socket()
    s.settimeout(TIMEOUT)
    try:
        s.connect((host, port))
        req = b"GET / HTTP/1.1\r\nHost: %b\r\nConnection: close\r\n\r\n" % host.encode()
        s.sendall(req)
        data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
        print("RESPONSE ({} bytes):\n".format(len(data)))
        print(data.decode(errors="replace")[:2000])
    except Exception as e:
        print("ERROR:", e)
    finally:
        s.close()

if __name__ == "__main__":
    print(f"Probing {HOST}:{PORT} ...")
    probe_tcp(HOST, PORT)