import socket
import struct

def send_packet(sock, pkt_type, data):
    header = struct.pack('<2i', pkt_type, len(data))
    sock.sendall(header + data)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('112.137.129.129', 27001))

    # Send PKT_HELLO
    student_code = b'23021639'  # Replace with your code
    send_packet(sock, 0, student_code)

    while True:
        # Read header
        header = sock.recv(8)
        pkt_type, pkt_len = struct.unpack('<2i', header)
        
        # Read data
        data = b''
        while len(data) < pkt_len:
            data += sock.recv(pkt_len - len(data))

        if pkt_type == 1:
            

if __name__ == '__main__':
    main()
