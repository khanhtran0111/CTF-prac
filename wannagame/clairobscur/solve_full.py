from sage.all import *
from Crypto.Util.number import long_to_bytes

# Copy the CO class from the challenge
class CO:
    def __init__(self, p: int, G: list[int], O: list[int]):
        assert is_prime(p)
        assert p.bit_length() == 256
        self.Fp = GF(p)
        self.G = [self.Fp(c) for c in G]
        self.O = [self.Fp(c) for c in O]
        assert self.is_on_curve(self.G)
        assert self.is_on_curve(self.O)

        self.L = self.random_element_from_basis(matrix(self.Fp, [self.G, self.O]).right_kernel_matrix())

    def random_element_from_basis(self, M):
        val = 0
        n = M.nrows()
        Fp = M.base_ring()
        for i in range(n):
            val += Fp.random_element() * M[i]
        return val
    
    def random_point(self):
        while True:
            a, b, c = [self.Fp.random_element() for _ in range(3)]
            x = self.Fp["d"].gen()
            f = a * b**2 + b * c**2 + c * x**2 + x * a**2
            r = f.roots()
            if len(r) > 0:
                d = r[0][0]
                assert self.is_on_curve([a, b, c, d])
                return [a, b, c, d]

    def is_on_curve(self, G: list):
        return G[0] * G[1]**2 + G[1] * G[2]**2 + G[2] * G[3]**2 + G[3] * G[0]**2 == 0

    def neg(self, P: list):
        if P == self.O:
            return P
        
        return self.intersect(P, self.O)
    
    def intersect(self, P: list, Q: list):
        aa = P[0] - Q[0]
        bb = P[1] - Q[1]
        cc = P[2] - Q[2]
        dd = P[3] - Q[3]
        A = aa * bb**2 + bb * cc**2 + cc * dd**2 + dd * aa**2
        C =   (P[1]**2 + 2 * P[0] * P[3]) * aa \
            + (P[2]**2 + 2 * P[0] * P[1]) * bb \
            + (P[3]**2 + 2 * P[1] * P[2]) * cc \
            + (P[0]**2 + 2 * P[2] * P[3]) * dd
        t = -C / A
        R = [0] * 4
        R[0] = P[0] + t * aa
        R[1] = P[1] + t * bb
        R[2] = P[2] + t * cc
        R[3] = P[3] + t * dd

        return R
    
    def add(self, P: list, Q: list):
        if P == self.O:
            return Q
        if Q == self.O:
            return P
        if P == self.neg(Q):
            return self.O
        R = self.intersect(P, Q)
        return self.neg(R)
    
    def double(self, P: list):
        Fa = 2 * P[0] * P[3] + P[1]**2
        Fb = 2 * P[0] * P[1] + P[2]**2
        Fc = 2 * P[1] * P[2] + P[3]**2
        Fd = 2 * P[2] * P[3] + P[0]**2
        vb = Matrix(self.Fp, [[Fa, Fb, Fc, Fd], self.L]).right_kernel_matrix()
        vx, vy, vz, vw = self.random_element_from_basis(vb)

        C3 = vx * vy**2 + vy * vz**2 + vz * vw**2 + vw * vx**2
        C2 =  P[0] * (2 * vw * vx + vy**2) \
            + P[1] * (2 * vx * vy + vz**2) \
            + P[2] * (2 * vy * vz + vw**2) \
            + P[3] * (2 * vw * vz + vx**2)
        t = -C2 / C3

        R = [0] * 4
        R[0] = P[0] + t * vx
        R[1] = P[1] + t * vy
        R[2] = P[2] + t * vz
        R[3] = P[3] + t * vw

        return self.neg(R)
    
    def scalarmult(self, k: int):
        assert k > 0
        R = None
        Q = self.G
        while k > 0:
            if k & 1:
                if R is None:
                    R = Q
                else:
                    R = self.add(R, Q)
            Q = self.double(Q)
            k >>= 1
        return R


# Brute force discrete log for small p
def discrete_log_bruteforce(curve, P):
    print("Brute forcing discrete log...")
    # The flag is 32 bytes, so max value is 256^32
    # But we can try smaller values first
    
    max_tries = 2**40  # Adjust based on p size
    
    for k in range(1, max_tries):
        if k % 100000 == 0:
            print(f"Tried {k} values...")
        
        try:
            Q = curve.scalarmult(k)
            if Q == P:
                print(f"Found k = {k}")
                return k
        except:
            continue
    
    return None


# Main solving logic
print("Step 1: Choose a small prime p for easy discrete log")
p = next_prime(2**20)  # Small prime
print(f"p = {p}")

print("\nStep 2: Find points on the curve")
Fp = GF(p)

def find_points(p, count=10):
    Fp = GF(p)
    points = []
    
    for a in range(min(50, p)):
        for b in range(min(50, p)):
            for c in range(min(50, p)):
                if len(points) >= count:
                    return points
                x = Fp['d'].gen()
                eq = Fp(a) * Fp(b)**2 + Fp(b) * Fp(c)**2 + Fp(c) * x**2 + x * Fp(a)**2
                roots = eq.roots()
                for d, _ in roots:
                    pt = [int(a), int(b), int(c), int(d)]
                    if pt not in points:
                        points.append(pt)
    return points

points = find_points(p, 5)
G = points[0]
O = points[1]

print(f"\nG = {G}")
print(f"O = {O}")

print("\n" + "="*60)
print("Send these inputs to the challenge:")
print("="*60)
print(f"p = {p}")
print(f"G = {','.join(map(str, G))}")
print(f"O = {','.join(map(str, O))}")
print("="*60)

# For testing locally or after getting P from server
# P = [...]  # Paste the result from the server here
# curve = CO(p, G, O)
# k = discrete_log_bruteforce(curve, P)
# if k:
#     flag_bytes = long_to_bytes(k)
#     print(f"Flag: W1{{{flag_bytes.decode()}}}")
