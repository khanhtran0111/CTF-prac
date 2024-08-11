from OpenSSL import crypto

csr_file_path = 'D:/Coding/Practice CTF/CTF-prac/picoCTF/readmycert.csr'

with open(csr_file_path, 'r') as csr_file:
    csr_data = csr_file.read()
    csr_file.close()

csr = crypto.load_certificate_request(crypto.FILETYPE_PEM, csr_data)

subject = csr.get_subject()

print(subject)
