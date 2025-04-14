def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    padding_len = block_size - (len(data) % block_size)
    padding = bytes([padding_len] * padding_len)
    return data + padding

data = b"YELLOW SUBMARINE"
target_length = 20
block_size = target_length

padded = pkcs7_pad(data, block_size)
print(padded)
