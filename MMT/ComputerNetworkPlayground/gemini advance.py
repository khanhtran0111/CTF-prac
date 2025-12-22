import socket
import struct

def int_to_little_endian(value: int) -> bytes:
    """Converts an integer to a 4-byte little-endian bytestring."""
    return struct.pack("<I", value)

def little_endian_to_int(data: bytes) -> int:
    """Converts a 4-byte little-endian bytestring to an integer."""
    return struct.unpack("<I", data)[0]

def main():
    server_address = ('112.137.129.129', 27001)
    student_id = "23021639"  # Replace with your actual ID

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(server_address)

            # --- Send PKT_HELLO ---
            packet_type = 0
            packet_len = len(student_id)
            packet_data = student_id.encode('ascii')
            packet = int_to_little_endian(packet_type) + int_to_little_endian(packet_len) + packet_data
            sock.sendall(packet)

            # --- Main Loop ---
            while True:
                # --- Read Packet Header ---
                header = sock.recv(8)
                if len(header) < 8:
                    print("Connection closed unexpectedly.")
                    break
                packet_type = little_endian_to_int(header[:4])
                data_length = little_endian_to_int(header[4:])

                # --- Read Packet Data ---
                data = sock.recv(data_length)
                if len(data) < data_length:
                    print("Connection closed unexpectedly.")
                    break

                # --- Handle Packet ---
                if packet_type == 1:  # PKT_CALC
                    a = little_endian_to_int(data[:4])
                    b = little_endian_to_int(data[4:])
                    result = a + b
                    print(f"Cal: {a} + {b} = {result}")
                    # --- Send PKT_RESULT ---
                    result_packet = int_to_little_endian(2) + int_to_little_endian(4) + int_to_little_endian(result)
                    sock.sendall(result_packet)

                elif packet_type == 4:  # PKT_FLAG
                    print(f"{data.decode('ascii')}")
                    break
                elif packet_type == 3: # PKT_BYE
                    print("Result denied")
                    break;
                else:
                    print(f"Unknown packet type: {packet_type}")
                    break

    except ConnectionRefusedError:
        print("Connection refused.  Make sure the server is running.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()