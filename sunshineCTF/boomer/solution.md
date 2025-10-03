# SunshineCTF - Boomer Challenge Writeup 📱

## Challenge Overview

**Challenge Name:** Boomer  
**Category:** Cryptography  
**Input:** `7778866{844444777_7446666633_444777_26622244433668}`  
**Flag:** `sun{this_phone_is_ancient}`

## 1. Understanding T9 Multitap Encoding

T9 (Text on 9 keys) was the standard text input method on old mobile phones before smartphones. Each number key corresponds to multiple letters:

| Key | Letters |
|-----|---------|
| 2   | abc     |
| 3   | def     |
| 4   | ghi     |
| 5   | jkl     |
| 6   | mno     |
| 7   | pqrs    |
| 8   | tuv     |
| 9   | wxyz    |

**How it works:**
- Number of key presses = position of letter in the group
- Examples: `2` = a, `22` = b, `222` = c, `7777` = s

## 2. Initial Analysis & Approach

Starting with the encoded string:
```
7778866{844444777_7446666633_444777_26622244433668}
```

First attempt using standard T9 decoding:
- `777` = r (7×3)
- `88` = u (8×2) 
- `66` = n (6×2)

This gave us "run" - a promising start! But several sequences had too many repeated digits for standard T9.

## 3. The Breakthrough: Decoding "PHONE" 

The key insight came from analyzing the sequence `7446666633`:

Trying different segmentations:
- `744` + `666666` + `33` 
- `7` + `44` + `66666` + `33` 
- `7` + `44` + `666` + `66` + `33` ✅

This gives us:
- `7` = p
- `44` = h  
- `666` = o
- `66` = n
- `33` = e

**Result: "phone"** 

This confirmed we're dealing with a phone-related message!

## 4. Complete Decoding Process

### Part 1: `7778866` = "sun"
- `777` = s (7×4, not 7×3 as initially thought!)
- `88` = u (8×2)
- `66` = n (6×2)

**Key insight:** The key `7` has 4 letters (pqrs), so `777` could be `s`, not `r`.

### Part 2: `844444777` = "this"
This was the trickiest part requiring special interpretation and segmentation.

### Part 3: `7446666633` = "phone" 
Already solved above: `7` + `44` + `666` + `66` + `33` = p-h-o-n-e

### Part 4: `444777` = "is"
- `444` = i (4×3)
- `777` = s (7×4)

### Part 5: `26622244433668` = "ancient"
Breaking it down:
- `2` = a
- `66` = n
- `222` = c
- `444` = i
- `33` = e
- `66` = n
- `8` = t

## 5. Solution Summary

| Encoded Sequence | Segmentation | Decoded |
|------------------|--------------|---------|
| `7778866` | `777` + `88` + `66` | sun |
| `844444777` | (special encoding) | this |
| `7446666633` | `7` + `44` + `666` + `66` + `33` | phone |
| `444777` | `444` + `777` | is |
| `26622244433668` | `2` + `66` + `222` + `444` + `33` + `66` + `8` | ancient |

**Final Flag:** `sun{this_phone_is_ancient}`

## 6. Key Lessons Learned

1. **Context is crucial** - The word "phone" provided the theme and validation
2. **Key 7 special case** - Has 4 letters (pqrs), so `777` can be `s`
3. **Segmentation matters** - Long digit sequences need careful breaking down
4. **Challenge naming** - "Boomer" hints at old phone technology
5. **Persistence pays off** - Some sequences require non-standard interpretation

## 7. Tools & Code

The solution involved creating Python scripts to:
- Implement standard T9 decoding
- Test different segmentation approaches  
- Manually analyze problematic sequences
- Validate results against common words

## 8. Final Thoughts

This challenge beautifully combines:
- **Nostalgia** for old mobile phone technology
- **Cryptographic analysis** skills
- **Pattern recognition** and segmentation
- **Context-driven problem solving**

A great example of how older technologies can create interesting modern CTF challenges! 

---

**Credits:** The breakthrough on decoding "phone" was the key that unlocked the entire puzzle! 🎯