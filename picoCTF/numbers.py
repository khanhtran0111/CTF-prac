import string

with open('D:/Coding/Practice CTF/CTF-prac/picoCTF/numbers.txt') as file:
    data = file.read()
    file.close()

val = data.split()
alpha = string.ascii_uppercase

res =""
for i in val:
    if i.isdigit():
        res += alpha[int(i) - 1]
    else:
        res += i

print(res)