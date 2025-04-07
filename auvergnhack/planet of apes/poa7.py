def decrypt_char(ch):
    if ch == '`':
        return 'c'
    elif ch == '^':
        return 'a'
    elif ch == '_':
        return 'b'
    elif ch.isalpha():
        if ch.islower():
            return chr((ord(ch) - ord('a') + 3) % 26 + ord('a'))
        else:
            return chr((ord(ch) - ord('A') + 3) % 26 + ord('A'))
    else:
        return ch

def decrypt_text(ciphertext):
    return ''.join(decrypt_char(ch) for ch in ciphertext)

if __name__ == '__main__':
    import os
    file_path = os.path.join(os.path.dirname(__file__), 'poa7.txt')
    try:
        with open(file_path, 'r') as f:
            cipher_text = f.read()
        plain_text = decrypt_text(cipher_text)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        import sys
        sys.exit(1)
    print("Decrypted message:\n")
    print(plain_text)
