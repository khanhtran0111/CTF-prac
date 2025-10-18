n=int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141",16)
import sys
s1=int(sys.argv[1],16); s2=int(sys.argv[2],16)
c1=int(sys.argv[3],16)%n; c2=int(sys.argv[4],16)%n; cT=int(sys.argv[5],16)%n
inv=pow((c1-c2)%n,-1,n)
print(f"{(s1 + ((cT-c1)%n)*((s1-s2)%n)*inv)%n:064x}")
