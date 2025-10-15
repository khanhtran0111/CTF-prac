from collections import Counter
import math
import binascii


b = b'\xe9\x81\xd9mA\x98\xa8\x06\x0beO\xe2\x9c\xae\x91\x0cF\xf9gx\xb7\x81S\xf6\xb8\xb2\xcb\xd0\x93\x82\x01N\x99ea\x9aq\x17J%\xa5\xcbQ\xee\x08\xe2\xdfWQ2}\x1c7\xc3\x94\x8d\xa5\x84\x18\xbf\xcdr>]'

print(len(b))

print("hex: ", b.hex())

print("first 32 hex char: ", b.hex()[:64])

freq = Counter(b)
entropy = -sum((count/len(b)) * math.log2(count/len(b)) for count in freq.values())
print("entropy (bits/byte) =", entropy)

blocks = [b[i:i+16] for i in range(0, len(b), 16)]
print("16-byte blocks:", len(blocks))
for i,blk in enumerate(blocks):
    print(i, blk.hex())
print("duplicate blocks:", len(blocks) - len(set(blocks)))

def score_ascii(x):
    return sum(ch in b'etaoin shrdluETAOIN SHRDLU' for ch in x)
for key in range(256):
    xored = bytes([c ^ key for c in b])
    if all(32 <= ch < 127 or ch in (9,10,13) for ch in xored[:40]):
        print("key", key, xored[:80])