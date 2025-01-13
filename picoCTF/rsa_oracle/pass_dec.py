import base64 

decoded_password_hex = "95bcff5132c554882dbc3f5447fa8573"

password_bytes = bytes.fromhex(decoded_password_hex)

try:
    password_text = password_bytes.decode('utf-8')
    print("Decrypted password (human-readable):", password_text)
except UnicodeDecodeError:
    print("The password is not plain text. It may be binary data or encoded differently.")
    print("Password as raw bytes:", password_bytes)
    print("Password as Base64:", base64.b64encode(password_bytes).decode())
