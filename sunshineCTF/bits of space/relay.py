import socket
import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from secrets import key

HOST = "0.0.0.0"
PORT = 9000

VALID_DEVICES = {
    0x13371337: b"Status Relay",
    0x1337babe: b"Ground Station Alpha",
    0xdeadbeef: b"Lunar Relay",
    0xdeadbabe: b"sun{REDACTED}"
}

CHANNEL_MESSAGES = {
    1: b"Channel 1: Deep Space Telemetry Stream.\n",
    2: b"Channel 2: Asteroid Mining Operations Log.\n",
    3: b"Channel 3: Secret Alien Communication Feed!\n",
}

def decrypt_subscription(data: bytes, key: bytes):
    iv = data[:AES.block_size]
    body = data[AES.block_size:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(body), AES.block_size)

    device_id, start, end, channel = struct.unpack("<IQQI", plaintext)
    return device_id, start, end, channel

def handle_client(conn):
    try:
        conn.sendall(b"== Space Relay ==\n")
        conn.sendall(b"Send your subscription packet:\n")

        data = conn.recv(1024).strip()
        if not data:
            conn.sendall(b"No data received.\n")
            return

        try:
            device_id, start, end, channel = decrypt_subscription(data, key)
        except Exception as e:
            conn.sendall(b"Invalid subscription. Access denied.\n")
            return

        if device_id not in VALID_DEVICES:
            conn.sendall(b"Unknown device ID. Authentication failed.\n")
            return

        # Secret Device
        if device_id == 0xdeadbabe:
            conn.sendall(b"You have reached the secret relay... here you go.\n")
            conn.sendall(VALID_DEVICES[device_id])
            return

        if channel not in CHANNEL_MESSAGES:
            conn.sendall(b"Unknown channel. No signal.\n")
            return

        device_name = VALID_DEVICES[device_id]
        conn.sendall(f"Authenticated device: {device_name}\n".encode())
        conn.sendall(CHANNEL_MESSAGES[channel])

    finally:
        conn.sendall(b"See you next time space cowboy.\n")
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Satellite relay listening on {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept()
            handle_client(conn)

if __name__ == "__main__":
    main()
