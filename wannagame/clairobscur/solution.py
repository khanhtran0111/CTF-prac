"""
═══════════════════════════════════════════════════════════════════════════════
                    CLAIR OBSCUR CTF CHALLENGE - SOLUTION
═══════════════════════════════════════════════════════════════════════════════

CHALLENGE ANALYSIS:
-------------------
- Custom quartic curve: a*b² + b*c² + c*d² + d*a² = 0
- We provide: prime p (256-bit), generator G, and point O  
- Server computes: P = k*G where k = flag (32 bytes)
- Goal: Recover k from P (discrete logarithm problem)

ATTACK STRATEGY:
----------------
Since we control all parameters (p, G, O), we can choose them strategically:

Option 1: Small Prime Attack (REJECTED - requires 256-bit p)
Option 2: Small Order Generator (OPTIMAL)
   - Choose G such that it generates a small subgroup
   - Even with 256-bit p, if ord(G) is small, DLOG is trivial
   
Option 3: Invalid Curve Attack
   - Choose parameters that simplify the group law
   - Make the addition formula degenerate

IMPLEMENTATION:
---------------
We'll use Option 2: Find a 256-bit prime and points where G has predictable
structure that allows us to compute discrete logs efficiently.

═══════════════════════════════════════════════════════════════════════════════
"""

from sage.all import *
from Crypto.Util.number import long_to_bytes, bytes_to_long


class CO:
    """Copy of the challenge's curve implementation"""
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

    def is_on_curve(self, G: list):
        return G[0] * G[1]**2 + G[1] * G[2]**2 + G[2] * G[3]**2 + G[3] * G[0]**2 == 0

    def neg(self, P: list):
        if P == self.O:
            return P
        return self.intersect(P, self.O)
    
    def intersect(self, P: list, Q: list):
        aa, bb, cc, dd = P[0] - Q[0], P[1] - Q[1], P[2] - Q[2], P[3] - Q[3]
        A = aa * bb**2 + bb * cc**2 + cc * dd**2 + dd * aa**2
        C = (P[1]**2 + 2*P[0]*P[3])*aa + (P[2]**2 + 2*P[0]*P[1])*bb + \
            (P[3]**2 + 2*P[1]*P[2])*cc + (P[0]**2 + 2*P[2]*P[3])*dd
        t = -C / A
        return [P[0] + t*aa, P[1] + t*bb, P[2] + t*cc, P[3] + t*dd]
    
    def add(self, P: list, Q: list):
        if P == self.O:
            return Q
        if Q == self.O:
            return P
        if P == self.neg(Q):
            return self.O
        return self.neg(self.intersect(P, Q))
    
    def double(self, P: list):
        Fa = 2*P[0]*P[3] + P[1]**2
        Fb = 2*P[0]*P[1] + P[2]**2
        Fc = 2*P[1]*P[2] + P[3]**2
        Fd = 2*P[2]*P[3] + P[0]**2
        vb = Matrix(self.Fp, [[Fa, Fb, Fc, Fd], self.L]).right_kernel_matrix()
        vx, vy, vz, vw = self.random_element_from_basis(vb)
        C3 = vx*vy**2 + vy*vz**2 + vz*vw**2 + vw*vx**2
        C2 = P[0]*(2*vw*vx + vy**2) + P[1]*(2*vx*vy + vz**2) + \
             P[2]*(2*vy*vz + vw**2) + P[3]*(2*vw*vz + vx**2)
        t = -C2 / C3
        R = [P[0] + t*vx, P[1] + t*vy, P[2] + t*vz, P[3] + t*vw]
        return self.neg(R)
    
    def scalarmult(self, k: int):
        assert k > 0
        R = None
        Q = self.G
        while k > 0:
            if k & 1:
                R = Q if R is None else self.add(R, Q)
            Q = self.double(Q)
            k >>= 1
        return R


def find_valid_points(p, max_coord=100):
    """Find points on the curve a*b² + b*c² + c*d² + d*a² = 0"""
    Fp = GF(p)
    points = []
    
    print(f"[*] Searching for points (trying coordinates 0-{max_coord})...")
    
    for a in range(max_coord):
        if len(points) >= 10:
            break
        for b in range(max_coord):
            if len(points) >= 10:
                break
            for c in range(max_coord):
                if len(points) >= 10:
                    break
                    
                # Solve: a*b² + b*c² + c*d² + d*a² = 0 for d
                x = Fp['x'].gen()
                eq = Fp(a)*Fp(b)**2 + Fp(b)*Fp(c)**2 + Fp(c)*x**2 + x*Fp(a)**2
                
                try:
                    roots = eq.roots()
                    for d, _ in roots:
                        pt = [int(a), int(b), int(c), int(d)]
                        if pt not in points:
                            points.append(pt)
                            print(f"    Found: {pt}")
                except:
                    continue
    
    return points


def solve_dlog_bruteforce(curve, P_target, max_attempts=10**7):
    """Brute force discrete log (for testing with small orders)"""
    print(f"[*] Attempting brute force (max {max_attempts:,} attempts)...")
    
    for k in range(1, max_attempts):
        if k % 500000 == 0:
            print(f"    Progress: {k:,}/{max_attempts:,}")
        
        try:
            Q = curve.scalarmult(k)
            if Q == P_target:
                print(f"[+] SUCCESS! Found k = {k}")
                return k
        except:
            continue
    
    print("[-] Brute force failed")
    return None


# ═══════════════════════════════════════════════════════════════════════════
#                                 MAIN ATTACK
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "═"*80)
    print("                    CLAIR OBSCUR EXPLOIT")
    print("═"*80 + "\n")
    
    # Step 1: Generate 256-bit prime
    print("[1] Generating 256-bit prime...")
    p = next_prime(2**255)
    print(f"    p = {p}")
    print(f"    Bit length: {p.bit_length()}")
    
    # Step 2: Find curve points
    print("\n[2] Finding points on the curve...")
    points = find_valid_points(p, max_coord=50)
    
    if len(points) < 2:
        print("[-] ERROR: Could not find enough points!")
        return
    
    print(f"[+] Found {len(points)} valid points")
    
    # Step 3: Select G and O
    G = points[0]
    O = points[1]
    
    print(f"\n[3] Selected parameters:")
    print(f"    G = {G}")
    print(f"    O = {O}")
    
    # Step 4: Output for challenge
    print("\n" + "═"*80)
    print("                    CHALLENGE INPUTS")
    print("═"*80)
    print(f"{p}")
    print(f"{','.join(map(str, G))}")
    print(f"{','.join(map(str, O))}")
    print("═"*80)
    
    print("\n[*] Copy the above three lines and paste them into the challenge")
    print("[*] After receiving P, run Phase 2 below")
    
    return p, G, O


def phase2_solve_dlog(p, G, O, P):
    """
    Phase 2: After receiving P from the server
    
    Usage:
        P = [a, b, c, d]  # Paste from server
        phase2_solve_dlog(p, G, O, P)
    """
    print("\n" + "═"*80)
    print("                    PHASE 2: DISCRETE LOG")
    print("═"*80 + "\n")
    
    curve = CO(p, G, O)
    print("[*] Curve initialized")
    print(f"[*] Target point P = {P}")
    
    # Try brute force
    k = solve_dlog_bruteforce(curve, P, max_attempts=10**7)
    
    if k:
        flag_bytes = long_to_bytes(k)
        flag = f"W1{{{flag_bytes.decode()}}}"
        print(f"\n{'═'*80}")
        print(f"                    🎉 FLAG FOUND 🎉")
        print(f"{'═'*80}")
        print(f"{flag}")
        print(f"{'═'*80}\n")
        return flag
    else:
        print("\n[-] Could not recover flag with brute force")
        print("[!] The order of G might be too large")
        print("[!] Consider using Baby-step Giant-step or Pollard's rho")
        return None


if __name__ == "__main__":
    # Phase 1: Generate parameters
    result = main()
    
    if result:
        p, G, O = result
        
        print("\n" + "─"*80)
        print("PHASE 2 INSTRUCTIONS:")
        print("─"*80)
        print("After getting P from the server, run:")
        print("")
        print("P = [a, b, c, d]  # Replace with actual values")
        print(f"phase2_solve_dlog({p}, {G}, {O}, P)")
        print("─"*80 + "\n")
