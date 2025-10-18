import sys, base64, hashlib, binascii
from cryptography.hazmat.primitives.serialization import load_pem_public_key, Encoding, PublicFormat
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def read_pub(path: str):
    with open(path, "rb") as f:
        pem = f.read()
    pub = load_pem_public_key(pem)
    cands = []
    cands.append(pem)
    stripped = b"".join(line for line in pem.splitlines() if not line.startswith(b"-----"))
    cands.append(stripped)
    der_spki = pub.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
    cands.append(der_spki)
    try:
        der_pkcs1 = pub.public_bytes(Encoding.DER, PublicFormat.PKCS1)
        cands.append(der_pkcs1)
    except Exception:
        pass
    try:
        pn = pub.public_numbers()
        if isinstance(pn, rsa.RSAPublicNumbers):
            n = pn.n
            e = pn.e
            be = n.to_bytes((n.bit_length()+7)//8, 'big')
            cands += [be, str(n).encode(), hex(n).encode(), f"{n}:{e}".encode(), f"{hex(n)}:{hex(e)}".encode()]
    except Exception:
        pass
    uniq = []
    seen = set()
    for b in cands:
        if b not in seen:
            uniq.append(b); seen.add(b)
    return pub, uniq

def try_decrypt_all(ct: bytes, k_bytes_list):
    res = []
    layouts = []
    if len(ct) >= 12+16+1:
        layouts.append(("AESGCM12", ct[:12], ct[12:-16], ct[-16:], "aesgcm"))
    if len(ct) >= 16+16+1:
        layouts.append(("AESGCM16", ct[:16], ct[16:-16], ct[-16:], "aesgcm"))
    if len(ct) >= 12+16+1:
        layouts.append(("CHACHA", ct[:12], ct[12:-16], ct[-16:], "chacha"))
    if len(ct) % 16 == 0 and len(ct) >= 32:
        layouts.append(("AESCBC", ct[:16], ct[16:], b"", "aescbc"))
    for label, iv, body, tag, mode in layouts:
        for ksrc in k_bytes_list:
            key = sha256(ksrc)
            try:
                if mode == "aesgcm":
                    a = AESGCM(key)
                    pt = a.decrypt(iv, body+tag, None)
                elif mode == "chacha":
                    a = ChaCha20Poly1305(key)
                    pt = a.decrypt(iv, body+tag, None)
                else:
                    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
                    dec = cipher.decryptor().update(body) + cipher.decryptor().finalize()
                    p = dec[-1]
                    if 1 <= p <= 16 and dec.endswith(bytes([p])*p):
                        pt = dec[:-p]
                    else:
                        pt = dec
                res.append((label, ksrc[:64], pt))
            except Exception as e:
                continue
    return res

def main():
    if len(sys.argv) != 3:
        print("Usage: decrypt_flag.py public.pem flag.enc.bin", file=sys.stderr)
        sys.exit(2)
    pub_path = sys.argv[1]
    ct_path = sys.argv[2]
    _, ksrcs = read_pub(pub_path)
    with open(ct_path, "rb") as f:
        ct = f.read()
    trials = try_decrypt_all(ct, ksrcs)
    hits = [(m, src, pt) for (m, src, pt) in trials if b"CSCV{" in pt and 0x7f not in pt]
    if hits:
        hits_sorted = sorted(hits, key=lambda t: len(t[2]))
        m, src, pt = hits_sorted[0]
        import re
        mobj = re.search(rb"CSCV\{[^}]+\}", pt)
        if mobj:
            print(mobj.group(0).decode())
            return
        print(pt.decode(errors="ignore"))
        return
    for m, src, pt in trials[:5]:
        print(m, len(pt), binascii.hexlify(pt[:32]))
    print("No flag found. Try adding more KDF candidates.")
    sys.exit(1)

if __name__ == "__main__":
    main()
