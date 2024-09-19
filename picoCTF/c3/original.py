lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"

with open('D:/Coding/CTF-prac/picoCTF/c3/ciphertext','r') as f:
    ciphertext = f.read()


prev = 0
out=""
for letter in ciphertext:
    ind = lookup2.index(letter)
    for x in range(100000):
        if (x - prev) % 40 == ind:
            out += lookup1[x]
            prev = x
            break
print(out)