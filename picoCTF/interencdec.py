import string
import base64

with open('D:/Coding/Practice CTF/CTF-prac/picoCTF/enc_flag.txt', 'r') as file:
    data = file.read()
    file.close()

#data = data.encode()
#data = bytes.fromhex(data.decode())
data = base64.b64decode(data)
data = bytes.fromhex(data)
print(data)