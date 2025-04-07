import base64
import binascii
import codecs
import urllib.parse

# Gợi ý: đáp án có thể là ZITF{...}
prefix = "ZiTF{"
suffix = "}"

# Các phần mã hóa sau prefix
parts = ["a1c", "e1", "14", "1ed", "f220e", "1416e06", "c6dc"]

# Hàm decode Base64
def decode_base64(text):
    try:
        padding_needed = len(text) % 4
        if padding_needed:
            text += "=" * (4 - padding_needed)
        return base64.b64decode(text).decode('utf-8', 'ignore')
    except Exception:
        return ""

# Hàm decode HEX
def decode_hex(text):
    try:
        if len(text) % 2:
            text = '0' + text
        return bytes.fromhex(text).decode('utf-8', 'ignore')
    except Exception:
        return ""

# Hàm decode ROT13
def decode_rot13(text):
    try:
        return codecs.decode(text, 'rot_13')
    except Exception:
        return ""

# Hàm URL decode
def decode_url(text):
    try:
        return urllib.parse.unquote(text)
    except Exception:
        return ""

# In kết quả decode từng phần và ghép thử flag
decoded_candidates = []

for idx, part in enumerate(parts):
    b64 = decode_base64(part)
    hx = decode_hex(part)
    rot = decode_rot13(part)
    url = decode_url(part)

    decoded_candidates.append([b64, hx, rot, url])

print("\n--- DECODED CANDIDATES BY PART ---")
for idx, cands in enumerate(decoded_candidates):
    print(f"Part {idx+1}: {parts[idx]}")
    print("  Base64:", cands[0])
    print("  Hex   :", cands[1])
    print("  ROT13 :", cands[2])
    print("  URL   :", cands[3])

# Thử tất cả tổ hợp (chọn 1 phương pháp cho mỗi phần)
from itertools import product

print("\n--- FLAG CANDIDATES ---")

for combo in product(*decoded_candidates):
    candidate = prefix + ''.join(combo) + suffix
    if all(c.isprintable() for c in candidate):
        print(candidate)
