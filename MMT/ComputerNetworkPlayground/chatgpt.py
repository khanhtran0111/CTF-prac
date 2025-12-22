import socket
import struct

def main():
    server_ip = "112.137.129.129"
    port = 27001

    # Establish a TCP connection.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, port))

    # --- Send PKT_HELLO ---
    student_code = "123456"  # Replace with your actual student code.
    pkt_type = 0  # PKT_HELLO
    pkt_len = len(student_code)
    # Pack the header in little-endian order: two 4-byte integers.
    header = struct.pack('<II', pkt_type, pkt_len)
    s.sendall(header)
    s.sendall(student_code.encode('ascii'))

    # --- Receive PKT_CALC ---
    response_header = s.recv(8)
    if len(response_header) < 8:
        print("Incomplete header")
        s.close()
        return

    resp_type, resp_len = struct.unpack('<II', response_header)
    if resp_type == 1 and resp_len == 8:
        data = s.recv(8)
        if len(data) < 8:
            print("Incomplete data for PKT_CALC")
            s.close()
            return
        a, b = struct.unpack('<II', data)
        result = (a + b) & 0xFFFFFFFF  # Ensure result fits in 32 bits.

        # --- Send PKT_RESULT ---
        pkt_type = 2  # PKT_RESULT
        pkt_len = 4
        header = struct.pack('<II', pkt_type, pkt_len)
        result_data = struct.pack('<I', result)
        s.sendall(header + result_data)

    # --- Receive Final Packet (PKT_FLAG or PKT_BYE) ---
    response_header = s.recv(8)
    if len(response_header) < 8:
        print("Incomplete header for final packet")
        s.close()
        return

    resp_type, resp_len = struct.unpack('<II', response_header)
    if resp_type == 4:  # PKT_FLAG
        flag = s.recv(resp_len)
        print("Received flag:", flag.decode('ascii'))
    elif resp_type == 3:
        print("Server sent PKT_BYE. Connection closed.")

    s.close()

if __name__ == "__main__":
    main()
#failed