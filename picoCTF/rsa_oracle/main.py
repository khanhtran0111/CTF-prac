from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import base64

n = 1234567890123456789012345678901234567890
d = 1234567890123456789012345678901234567890

password_enc_content = '1634668422544022562287275254811184478161245548888973650857381112077711852144181630709254123963471597994127621183174673720047559236204808750789430675058597'
ciphertext = int(password_enc_content)

plaintext = pow(ciphertext, d, n)
decoded_password = long_to_bytes(plaintext).strip()

print("Decrypted password (raw bytes):", decoded_password)
print("Decrypted password (hex):", decoded_password.hex())

secret_enc_path = '/home/khanhtran/Documents/coding/python/CTF-prac/picoCTF/rsa_oracle/secret.enc'

with open(secret_enc_path, "rb") as file:
    content = file.read()

try:
    decoded_content = base64.b64decode(content, validate=True)
except base64.binascii.Error as e:
    print("Error decoding base64 content:", e)
    print("Raw content:", content)
    exit(1)

salt = decoded_content[:16]
ciphertext = decoded_content[16:]

key = PBKDF2(decoded_password, salt, dkLen=32)

cipher = AES.new(key, AES.MODE_CBC, iv=salt)
decrypted_message = cipher.decrypt(ciphertext)

pad_len = decrypted_message[-1]
if pad_len < 1 or pad_len > AES.block_size:
    raise ValueError("Invalid padding")
decrypted_message = decrypted_message[:-pad_len]

try:
    print("Decrypted message:", decrypted_message.decode())
except UnicodeDecodeError:
    print("Decrypted message (raw bytes):", decrypted_message)
    print("Decrypted message (hex):", decrypted_message.hex())
