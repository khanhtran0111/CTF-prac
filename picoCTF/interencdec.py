import string
import base64
def decrypt_flag(flag):
    decrypted_flag = ""
    for char in flag:
        if char.isalpha() and char.islower():
            decrypted_flag += chr((ord(char) - 7 - ord('a')) % 26 + ord('a'))
        elif char.isalpha() and char.isupper():
            decrypted_flag += chr((ord(char) - 7 - ord('A')) % 26 + ord('A'))
        else:
            decrypted_flag += char
    return decrypted_flag

with open('D:/Coding/Practice CTF/CTF-prac/picoCTF/enc_flag.txt', 'r') as file:
    data = file.read()
    file.close()

decode_bytes = base64.b64decode(data)
flag = decode_bytes.decode('utf-8')
print(flag)

#flag = "wpjvJAM{jhlzhy_k3jy9wa3k_h47j6k69}"
decrypted_flag = decrypt_flag(flag)
print(decrypted_flag)