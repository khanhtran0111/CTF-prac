from Crypto.Util.number import bytes_to_long
cipher_hex = "e981d96d4198a8060b654fe29cae910c46f96778b78153f6b8b2cbd09382014e9965619a71174a25a5cb51ee08e2df5751327d1c37c3948da58418bfcd723e5d"
c = int(cipher_hex, 16)
print("len(hex)=", len(cipher_hex))
print("cipher int =", c)