from pyfinite import ffield

F = ffield.FField(8, gen=0x11b, useLUT=0)

def affine_transform(byte):
    c = 0x63
    result = 0
    for i in range(8):
        bit = (
            ((byte >> i) & 1) ^
            ((byte >> ((i + 4) % 8)) & 1) ^
            ((byte >> ((i + 5) % 8)) & 1) ^
            ((byte >> ((i + 6) % 8)) & 1) ^
            ((byte >> ((i + 7) % 8)) & 1) ^
            ((c >> i) & 1)
        )
        result |= (bit << i)
    return result

def aes_sbox(byte):
    if byte == 0:
        inv = 0
    else:
        inv = F.Inverse(byte)
    return affine_transform(inv)

print(hex(aes_sbox(0xA5)))  # Output: 0x6
