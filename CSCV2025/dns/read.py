import re, csv, sys
rows=[]
with open('exfil.csv', newline='', encoding='utf-8', errors='ignore') as f:
    r=csv.reader(f)
    hdr=next(r,None)
    for time_epoch,qname in r:
        try: t=float(time_epoch)
        except: continue
        m=re.fullmatch(r'(?:p|f)\.([0-9a-f]+)\.hex\.cloudflar3\.com\.?', qname)
        if m: rows.append((t, m.group(1)))
rows.sort(key=lambda x:x[0])
hex_chunks=[hx for _,hx in rows]
full_hex=''.join(hex_chunks)
open('payload.hex','w').write(full_hex)
data=bytes.fromhex(full_hex) if full_hex else b''
open('payload.bin','wb').write(data)
print("chunks:", len(hex_chunks), "bytes:", len(data))