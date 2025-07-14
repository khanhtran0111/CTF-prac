import ast, hashlib, re

lines = open('enc_flag','r').read().splitlines()
key_literal = lines[0].split('Key:')[1].strip()
cipher_literal = lines[1].split('Encrypted Blockchain:')[1].strip()
key_bytes    = ast.literal_eval(key_literal)
cipher_bytes = ast.literal_eval(cipher_literal)
key_hash = hashlib.sha256(key_bytes).digest()
block_size = 16
plain = b''
for i in range(0, len(cipher_bytes), block_size):
    blk = cipher_bytes[i:i+block_size]
    plain += bytes(b ^ k for b, k in zip(blk, key_hash))
pad_len = plain[-1]
plain   = plain[:-pad_len]
text = plain.decode('utf-8')

m = re.search(r'picoCTF\{.*?\}', text)

print(m.group(0))