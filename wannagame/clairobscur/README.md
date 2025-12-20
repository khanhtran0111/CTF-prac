# Clair Obscur CTF Challenge - Solution

## Challenge Overview

This is a custom elliptic curve-like cryptography challenge that implements operations on a quartic curve.

### The Curve
The challenge uses points on the curve defined by:
```
a·b² + b·c² + c·d² + d·a² = 0
```

Where points are 4-tuples `[a, b, c, d]` over a finite field `GF(p)`.

### The Challenge
- You provide: a 256-bit prime `p`, a generator point `G`, and a point `O`
- Server computes: `P = k·G` where `k` is the flag (encoded as an integer)
- Goal: Recover `k` from `P` (discrete logarithm problem)

## Attack Strategy

### Key Insight
**We control all the parameters!** The challenge lets us choose `p`, `G`, and `O`. This gives us complete control over the curve structure.

### Attack Approach

Since the challenge requires a 256-bit prime, we can't simply use a tiny prime. However, we can still make the problem tractable:

1. **Choose a 256-bit prime `p`**
2. **Find points `G` and `O` on the curve** 
3. **Hope that `G` generates a small subgroup** - Even with a large prime, if the point `G` has small order, the discrete log becomes easy
4. **Use brute force or smart algorithms** to solve DLOG in the small subgroup

### Why This Works
- The order of a point depends on the curve structure, not just the prime
- By choosing specific points (especially simple ones with small coordinates), we might get lucky with small orders
- The flag is only 32 bytes (256 bits), but if we have additional structure, Baby-step Giant-step or Pollard's rho becomes feasible

## Solution Steps

### Phase 1: Generate Parameters

```bash
sage solution.py
```

This will:
1. Generate a 256-bit prime
2. Find valid points on the curve
3. Output the parameters to send to the challenge

### Phase 2: Solve Discrete Log

After receiving `P` from the server:

```python
from solution import phase2_solve_dlog

# Paste the P value from server
P = [a, b, c, d]

# Run the solver (use the p, G, O from Phase 1)
phase2_solve_dlog(p, G, O, P)
```

## Files

- `solution.py` - Main solution script with full implementation
- `chall.py` - Original challenge file
- `README.md` - This file

## Requirements

```bash
# Install SageMath
# On Ubuntu/Debian:
sudo apt-get install sagemath

# Or use Docker:
docker pull sagemath/sagemath
```

## Alternative Approaches

If brute force is too slow:

1. **Baby-step Giant-step**: O(√n) time and space
2. **Pollard's Rho**: O(√n) time, O(1) space
3. **Pohlig-Hellman**: If the order factors nicely
4. **Index Calculus**: For some curve structures

## Flag Format

```
W1{...}
```

Where the content is the 32-byte flag encoded from the discrete log result.

## Notes

- The challenge's custom curve is not a standard elliptic curve
- The group law is defined through line intersections in projective space
- The security relies on the discrete log problem being hard, but with controlled parameters, we can break it
