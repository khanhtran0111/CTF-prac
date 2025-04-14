segment_map = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3,
    'E': 4, 'F': 5, 'G': 6, 'H': 7,
    'I': 8, 'J': 9, 'K': 10, 'L': 11,
    'M': 12, 'N': 13
}

char_to_segments = {
    'Z': ['A', 'L', 'M', 'D'],
    'I': ['A', 'I', 'J', 'D'],
}

def encode_character(ch):
    """Trả về chuỗi bit biểu diễn ký tự được mã hoá"""
    bits = [0] * 14
    segments = char_to_segments.get(ch.upper(), [])
    for seg in segments:
        bit_index = segment_map[seg]
        bits[13 - bit_index] = 1 
    return ''.join(map(str, bits))

def encode_string(s):
    """Mã hoá cả chuỗi thành danh sách các chuỗi bit"""
    return [encode_character(ch) for ch in s]

input_str = "ZI"
encoded = encode_string(input_str)

for ch, code in zip(input_str, encoded):
    print(f"{ch} => {code}")
