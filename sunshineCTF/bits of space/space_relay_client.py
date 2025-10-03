import socket
import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

# Target device ID that contains the flag
TARGET_DEVICE_ID = 0xdeadbabe  # sun{REDACTED}

# Other valid device IDs for reference
VALID_DEVICES = {
    0x13371337: b"Status Relay",
    0x1337babe: b"Ground Station Alpha", 
    0xdeadbeef: b"Lunar Relay",
    0xdeadbabe: b"sun{REDACTED}"
}

def create_subscription_packet(device_id, start, end, channel, key):
    """Create encrypted subscription packet"""
    
    # Pack the data according to struct format "<IQQI"
    # < = little endian
    # I = unsigned int (4 bytes) - device_id
    # Q = unsigned long long (8 bytes) - start
    # Q = unsigned long long (8 bytes) - end  
    # I = unsigned int (4 bytes) - channel
    
    plaintext = struct.pack("<IQQI", device_id, start, end, channel)
    print(f"Plaintext data: device_id=0x{device_id:08x}, start={start}, end={end}, channel={channel}")
    print(f"Packed plaintext: {plaintext.hex()}")
    
    # Pad the plaintext to AES block size
    padded_plaintext = pad(plaintext, AES.block_size)
    
    # Generate random IV
    iv = os.urandom(AES.block_size)
    
    # Encrypt using AES CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded_plaintext)
    
    # Combine IV + ciphertext
    packet = iv + ciphertext
    
    print(f"IV: {iv.hex()}")
    print(f"Ciphertext: {ciphertext.hex()}")
    print(f"Full packet: {packet.hex()}")
    
    return packet

def connect_to_relay(host="localhost", port=9000):
    """Connect to the space relay server"""
    
    try:
        # Create socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        # Receive welcome message
        response = sock.recv(1024)
        print("Server response:")
        print(response.decode())
        
        return sock
        
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

def attempt_connection_without_key():
    """Try to connect without knowing the key - this will fail but shows the process"""
    
    print("=== Attempting connection without key (will fail) ===")
    
    # We don't have the actual key, so let's try with a dummy key
    dummy_key = b"0" * 32  # 32 bytes for AES-256
    
    # Try to create a packet for the target device
    packet = create_subscription_packet(
        device_id=TARGET_DEVICE_ID,
        start=0,
        end=1000,
        channel=1,
        key=dummy_key
    )
    
    # Connect to server (if running locally)
    sock = connect_to_relay()
    if sock:
        try:
            sock.send(packet)
            response = sock.recv(1024)
            print("Server response:")
            print(response.decode())
        except Exception as e:
            print(f"Error sending packet: {e}")
        finally:
            sock.close()

def analyze_protocol():
    """Analyze the protocol structure"""
    
    print("=== Protocol Analysis ===")
    print("1. Server expects encrypted subscription packet")
    print("2. Packet structure after decryption:")
    print("   - device_id (4 bytes, unsigned int)")
    print("   - start (8 bytes, unsigned long long)")  
    print("   - end (8 bytes, unsigned long long)")
    print("   - channel (4 bytes, unsigned int)")
    print("3. Total plaintext size: 24 bytes")
    print("4. Encryption: AES CBC mode with unknown key")
    print("5. Packet format: [IV (16 bytes)] + [Ciphertext]")
    print()
    
    print("Valid Device IDs:")
    for device_id, name in VALID_DEVICES.items():
        print(f"  0x{device_id:08x}: {name}")
    print()
    
    print("Target: 0xdeadbabe contains the flag")
    print()
    
    print("Challenge: We need the encryption key to create valid packets")

def look_for_key_hints():
    """Look for hints about the encryption key"""
    
    print("=== Looking for key hints ===")
    print("1. Key is imported from 'secrets' module")
    print("2. This suggests the key might be:")
    print("   - In a separate file called secrets.py")
    print("   - Hardcoded somewhere else")
    print("   - Derivable from some pattern")
    print()
    
    print("Possible approaches:")
    print("1. Check if there's a secrets.py file")
    print("2. Look for key in environment variables")
    print("3. Try common/weak keys")
    print("4. Check if the server is actually running somewhere to connect to")
    print("5. Look for other files that might contain the key")

def check_for_remote_server():
    """Check if the server is running on a remote host"""
    
    print("=== Checking for remote server ===")
    
    # Common CTF server hosts to try
    hosts_to_try = [
        "localhost",
        "127.0.0.1", 
        "2025.sunshinectf.games",  # Common CTF domain pattern
        "challs.sunshinectf.games",
        "relay.sunshinectf.games"
    ]
    
    port = 9000
    
    for host in hosts_to_try:
        print(f"Trying {host}:{port}...")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # 5 second timeout
            result = sock.connect_ex((host, port))
            
            if result == 0:
                print(f"🎯 Found server at {host}:{port}!")
                
                # Try to get the welcome message
                sock.settimeout(10)
                response = sock.recv(1024)
                print("Server says:")
                print(response.decode())
                sock.close()
                return host
            else:
                print(f"  No server at {host}:{port}")
                
        except Exception as e:
            print(f"  Error connecting to {host}: {e}")
        finally:
            try:
                sock.close()
            except:
                pass
    
    return None

def main():
    print("Space Relay Challenge Analysis")
    print("=" * 40)
    
    analyze_protocol()
    look_for_key_hints()
    
    # Try to find the server
    server_host = check_for_remote_server()
    
    if server_host:
        print(f"\n🎯 Found server at {server_host}!")
        print("Next step: Need to find the encryption key to create valid packets")
    else:
        print("\nNo server found. The server might be:")
        print("1. Not currently running")
        print("2. On a different host/port")
        print("3. Part of a local setup we need to run")

if __name__ == "__main__":
    main()