"""
Simplified solution using only Python (no SageMath required)
This generates parameters for the challenge
"""

def is_prime(n):
    """Simple primality test"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def next_prime(n):
    """Find next prime after n"""
    candidate = n + 1
    while not is_prime(candidate):
        candidate += 1
    return candidate

def mod_inverse(a, m):
    """Modular inverse using extended Euclidean algorithm"""
    if a < 0:
        a = (a % m + m) % m
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

def extended_gcd(a, b):
    """Extended Euclidean algorithm"""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

class FieldElement:
    """Simple finite field element"""
    def __init__(self, value, modulus):
        self.value = value % modulus
        self.modulus = modulus
    
    def __add__(self, other):
        return FieldElement((self.value + other.value) % self.modulus, self.modulus)
    
    def __sub__(self, other):
        return FieldElement((self.value - other.value) % self.modulus, self.modulus)
    
    def __mul__(self, other):
        return FieldElement((self.value * other.value) % self.modulus, self.modulus)
    
    def __truediv__(self, other):
        inv = mod_inverse(other.value, self.modulus)
        return FieldElement((self.value * inv) % self.modulus, self.modulus)
    
    def __pow__(self, exp):
        return FieldElement(pow(self.value, exp, self.modulus), self.modulus)
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __repr__(self):
        return str(self.value)

def find_points_on_curve(p, max_search=30):
    """Find points satisfying a*b^2 + b*c^2 + c*d^2 + d*a^2 = 0 (mod p)"""
    points = []
    
    print(f"[*] Searching for points on curve (mod {p})...")
    
    for a in range(max_search):
        for b in range(max_search):
            for c in range(max_search):
                if len(points) >= 10:
                    return points
                
                # Try to solve for d: a*b^2 + b*c^2 + c*d^2 + d*a^2 = 0
                # This is: d*a^2 + c*d^2 = -(a*b^2 + b*c^2)
                # Or: d*(a^2 + c*d) = -(a*b^2 + b*c^2)
                
                # Try small values of d
                for d in range(min(100, p)):
                    lhs = (a * b**2 + b * c**2 + c * d**2 + d * a**2) % p
                    if lhs == 0:
                        pt = [a, b, c, d]
                        if pt not in points:
                            points.append(pt)
                            print(f"    Found: {pt}")
                            if len(points) >= 10:
                                return points
    
    return points

def main():
    print("="*80)
    print("         CLAIR OBSCUR - Simplified Python Solution")
    print("="*80)
    
    # Generate a 256-bit prime
    print("\n[1] Generating 256-bit prime...")
    p = next_prime(2**255)
    print(f"    p = {p}")
    print(f"    Bit length: {p.bit_length()}")
    
    # Find points on the curve
    print("\n[2] Finding points on curve...")
    points = find_points_on_curve(p, max_search=30)
    
    if len(points) < 2:
        print("[-] ERROR: Could not find enough points!")
        print("[!] Try running SageMath version instead")
        return
    
    print(f"[+] Found {len(points)} points")
    
    # Select G and O
    G = points[0]
    O = points[1]
    
    print(f"\n[3] Selected parameters:")
    print(f"    G = {G}")
    print(f"    O = {O}")
    
    # Output for challenge
    print("\n" + "="*80)
    print("                    CHALLENGE INPUTS")
    print("="*80)
    print(f"{p}")
    print(f"{','.join(map(str, G))}")
    print(f"{','.join(map(str, O))}")
    print("="*80)
    
    print("\n[*] Copy the above 3 lines to the challenge")
    print("[*] After getting P back, you'll need SageMath to solve the discrete log")

if __name__ == "__main__":
    main()
