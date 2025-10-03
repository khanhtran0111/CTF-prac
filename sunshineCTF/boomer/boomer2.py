def decode_t9_smart(encoded_string):
    """
    Smart T9 decoder that tries to handle longer sequences
    by breaking them down intelligently
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
    
    def decode_sequence(seq):
        """Try to decode a sequence of same digits"""
        if not seq or seq[0] not in keypad:
            return seq
            
        digit = seq[0]
        length = len(seq)
        letters = keypad[digit]
        
        # If length is within valid range, decode normally
        if length <= len(letters):
            return letters[length - 1]
        
        # If too long, try to break it down
        # For example: 44444 could be 444 + 4 + 4 = i + g + g
        # Or it could be 444 + 44 = i + g  
        result = ""
        remaining = length
        
        # Try to use maximum valid sequences first
        while remaining > 0:
            if remaining >= len(letters):
                result += letters[-1]  # Last letter (maximum presses)
                remaining -= len(letters)
            else:
                result += letters[remaining - 1]
                remaining = 0
                
        return result
    
    result = ""
    i = 0
    
    print("Smart decoding:")
    
    while i < len(encoded_string):
        if encoded_string[i] in keypad:
            # Count consecutive occurrences of the same digit
            digit = encoded_string[i]
            count = 0
            
            while i < len(encoded_string) and encoded_string[i] == digit:
                count += 1
                i += 1
            
            decoded = decode_sequence(digit * count)
            print(f"{digit} x {count} = '{decoded}'")
            result += decoded
        else:
            # Non-digit characters (like brackets, underscores) are kept as is
            print(f"Non-digit: '{encoded_string[i]}'")
            result += encoded_string[i]
            i += 1
    
    return result

def decode_t9_manual():
    """Manual decoding based on analysis"""
    # Let's manually decode each part:
    # 777 88 66 { 8 44444 777 _ 744 666666 33 _ 444 777 _ 2 66 222 444 33 66 8 }
    
    parts = {
        '777': 'r',      # 7x3 = r
        '88': 'u',       # 8x2 = u  
        '66': 'n',       # 6x2 = n
        '8': 't',        # 8x1 = t
        '44444': '?',    # Need to figure this out
        '777': 'r',      # 7x3 = r
        '744': '?',      # 7x1 + 4x2 = p + h?
        '666666': '?',   # 6x6 = ?
        '33': 'e',       # 3x2 = e
        '444': 'i',      # 4x3 = i
        '777': 'r',      # 7x3 = r
        '2': 'a',        # 2x1 = a
        '66': 'n',       # 6x2 = n
        '222': 'c',      # 2x3 = c
        '444': 'i',      # 4x3 = i
        '33': 'e',       # 3x2 = e
        '66': 'n',       # 6x2 = n
        '8': 't'         # 8x1 = t
    }
    
    # For 44444 (4x5), since 4 maps to 'ghi' (max 3), maybe it's 444+4+4 = i+g+g?
    # Or maybe 4444+4 = ? + g (but 4x4 is still invalid)
    # Let's try: 444+44 = i + g
    print("\nManual decoding attempt:")
    print("44444 could be 444+44 = i+g = 'ig'")
    print("666666 could be 666+666 = o+o = 'oo'") 
    print("Or maybe 666666 = 666+66+6 = o+n+m")
    
    return "Manual analysis needed"

def main():
    encoded = "7778866{844444777_7446666633_444777_26622244433668}"
    
    print("Original:", encoded)
    print("\nSmart decoded:", decode_t9_smart(encoded))
    
    decode_t9_manual()

if __name__ == "__main__":
    main()