from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii
import itertools

cipher_hex = "e981d96d4198a8060b654fe29cae910c46f96778b78153f6b8b2cbd09382014e9965619a71174a25a5cb51ee08e2df5751327d1c37c3948da58418bfcd723e5d"
cipher_hex = cipher_hex.strip()
cipher = bytes.fromhex(cipher_hex)

iv = b"Identity_Thief!!"

candidates = [
    "O",
    "O_E",               
    "Point at infinity",
    "Infinity",
    "Point(infinity)",
    "point at infinity",
    "0:1:0",
    "(0 : 1 : 0)",
    "(0:1:0)",
    "(0, 1, 0)",
    "(0,1,0)",
    "(", ")",
    "()", 
    "Point(0, 1, 0)", 
    "Point(0 : 1 : 0)",
    "0 : 1 : 0",
    "0 : 1 : 0 on E",   
    "O on E",
]

more = []
for s in candidates:
    more.append(s)
    more.append(s + "\n")
    more.append(" " + s)
    more.append(s + " ")
    more.append("'" + s + "'")
    more.append("\"" + s + "\"")
    more.append("Point " + s)
    more.append("E" + s)
candidates = list(dict.fromkeys(more))  

def key_from_cstr(s):
    h = sha256()
    h.update(s.encode())
    return h.digest()[16:32]

def plausible_plaintext(pt):
    try:
        t = pt.decode('utf-8')
    except:
        return False
    if any(c.isalpha() for c in t) and sum(1 for ch in t if ch.isprintable()) > len(t)*0.8:
        return True
    if "flag" in t.lower() or "CTF" in t or "{" in t and "}" in t:
        return True
    return False

for s in candidates:
    key = key_from_cstr(s)
    try:
        cipherobj = AES.new(key, AES.MODE_CBC, iv)
        pt = cipherobj.decrypt(cipher)
        try:
            pt2 = unpad(pt, 16)
        except ValueError:
            continue
        if plausible_plaintext(pt2):
            print("+++ Found plausible plaintext with str(C) = {!r} +++".format(s))
            print("Key (hex):", key.hex())
            print("Plaintext:")
            print(pt2)
            break
    except Exception as e:
        continue
else:
    print("No candidate produced plausible plaintext. You can add more candidate strings to the list.")
    print("Tried {} candidates.".format(len(candidates)))
