import base64  # Importing base64 module

# Hexadecimal representation of the password
decoded_password_hex = "95bcff5132c554882dbc3f5447fa8573"

# Convert hex to bytes
password_bytes = bytes.fromhex(decoded_password_hex)

# Try decoding to human-readable text
try:
    password_text = password_bytes.decode('utf-8')  # Attempt UTF-8 decoding
    print("Decrypted password (human-readable):", password_text)
except UnicodeDecodeError:
    print("The password is not plain text. It may be binary data or encoded differently.")
    print("Password as raw bytes:", password_bytes)
    print("Password as Base64:", base64.b64encode(password_bytes).decode())  # Encode to Base64 for further analysis
