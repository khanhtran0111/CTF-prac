with open('D:/Coding/CTF-prac/the cryptopals crypto challenges/p5/string.txt') as f:
    input_string = f.read()

with open('D:/Coding/CTF-prac/the cryptopals crypto challenges/p5/key.txt') as f:
    key = f.read()

def repeating_key_xor(plaintext, key):
    res = []
    key_len = len(key)
    m = len(plaintext)
    plaintext_byte = plaintext.encode()
    key_byte = key.encode()
    for i in range (len((plaintext))):
        res.append(plaintext_byte[i]^key_byte[i % key_len])
    
    return ''.join(f'{byte:02x}' for byte in res)
    # You XOR each byte of the plaintext with the corresponding byte of the key, and then you want to 
    # represent that XOR result in hexadecimal. Since each XOR operation results in a byte, this line
    # this thi function ensures that each byte is represented as a clean two-character hex value.


message = repeating_key_xor(input_string, key)
print(message)

#Resault:
#0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f