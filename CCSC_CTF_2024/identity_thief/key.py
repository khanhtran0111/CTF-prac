from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ciphertext_hex: hex you already have
ciphertext = bytes.fromhex("e981d96d4198a8060b654fe29cae910c46f96778b78153f6b8b2cbd09382014e9965619a71174a25a5cb51ee08e2df5751327d1c37c3948da58418bfcd723e5d")  

def key_from_C(C):
    h = sha256()
    h.update(str(C).encode())      # dùng chính xác str(C) như Sage in ra
    return h.digest()[16:32]

key = key_from_C(C)   # C phải là object/biểu diễn giống Sage -> convert sang str như Sage
cipher = AES.new(key, AES.MODE_CBC, iv)
pt = unpad(cipher.decrypt(ciphertext), 16)
print(pt)
