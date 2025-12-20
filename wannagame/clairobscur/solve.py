from sage.all import *
from Crypto.Util.number import long_to_bytes
import sys

# Strategy: We control p, G, and O
# We can choose a small prime p to make discrete log easy
# The curve equation is: a*b^2 + b*c^2 + c*d^2 + d*a^2 = 0

# Choose a small prime for easy discrete log
p = 2**20 - 3  # Small prime, about 20 bits

# We need to find points on the curve
# Let's try to find simple points
Fp = GF(p)

# Try to find a generator point G
# For a=1, b=0, c=0, d=0: 1*0 + 0*0 + 0*0 + 0*1 = 0 ✓
# But this might be a trivial point

# Let's try a=0, b=1, c=0, d=0: 0*1 + 1*0 + 0*0 + 0*0 = 0 ✓
# Or a=1, b=1, c=0, d=-1: 1*1 + 1*0 + 0*1 + (-1)*1 = 1 - 1 = 0 ✓

# Let me find valid points systematically
def is_on_curve(p, point):
    a, b, c, d = point
    Fp = GF(p)
    a, b, c, d = Fp(a), Fp(b), Fp(c), Fp(d)
    return a * b**2 + b * c**2 + c * d**2 + d * a**2 == 0

# Find a generator point
def find_points(p, count=10):
    Fp = GF(p)
    points = []
    
    for a in range(min(100, p)):
        for b in range(min(100, p)):
            for c in range(min(100, p)):
                if len(points) >= count:
                    return points
                # Solve for d: a*b^2 + b*c^2 + c*d^2 + d*a^2 = 0
                # d*a^2 + c*d^2 = -a*b^2 - b*c^2
                # d*(a^2 + c*d) = -a*b^2 - b*c^2
                
                # Try to solve for d
                x = Fp['d'].gen()
                eq = Fp(a) * Fp(b)**2 + Fp(b) * Fp(c)**2 + Fp(c) * x**2 + x * Fp(a)**2
                roots = eq.roots()
                for d, _ in roots:
                    pt = [int(a), int(b), int(c), int(d)]
                    if pt not in points:
                        points.append(pt)
                        if len(points) >= count:
                            return points
    return points

print(f"Finding points on curve with p = {p}...")
points = find_points(p, 5)
print(f"Found {len(points)} points")
for i, pt in enumerate(points):
    print(f"Point {i}: {pt}, on_curve: {is_on_curve(p, pt)}")

# Use first two distinct points as G and O
G = points[0]
O = points[1]

print(f"\nChosen parameters:")
print(f"p = {p}")
print(f"G = {','.join(map(str, G))}")
print(f"O = {','.join(map(str, O))}")

print("\nSend these to the challenge:")
print(p)
print(','.join(map(str, G)))
print(','.join(map(str, O)))

print("\n" + "="*60)
print("After getting P from the server, paste it here:")
print("="*60)
