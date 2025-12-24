import hashlib

target = "f33e7acc20580138923e9e07f3f02536"

def md5_hex(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()

candidate = "CYsTaCK"  
print(md5_hex(candidate))
print("match?", md5_hex(candidate) == target)
