import base64

with open('D:/Coding/Practice CTF/CTF-prac/the cryptopals crypto challenges/p1/p1.txt', 'r') as file:
    data = file.read()

#data = data.encode()
data = bytes.fromhex(data)
#print(data)
data = base64.b64encode(data).decode()

print(data)