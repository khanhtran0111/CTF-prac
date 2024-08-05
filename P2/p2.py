import base64

with open('d:/Coding/Practice CTF/CTF-prac/P2/p2.txt', 'r') as file:
    data = file.read()

data = data.encode()

data = bytes.fromhex(data.decode())
print(data)