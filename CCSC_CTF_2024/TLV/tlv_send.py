import socket, struct, sys

HOST = sys.argv[1] if len(sys.argv)>1 else "127.0.0.1"
PORT = int(sys.argv[2]) if len(sys.argv)>2 else 8080

def mk_tlv(t, val: bytes):
    return struct.pack("!B H", t, len(val)) + val

def main():
    s = socket.create_connection((HOST, PORT), timeout=5)
    payload = mk_tlv(1, b"hello")
    print("Send:", payload)
    s.sendall(payload)
    try:
        r = s.recv(4096)
        print("Recv:", r)
    except Exception as e:
        print("Recv error:", e)
    finally:
        s.close()

if __name__ == "__main__":
    main()
