def generator(g, x, p):
    return pow(g, x) % p

# def dynamic_xor_decrypt(cipher_text, text_key):
#     key_length = len(text_key)
#     plaintext = ""
#     for i, char in enumerate(cipher_text):
#         key_char = text_key[i % key_length]
#         decrypted_char = chr(ord(char) ^ ord(key_char))
#         plaintext += decrypted_char
#     return plaintext[::-1]

def dynamic_xor_decrypt(plaintext, text_key):
    cipher_text = ""
    key_length = len(text_key)

    for i, char in enumerate(plaintext[::-1]):
        key_char = text_key[i % key_length]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        cipher_text += encrypted_char

    plaintext = cipher_text
    cipher_text = ""

    for i, char in enumerate(plaintext[::-1]):
        key_char = text_key[i % key_length]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        cipher_text += encrypted_char

    plaintext = cipher_text
    cipher_text = ""

    for i, char in enumerate(plaintext[::-1]):
        key_char = text_key[i % key_length]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        cipher_text += encrypted_char
    
    return cipher_text

# def dec(cipher, a, b, g, p, text_key):
#     u = generator(g, a, p)
#     v = generator(g, b, p)
#     shared_key = generator(v, a, p)

#     constant = 311
#     ascii_values = [cipher_char // (shared_key * constant) for cipher_char in cipher if cipher_char != 0]
#     semi_plaintext = ''.join(chr(value) for value in ascii_values)
#     return dynamic_xor_decrypt(semi_plaintext, text_key)

def dec(cipher, key):
    plaintext = ""
    for encrypted_value in cipher:
        decrypted_value = encrypted_value // (key * 311)
        plaintext += chr(decrypted_value)
    return plaintext

if __name__ == "__main__":
    cipher = [131553, 993956, 964722, 1359381, 43851, 1169360, 950105, 321574, 1081658, 613914, 0, 1213211, 306957, 73085, 993956, 0, 321574, 1257062, 14617, 906254, 350808, 394659, 87702, 87702, 248489, 87702, 380042, 745467, 467744, 716233, 380042, 102319, 175404, 248489]
    a = 94
    b = 21
    g = 31
    p = 97

    text_key = "trudeau"

    u = generator(g, a, p)
    v = generator(g, b, p)
    key = generator(v, a, p)
    b_key = generator(u, b, p)

    shared_key = None

    if key == b_key:
        shared_key = key
    else:
        print("deo co key")
    
    semi_cipher = dec(cipher, shared_key)
    flag = dynamic_xor_decrypt(semi_cipher, text_key)
    print(f"Decrypted message: {flag}")