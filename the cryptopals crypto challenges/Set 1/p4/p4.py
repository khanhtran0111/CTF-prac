import binascii

def xor_single_byte(data, key):
    """XORs each byte of the data with the single byte key."""
    return bytes([b ^ key for b in data])

def score_text(text):
    """Scores text based on the frequency of English letters and common characters."""
    # English letter frequency (approximate) and common characters
    frequency = {
        'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3, 'e': 12.7, 'f': 2.2, 'g': 2.0,
        'h': 6.1, 'i': 7.0, 'j': 0.15, 'k': 0.77, 'l': 4.0, 'm': 2.4, 'n': 6.7,
        'o': 7.5, 'p': 1.9, 'q': 0.095, 'r': 6.0, 's': 6.3, 't': 9.1, 'u': 2.8,
        'v': 0.98, 'w': 2.4, 'x': 0.15, 'y': 2.0, 'z': 0.074, ' ': 13.0
    }
    
    # Score based on frequency of common English characters
    score = 0
    for byte in text:
        char = chr(byte)
        score += frequency.get(char.lower(), 0)
    
    return score

def decrypt_xor_cipher(hex_string):
    """Decrypts the XOR ciphered hex string by trying all possible single byte keys."""
    data = bytes.fromhex(hex_string)
    best_score = 0
    best_result = ""
    best_key = None
    
    for key in range(256):
        decrypted = xor_single_byte(data, key)
        try:
            decrypted_text = decrypted.decode('ascii')
            text_score = score_text(decrypted)
            if text_score > best_score:
                best_score = text_score
                best_result = decrypted_text
                best_key = key
        except UnicodeDecodeError:
            # Ignore non-ASCII results
            continue
    
    return best_key, best_result

# Hex-encoded string to decrypt
with open('D:/Coding/Practice CTF/CTF-prac/the cryptopals crypto challenges/p4/p4.txt', 'r') as file:
    hex_string = file.read()

# Decrypt the message
key, message = decrypt_xor_cipher(hex_string)

print(f"Key: {key}")
print(f"Decrypted Message: {message}")
