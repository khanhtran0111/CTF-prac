#Đề bài: Translate mã ở file hex64.txt
import base64

with open('d:/Coding/Practice CTF/CTF-prac/P1/hex64.txt', 'r') as file:
    data = file.read()

data = data.encode()
for i in range(15):
    data = bytes.fromhex(data.decode())
    data = base64.b64decode(data)

print(data.decode())

