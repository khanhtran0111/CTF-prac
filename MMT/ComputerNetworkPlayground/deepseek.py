import socket
import struct

def recv_all(sock, length):
    data = b''
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data += packet
    return data

HOST = '112.137.129.129'
PORT = 27001
student_id = b'23021639'  # Replace with your ID

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    # Send PKT_HELLO
    header = struct.pack('<II', 0, len(student_id))
    s.sendall(header + student_id)
    
    while True:
        header = recv_all(s, 8)
        if not header or len(header) != 8:
            break
        
        type_, len_ = struct.unpack('<II', header)
        
        if type_ == 1:  # PKT_CALC
            data = recv_all(s, 8)
            a, b = struct.unpack('<II', data)
            sum_ = a + b
            
            # Send PKT_RESULT
            response_header = struct.pack('<II', 2, 4)
            response_data = struct.pack('<I', sum_)
            s.sendall(response_header + response_data)
        elif type_ == 4:  # PKT_FLAG
            data = recv_all(s, len_)
            print(f"Flag: {data.decode()}")
            break
        elif type_ == 3:  # PKT_BYE
            print("Connection closed by server.")
            break
        else:
            print(f"Unknown packet type: {type_}")
            break