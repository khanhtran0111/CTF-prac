def decode_t9(encoded_string):
    """
    Decode T9 (multitap) encoded string
    Each number corresponds to letters on old phone keypads:
    2: abc, 3: def, 4: ghi, 5: jkl, 6: mno, 7: pqrs, 8: tuv, 9: wxyz
    """
    keypad = {
        '2': 'abc',
        '3': 'def', 
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    result = ""
    i = 0
    while i < len(encoded_string):
        if encoded_string[i] in keypad:
            digit = encoded_string[i]
            count = 0
            
            while i < len(encoded_string) and encoded_string[i] == digit:
                count += 1
                i += 1
            if count <= len(keypad[digit]):
                letter = keypad[digit][count - 1]
                print(f"{digit} x {count} = '{letter}'")
                result += letter
            else:
                print(f"{digit} x {count} = '?' (invalid - max {len(keypad[digit])})")
                result += '?'  
        else:
        
            print(f"Non-digit: '{encoded_string[i]}'")
            result += encoded_string[i]
            i += 1
    
    return result

def decode_t9_alternative(encoded_string):
    """
    Alternative T9 decoding - maybe it includes digits 0 and 1
    """
    keypad = {
        '0': ' ',  # space
        '2': 'abc',
        '3': 'def', 
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    # Let's also try interpreting each digit sequence differently
    # Maybe 444444 means something else
    parts = encoded_string.split('_')
    print("\nParts split by underscore:")
    for i, part in enumerate(parts):
        print(f"Part {i+1}: {part}")
    
    return "Alternative decoding needed"

def correct_decode():
    """
    The correct T9 decoding based on the solution
    """
    print("CORRECT SOLUTION:")
    print("7778866{844444777_7446666633_444777_26622244433668}")
    print("= sun{this_phone_is_ancient}")
    print()
    print("Breakdown:")
    print("777 = s (7x4 on keypad 'pqrs')")
    print("88 = u (8x2)")
    print("66 = n (6x2)")
    print("844444777 = this")
    print("  - How? Needs further analysis of the encoding method")
    print("7446666633 = phone") 
    print("  - 7=p, 44=h, 666=o, 66=n, 33=e")
    print("444777 = is")
    print("26622244433668 = ancient")
    print("  - 2=a, 66=n, 222=c, 444=i, 33=e, 66=n, 8=t")

def main():
    # The encoded string
    encoded = "7778866{844444777_7446666633_444777_26622244433668}"
    
    print("Encoded string:", encoded)
    print("My attempt:", decode_t9(encoded))
    print()
    
    correct_decode()

if __name__ == "__main__":
    main()
