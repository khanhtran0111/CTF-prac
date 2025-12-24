import base64
import re

hex_str = """
05 73 A0 E0 69 95 D8 5A 13 86 DD 60 9B 06 40 26 07 53 60 2A BC BA DE C0 DE
20 01 41 D0 02 42 33 04 96 74 50 BC EA 7D B8 C1 D7 03 80 18 E1 CF A0 01 01
08 0A 09 3E 69 B9 17 A1 7E D3 47 45 54 20 2F 20 48 54 54 50 2F 31 2E 31 0A
41 75 74 68 6F 72 69 7A 61 74 69 6F 6E 3A 20 42 61 73 69 63 20 51 33 6C 54
64 47 46 6A 61 30 4E 76 62 6D 5A 70 5A 47 56 75 64 47 6C 68 62 41 3D 3D 0A
55 73 65 72 2D 41 67 65 6E 74 3A 20 61 67 65 6E 74 43 0A 48 6F 73 74 3A 20
63 79 73 74 61 63 6B 2E 6E 65 74 0A 41 63 63 65 70 74 3A 20 2A 2F 2A 0A 0A
"""

raw = bytes(int(b, 16) for b in re.findall(r"[0-9A-Fa-f]{2}", hex_str))

idx = raw.find(b"GET ")
if idx == -1:
    raise ValueError("No HTTP payload found")

http = raw[idx:] 
print("HTTP payload (decoded):")
print(http.decode("ascii", errors="replace"))

m = re.search(rb"Authorization:\s*Basic\s+([A-Za-z0-9+/=]+)", http)
if not m:
    raise ValueError("No Basic Authorization header found")

token_b64 = m.group(1).decode("ascii")
secret = base64.b64decode(token_b64).decode("utf-8", errors="replace")

print("\nBase64 token:", token_b64)
print("CONFIDENTIAL:", secret)
