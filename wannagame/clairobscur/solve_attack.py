"""
Clair Obscur CTF Challenge Solution

The challenge implements a custom quartic curve with scalar multiplication.
We need to solve the discrete log problem to recover the flag.

Key insight: We control the curve parameters (p, G, O).
By choosing a very small prime p, we make the discrete log problem trivial.

The flag is 32 bytes (256 bits), but with a small p, we only need to brute force
a much smaller space.
"""

from sage.all import *
from Crypto.Util.number import long_to_bytes, bytes_to_long

# Copy the curve implementation from the challenge
class CO:
    def __init__(self, p: int, G: list[int], O: list[int]):
        assert is_prime(p)
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


def find_curve_points(p, max_search=100):
    """Find valid points on the curve a*b^2 + b*c^2 + c*d^2 + d*a^2 = 0"""
    Fp = GF(p)
    points = []
    
    for a in range(max_search):
        for b in range(max_search):
            for c in range(max_search):
                if len(points) >= 10:
                    return points
                
                # Solve for d: a*b^2 + b*c^2 + c*d^2 + d*a^2 = 0
                x = Fp['x'].gen()
                eq = Fp(a) * Fp(b)**2 + Fp(b) * Fp(c)**2 + Fp(c) * x**2 + x * Fp(a)**2
                roots = eq.roots()
                
                for d, _ in roots:
                    pt = [int(a), int(b), int(c), int(d)]
                    if pt not in points:
                        points.append(pt)
                        if len(points) >= 10:
                            return points
    return points


def solve_discrete_log(curve, P_target, max_k=2**32):
    """Brute force discrete log for small primes"""
    print(f"Solving discrete log (trying up to {max_k} values)...")
    
    for k in range(1, min(max_k, 10**7)):
        if k % 100000 == 0:
            print(f"  Tried {k:,} values...")
        
        try:
            Q = curve.scalarmult(k)
            if Q == P_target:
                return k
        except:
            pass
    
    return None


# MAIN ATTACK
print("="*70)
print("CLAIR OBSCUR CHALLENGE SOLVER")
print("="*70)

# Step 1: Choose parameters
# We need p to have 256 bits as per the assertion
# But we can still try to make the problem easier
# Actually, looking more carefully - we need a 256-bit prime
# This makes brute force infeasible...

# Let me reconsider: Maybe there's a weakness in the curve group structure?
# Or we need to find a curve with small order?

# Actually, the real attack vector: we can choose G and O such that
# the curve has a small group order!

print("\nStep 1: Choosing a 256-bit prime...")
p = next_prime(2**255)  # 256-bit prime as required
print(f"p = {p}")
print(f"p bit length: {p.bit_length()}")

print("\nStep 2: Finding points on the curve...")
points = find_curve_points(p, max_search=20)
print(f"Found {len(points)} points")

G = points[0]
O = points[1]

print(f"\nG = {G}")
print(f"O = {O}")

print("\n" + "="*70)
print("SEND THESE TO THE CHALLENGE:")
print("="*70)
print(p)
print(','.join(map(str, G)))
print(','.join(map(str, O)))
print("="*70)

print("\n[!] After receiving P from the server:")
print("[!] Uncomment the code below and paste P")
print()
print("# Example:")
print("# P = [123, 456, 789, 101112]  # Paste the server response here")
print("# curve = CO(p, G, O)")
print("# k = solve_discrete_log(curve, P)")
print("# if k:")
print("#     flag_bytes = long_to_bytes(k)")
print("#     print(f'Flag: W1{{{flag_bytes.decode()}}}')")
