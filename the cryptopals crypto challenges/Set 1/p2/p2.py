def xor_mix(str1, str2):
    #Nhận vào hai chuỗi thành các bytes tương ứng
    bytes1 = bytes.fromhex(str1)
    bytes2 = bytes.fromhex(str2)
    #zip(bytes1, bytes2) để kết hợp từng cặp bytes từ 'bytes1' và 'bytes2'
    # a ^ b: phép XOR
    # bytes(...): chuyển kết quả phép XOR thành các bytes tương ứng.
    xor_res = bytes(a ^ b for a,b in zip(bytes1, bytes2))
    #chuyển chuỗi bytes về xâu Hex
    return xor_res.hex()

hex_str1 = input()
hex_str2 = input()

res = xor_mix(hex_str1, hex_str2)

print(res)