#!/usr/bin/env python3

def hex_to_bytes(hex_string):
    """Convert hex string to bytes"""
    return bytes.fromhex(hex_string)

def bytes_to_hex(byte_data):
    """Convert bytes to hex string"""
    return byte_data.hex()

def xor_bytes(a, b):
    """XOR two byte sequences"""
    return bytes(x ^ y for x, y in zip(a, b))

def is_printable_ascii(byte_val):
    """Check if a byte value is printable ASCII"""
    return 32 <= byte_val <= 126

def is_letter(byte_val):
    """Check if a byte value is a letter"""
    return (65 <= byte_val <= 90) or (97 <= byte_val <= 122)

def analyze_xor_with_space(ciphertexts):
    """
    When space (0x20) is XORed with a letter, it flips the case.
    This helps us identify positions where one plaintext has space and another has a letter.
    """
    results = []
    
    for i, ct1 in enumerate(ciphertexts):
        for j, ct2 in enumerate(ciphertexts):
            if i >= j:
                continue
                
            xored = xor_bytes(ct1, ct2)
            analysis = []
            
            for k, byte_val in enumerate(xored):
                # If XOR result is letter, one of the original chars was likely space
                if is_letter(byte_val):
                    analysis.append((k, byte_val, chr(byte_val)))
            
            if analysis:
                results.append((i, j, analysis))
    
    return results

def solve_stream_cipher():
    # Given ciphertexts
    ciphertexts_hex = [
        "315c4eeaa8b5f8aaf9174145bf43e1784b8fa00dc71d885a804e5ee9fa40b16349c146fb778cdf2d3aff021dfff5b403b510d0d0455468aeb98622b137dae857553ccd8883a7bc37520e06e515d22c954eba5025b8cc57ee59418ce7dc6bc41556bdb36bbca3e8774301fbcaa3b83b220809560987815f65286764703de0f3d524400a19b159610b11ef3e",
        "234c02ecbbfbafa3ed18510abd11fa724fcda2018a1a8342cf064bbde548b12b07df44ba7191d9606ef4081ffde5ad46a5069d9f7f543bedb9c861bf29c7e205132eda9382b0bc2c5c4b45f919cf3a9f1cb74151f6d551f4480c82b2cb24cc5b028aa76eb7b4ab24171ab3cdadb8356f",
        "32510ba9a7b2bba9b8005d43a304b5714cc0bb0c8a34884dd91304b8ad40b62b07df44ba6e9d8a2368e51d04e0e7b207b70b9b8261112bacb6c866a232dfe257527dc29398f5f3251a0d47e503c66e935de81230b59b7afb5f41afa8d661cb",
        "32510ba9aab2a8a4fd06414fb517b5605cc0aa0dc91a8908c2064ba8ad5ea06a029056f47a8ad3306ef5021eafe1ac01a81197847a5c68a1b78769a37bc8f4575432c198ccb4ef63590256e305cd3a9544ee4160ead45aef520489e7da7d835402bca670bda8eb775200b8dabbba246b130f040d8ec6447e2c767f3d30ed81ea2e4c1404e1315a1010e7229be6636aaa",
        "3f561ba9adb4b6ebec54424ba317b564418fac0dd35f8c08d31a1fe9e24fe56808c213f17c81d9607cee021dafe1e001b21ade877a5e68bea88d61b93ac5ee0d562e8e9582f5ef375f0a4ae20ed86e935de81230b59b73fb4302cd95d770c65b40aaa065f2a5e33a5a0bb5dcaba43722130f042f8ec85b7c2070",
        "32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd2061bbde24eb76a19d84aba34d8de287be84d07e7e9a30ee714979c7e1123a8bd9822a33ecaf512472e8e8f8db3f9635c1949e640c621854eba0d79eccf52ff111284b4cc61d11902aebc66f2b2e436434eacc0aba938220b084800c2ca4e693522643573b2c4ce35050b0cf774201f0fe52ac9f26d71b6cf61a711cc229f77ace7aa88a2f19983122b11be87a59c355d25f8e4",
        "32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd90f1fa6ea5ba47b01c909ba7696cf606ef40c04afe1ac0aa8148dd066592ded9f8774b529c7ea125d298e8883f5e9305f4b44f915cb2bd05af51373fd9b4af511039fa2d96f83414aaaf261bda2e97b170fb5cce2a53e675c154c0d9681596934777e2275b381ce2e40582afe67650b13e72287ff2270abcf73bb028932836fbdecfecee0a3b894473c1bbeb6b4913a536ce4f9b13f1efff71ea313c8661dd9a4ce",
        "315c4eeaa8b5f8bffd11155ea506b56041c6a00c8a08854dd21a4bbde54ce56801d943ba708b8a3574f40c00fff9e00fa1439fd0654327a3bfc860b92f89ee04132ecb9298f5fd2d5e4b45e40ecc3b9d59e9417df7c95bba410e9aa2ca24c5474da2f276baa3ac325918b2daada43d6712150441c2e04f6565517f317da9d3",
        "271946f9bbb2aeadec111841a81abc300ecaa01bd8069d5cc91005e9fe4aad6e04d513e96d99de2569bc5e50eeeca709b50a8a987f4264edb6896fb537d0a716132ddc938fb0f836480e06ed0fcd6e9759f40462f9cf57f4564186a2c1778f1543efa270bda5e933421cbe88a4a52222190f471e9bd15f652b653b7071aec59a2705081ffe72651d08f822c9ed6d76e48b63ab15d0208573a7eef027",
        "466d06ece998b7a2fb1d464fed2ced7641ddaa3cc31c9941cf110abbf409ed39598005b3399ccfafb61d0315fca0a314be138a9f32503bedac8067f03adbf3575c3b8edc9ba7f537530541ab0f9f3cd04ff50d66f1d559ba520e89a2cb2a83",
    ]
    
    # Target ciphertext to decrypt
    target_hex = "32510ba9babebbbefd001547a810e67149caee11d945cd7fc81a05e9f85aac650e9052ba6a8cd8257bf14d13e6f0a803b54fde9e77472dbff89d71b57bddef121336cb85ccb8f3315f4b52e301d16e9f52f904"
    
    # Convert to bytes
    ciphertexts = [hex_to_bytes(ct) for ct in ciphertexts_hex]
    target = hex_to_bytes(target_hex)
    
    print("Analyzing ciphertexts...")
    print(f"Number of ciphertexts: {len(ciphertexts)}")
    print(f"Target length: {len(target)} bytes")
    
    # Find the minimum length to work with
    min_len = min(len(ct) for ct in ciphertexts + [target])
    print(f"Working with {min_len} bytes")
    
    # Truncate all ciphertexts to minimum length
    ciphertexts = [ct[:min_len] for ct in ciphertexts]
    target = target[:min_len]
    
    # Try to recover the key by analyzing XOR patterns
    possible_key = [None] * min_len
    
    # For each position, try to determine the key byte
    for pos in range(min_len):
        # Collect all ciphertext bytes at this position
        ct_bytes = [ct[pos] for ct in ciphertexts]
        target_byte = target[pos]
        
        # Try different assumptions about spaces in the plaintexts
        for space_assumption in range(len(ciphertexts)):
            # Assume ciphertext[space_assumption] has a space at position pos
            assumed_key_byte = ct_bytes[space_assumption] ^ ord(' ')
            
            # Check if this key byte makes sense for other ciphertexts
            valid = True
            decoded_chars = []
            
            for i, ct_byte in enumerate(ct_bytes):
                decoded_char = ct_byte ^ assumed_key_byte
                if not is_printable_ascii(decoded_char):
                    valid = False
                    break
                decoded_chars.append(chr(decoded_char))
            
            if valid:
                # Also check target
                target_char = target_byte ^ assumed_key_byte
                if is_printable_ascii(target_char):
                    possible_key[pos] = assumed_key_byte
                    print(f"Position {pos}: key=0x{assumed_key_byte:02x}, target_char='{chr(target_char)}'")
                    break
    
    # Try to decode the target with recovered key
    result = []
    for i, byte_val in enumerate(target):
        if i < len(possible_key) and possible_key[i] is not None:
            decoded = byte_val ^ possible_key[i]
            if is_printable_ascii(decoded):
                result.append(chr(decoded))
            else:
                result.append('?')
        else:
            result.append('?')
    
    decoded_message = ''.join(result)
    print(f"\nDecoded target message: '{decoded_message}'")
    
    # Try alternative approach: use frequency analysis and common patterns
    print("\nTrying alternative approach...")
    
    # Use more sophisticated key recovery
    recovered_key = recover_key_advanced(ciphertexts, target)
    
    if recovered_key:
        final_message = ''.join(chr(b ^ k) for b, k in zip(target, recovered_key) if k is not None)
        print(f"Final decoded message: '{final_message}'")
        return final_message.strip()
    
    return decoded_message.strip()

def recover_key_advanced(ciphertexts, target):
    """Advanced key recovery using multiple techniques"""
    min_len = min(len(ct) for ct in ciphertexts + [target])
    possible_key = [None] * min_len
    
    # Method 1: Space character analysis
    for pos in range(min_len):
        candidates = []
        
        # For each ciphertext, assume it has a space at this position
        for i, ct in enumerate(ciphertexts):
            key_candidate = ct[pos] ^ ord(' ')
            
            # Test this key candidate against all ciphertexts
            valid_count = 0
            for j, ct2 in enumerate(ciphertexts):
                if j == i:
                    continue
                decoded = ct2[pos] ^ key_candidate
                if is_printable_ascii(decoded):
                    valid_count += 1
            
            # Also test against target
            target_decoded = target[pos] ^ key_candidate
            if is_printable_ascii(target_decoded):
                valid_count += 1
            
            candidates.append((key_candidate, valid_count, target_decoded))
        
        # Choose the candidate with highest valid count
        if candidates:
            best_candidate = max(candidates, key=lambda x: x[1])
            if best_candidate[1] > len(ciphertexts) // 2:  # Threshold
                possible_key[pos] = best_candidate[0]
    
    # Method 2: Common English patterns
    common_words = [b'the ', b'and ', b'that', b'have', b'for ', b'not ', b'with', b'you ', b'this', b'but ', b'his ', b'from']
    
    for word in common_words:
        for ct in ciphertexts:
            for start_pos in range(len(ct) - len(word) + 1):
                # Try this word at this position
                for i, char in enumerate(word):
                    pos = start_pos + i
                    if pos < len(possible_key):
                        key_byte = ct[pos] ^ char
                        
                        # Verify this key byte works for other ciphertexts
                        if verify_key_byte(key_byte, pos, ciphertexts + [target]):
                            possible_key[pos] = key_byte
    
    return possible_key

def verify_key_byte(key_byte, position, ciphertexts):
    """Verify if a key byte at a position produces reasonable results"""
    valid_count = 0
    for ct in ciphertexts:
        if position < len(ct):
            decoded = ct[position] ^ key_byte
            if is_printable_ascii(decoded):
                valid_count += 1
    
    return valid_count >= len(ciphertexts) * 0.8  # 80% threshold

if __name__ == "__main__":
    message = solve_stream_cipher()
    print(f"\n=== FINAL ANSWER ===")
    print(f"Secret message: {message}")