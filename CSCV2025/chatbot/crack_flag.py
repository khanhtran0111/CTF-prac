import sys, hashlib, hmac, binascii
from cryptography.hazmat.primitives.serialization import load_pem_public_key, Encoding, PublicFormat
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def sha256(b): return hashlib.sha256(b).digest()
def hmac256(k,m): return hmac.new(k,m,hashlib.sha256).digest()

if len(sys.argv)!=3:
    print("Usage: python3 crack_flag.py public.pem flag.enc.bin", file=sys.stderr); sys.exit(2)

pem = open(sys.argv[1],'rb').read()
try:
    pub = load_pem_public_key(pem)
    der_spki = pub.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
except Exception:
    print("public.pem không hợp lệ"); sys.exit(1)

ct = open(sys.argv[2],'rb').read()
iv, body = ct[:16], ct[16:]  # AES-CBC layout

pepper = b"qVIp02d"

# sinh tập khóa thử
cands = set()
# chỉ từ PEM/DER
cands.add(sha256(pem))
cands.add(sha256(der_spki))
# trộn pepper theo nhiều cách phổ biến
for base in (pem, der_spki):
    cands.add(sha256(base + pepper))
    cands.add(sha256(pepper + base))
    cands.add(hmac256(pepper, base))
    cands.add(hmac256(base, pepper))
# thêm một số biến thể băm lồng nhau
for base in (pem, der_spki):
    cands.add(sha256(sha256(base) + pepper))
    cands.add(sha256(pepper + sha256(base)))

def try_aes_cbc(key):
    dec = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor().update(body) + \
          Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor().finalize()
    # PKCS#7 unpad nếu hợp lệ
    p = dec[-1]
    if 1<=p<=16 and dec.endswith(bytes([p])*p): dec = dec[:-p]
    return dec

hits = []
for k in cands:
    pt = try_aes_cbc(k)
    if b"CSCV{" in pt and 0x00 not in pt[:2]:
        hits.append(pt)

if hits:
    import re
    s = hits[0].decode('utf-8','ignore')
    m = re.search(r'CSCV\{[^}]+\}', s)
    print(m.group(0) if m else s)
else:
    # in chẩn đoán ngắn gọn
    print("Chưa mở được. Thử khác KDF hoặc thuật toán.")