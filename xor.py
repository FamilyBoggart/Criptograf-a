# METHODS TESTED
def xor_encrypt(data: bytes, key: bytes) -> bytes:
    key = (key * (len(data) // len(key) + 1))[:len(data)]  # Repite la clave para igualar la longitud
    return bytes([b ^ k for b, k in zip(data, key)])

def parse_data(data):
    if isinstance(data, str):
        return data.encode('utf-8').decode('unicode_escape').encode('latin1')
    elif isinstance(data, bytes):
        return data
    elif isinstance(data, int):
        length = (data.bit_length() + 7) // 8 or 1
        return data.to_bytes(length, byteorder = 'big')
    else:
        raise TypeError(f"Tipo de dato no soportado : {type(data)}")

def encrypt_decrypt(cypher_text, key, plaintext = None):
	cypher_text = parse_data(cypher_text)
	key = parse_data(key)
	result = xor_encrypt(cypher_text, key)
	return result

def add_null_byte(data):
    data=parse_data(data)
    return data + b'\x00'

def check_legible_byte(data : int):
    return 32 <= data <= 126

def substr_bytes(data, start, size):
    if not (0 <= start <= len(data)):
        raise ValueError("Out of Range")
    return data[start:start + size]

def check_legible_bytearray(data):
    for b in data:
        if not check_legible_byte(b):
            return False
    return True
#UNTESTED
""" Known text attack"""
#1. We need to know at least a fragment of plain text, in CTFs it's usual to know how the flag format is, such as CTF{}
# It will be manadatory to guess the key and the plaintext
def known_text_attack(cypher_text, flag_format = "CTF{"):
    plain_text = flag_format
    result = encrypt_decrypt(cypher_text, flag_format)
    
    
    
    print(result)
    return result

def unit_test():
	assert parse_data("Hola Mundo") == b'Hola Mundo' #String
	assert parse_data("\x48\x6f\x6c\x61\x20\x4d\x75\x6e\x64\x6f") == b'Hola Mundo' #Byte Strings
	assert parse_data("Hola\x20Mundo") == b'Hola Mundo' #Hibrido
	assert parse_data(7038329) == b'key' #Enteros
	
	cypher_text = "\x28\x31\x3f\x24\x00\x5b\x1a\x07\x34\x0c\x0a\x00\x00\x5b\x40\x2b\x0d\x09\x4d\x38\x2b\x5c\x11\x00\x0a\x0c\x17\x6c\x10\x6c\x11\x0d\x34\x0e\x17\x30\x03\x5d\x2c\x00\x58\x1d\x0d\x00\x40\x47\x07\x40\x08\x0e\x04"
	key = "key_t3st"
	assert encrypt_decrypt(cypher_text, key) == b'CTF{this_is_th3_fl4g_obtain3d_by_known_t3xt_4tt4ck}'

	assert add_null_byte(b'Hola') == b'Hola\x00'
	assert len(add_null_byte("Hola")) == 5

	assert check_legible_byte(b'\x20'[0]) == True #Bytes works as arrays and integeres as their indexed positions
	assert check_legible_byte(b'Hola'[2]) == True
	assert "Hola"[2] == 'l'
	assert b'Hola'[2] == 108

	assert substr_bytes(b'Hola Mundo',0,4) == b'Hola'
	assert substr_bytes(b'Hola Mundo',5,5) == b'Mundo'
	try:
		substr_bytes(b'Hola Mundo', 15, 3)
		assert False, "Se esperaba ValueError por índice fuera de rango"
	except ValueError as e:
		assert str(e) == "Out of Range"

	assert check_legible_bytearray(b'Hola Mundo') == True
	assert check_legible_bytearray(b'Hola\x1cMundo') == False
	cypher_text = "\x28\x31\x3f\x24\x00\x5b\x1a\x07\x34\x0c\x0a\x00\x00\x5b\x40\x2b\x0d\x09\x4d\x38\x2b\x5c\x11\x00\x0a\x0c\x17\x6c\x10\x6c\x11\x0d\x34\x0e\x17\x30\x03\x5d\x2c\x00\x58\x1d\x0d\x00\x40\x47\x07\x40\x08\x0e\x04"
	key = "key_t3st"
	#known_text_attack(cypher_text)
	print("Unit Test OK")


unit_test()



