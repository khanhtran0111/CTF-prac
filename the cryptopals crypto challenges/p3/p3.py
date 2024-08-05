import binascii
from itertools import cycle

def xor_decrypt(ciphertext, key):
    """Decrypts ciphertext by XORing with the given key."""
    return bytes([b ^ key for b in ciphertext])

def is_english(text):
    """Check if the text is readable English based on simple heuristics."""
    return all(32 <= b < 127 or b in [10, 13] for b in text)

def main():
    hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    ciphertext = binascii.unhexlify(hex_string)
    
    # Try every possible single-byte key
    for key in range(256):
        plaintext = xor_decrypt(ciphertext, key)
        if is_english(plaintext):
            print(f"Key: {key:02x} -> {plaintext.decode('ascii', errors='ignore')}")

if __name__ == "__main__":
    main()
