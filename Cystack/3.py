import hashlib
import string
import itertools
from datetime import datetime

target = "f33e7acc20580138923e9e07f3f02536"

def md5_hex(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()

def try_case_combinations(base_word):
    for i in range(2 ** len(base_word)):
        variant = ""
        for j, char in enumerate(base_word):
            if char.isalpha():
                if i & (1 << j):
                    variant += char.upper()
                else:
                    variant += char.lower()
            else:
                variant += char
        
        if md5_hex(variant) == target:
            return variant
    return None

def brute_force(charset, length):
    total = len(charset) ** length
    print(f"Total combinations: {total:,}")
    
    count = 0
    start_time = datetime.now()
    
    for combo in itertools.product(charset, repeat=length):
        password = ''.join(combo)
        count += 1
        
        if md5_hex(password) == target:
            return password, count
        
        if count % 100000 == 0:
            elapsed = (datetime.now() - start_time).total_seconds()
            rate = count / elapsed if elapsed > 0 else 0
            print(f"  Checked: {count:,} | Rate: {rate:,.0f}/sec | Current: {password}")
    
    return None, count

print("="*70)
print("MD5 HASH CRACKER - COMPREHENSIVE ATTACK")
print("="*70)
print(f"Target Hash: {target}")
print(f"Password Length: 7 characters")
print(f"Started at: {datetime.now().strftime('%H:%M:%S')}\n")

print("[STRATEGY 1] Dictionary Attack with Case Variations")
print("-"*70)

wordlist = [
    "welcome", "default", "password"[:7], "passw0rd", "passwrd", "passwd",
    "admin12", "admin", "user123", "letmein", "monkey", "dragon",
    "master", "abc123", "qwerty", "shadow", "ashley", "bailey",
    "charlie", "diamond", "flower", "freedom", "ginger", "hannah",
    "jackson", "jordan", "killer", "lauren", "london", "maggie",
    "maxwell", "michael", "nicole", "oliver", "pepper", "princess"[:7],
    "robert", "samantha"[:7], "steven", "summer", "thomas", "william",
    "yourpwd", "YourPwd", "hacked", "pwned", "flag123", "ctf2024",
    "root123", "test123", "demo123", "cystack",
    "abc1234"[:7], "qwe123", "asd123", "zxc123", "pass123",
    "admin1", "user1", "test1", "demo1",
]

for word in wordlist:
    if len(word) == 7:
        print(f"Trying '{word}'...", end=" ")
        result = try_case_combinations(word)
        if result:
            print(f"\n\n{'='*70}")
            print("PASSWORD FOUND!")
            print(f"{'='*70}")
            print(f"Password: '{result}'")
            print(f"MD5 Hash: {md5_hex(result)}")
            print(f"Strategy: Dictionary with case variations")
            print(f"Base word: '{word}'")
            print(f"{'='*70}")
            exit()
        print("X")

print("\n[STRATEGY 2] Common Patterns")
print("-"*70)

common_words = ["admin", "user", "test", "pass", "root", "demo"]
for word in common_words:
    for digit in "0123456789":
        pattern = (word + digit)[:7]
        if len(pattern) == 7:
            result = try_case_combinations(pattern)
            if result:
                print(f"\nFound: '{result}'")
                exit()

print("Patterns checked X\n")

print("[STRATEGY 3] Brute Force Attack")
print("-"*70)

strategies = [
    ("Lowercase only", string.ascii_lowercase, "Fast"),
    ("Uppercase only", string.ascii_uppercase, "Fast"),
    ("Lowercase + digits", string.ascii_lowercase + string.digits, "Medium"),
    ("Uppercase + digits", string.ascii_uppercase + string.digits, "Medium"),
    ("Letters only (mixed case)", string.ascii_letters, "Slow - 8 billion combinations"),
    ("Alphanumeric", string.ascii_letters + string.digits, "Very slow - 3.5 trillion combinations"),
]

for name, charset, speed in strategies:
    total = len(charset) ** 7
    print(f"\n{name} ({len(charset)} chars) - {speed}")
    print(f"Combinations: {total:,}")
    
    if total > 10_000_000:
        choice = input("This will take a LONG time. Continue? (y/n): ")
        if choice.lower() != 'y':
            print("Skipped.")
            continue
    
    print("Starting brute force...")
    result, count = brute_force(charset, 7)
    
    if result:
        print(f"\n{'='*70}")
        print("PASSWORD FOUND!")
        print(f"{'='*70}")
        print(f"Password: '{result}'")
        print(f"MD5 Hash: {md5_hex(result)}")
        print(f"Strategy: Brute force ({name})")
        print(f"Attempts: {count:,}")
        print(f"{'='*70}")
        exit()
    else:
        print(f"Not found after {count:,} attempts.\n")

print("\n" + "="*70)
print("Password not found with available strategies.")
print("Consider using professional tools like hashcat or john the ripper.")
print("="*70)
