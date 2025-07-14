with open('./enc', 'rb') as f:
    raw = f.read()
try:
    enc = raw.decode('utf-8')
except UnicodeDecodeError:
    enc = raw.decode('latin-1')

# Thuật toán decoding:
# Mỗi ký tự trong enc là kết quả của
#    codepoint = (ord(flag[i]) << 8) + ord(flag[i+1])
# Do đó để lấy lại hai ký tự gốc ta làm:
flag_chars = []
for c in enc:
    code = ord(c)
    high = code >> 8         
    low  = code & 0xFF       
    flag_chars.append(chr(high))
    flag_chars.append(chr(low))

flag = ''.join(flag_chars)
print(flag)
