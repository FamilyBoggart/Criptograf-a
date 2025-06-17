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

def count_legible_bytes(data):
    cont  = 0
    for b in data:
        if check_legible_byte(b):
            cont += 1
    print(f"Caracteres legibles: {cont}")
        
def iterate_bytes(data, size):
    for i in range(0, len(data), size):
        block = data[i:i + size]
        print(block)

""" Known text attack"""
def known_text_attack(cypher_text, flag_format = "CTF{"):
	i = 0
	plain_text = parse_data(flag_format)
	while len(plain_text) < len(cypher_text):
		result = encrypt_decrypt(cypher_text, flag_format)

		#1 Obtenemos la key que generaría el comienzo del flag
		byte_block = substr_bytes(result, 0, len(plain_text))
		
		#2 Iterar sobre la posible clave
		result = encrypt_decrypt(cypher_text, byte_block)
		
		#3 Comprobar si tenemos carácteres legibles justo despues de la flag, con el mismo tamaño que flag format
		j = 0
		while(check_legible_bytearray(substr_bytes(result,j,len(flag_format)))):
			print(j)
			j += len(plain_text)
			if j >= len(cypher_text):
				print(f"PLAINTEXT: {result}")
				return plain_text
		# 4. Añadir un caracter nulo
		plain_text += b'\x00'
	print("No encontrado")
	return result

def unit_test():
	test1 = xor_encrypt(b'Hola Mundo',b'key')
	test2 = xor_encrypt(b'Hola Mundo',b'KEY')
	assert test1 != test2

	assert parse_data("Hola Mundo") == b'Hola Mundo' #String
	assert parse_data("\x48\x6f\x6c\x61\x20\x4d\x75\x6e\x64\x6f") == b'Hola Mundo' #Byte Strings
	assert parse_data("Hola\x20Mundo") == b'Hola Mundo' #Hibrido
	assert parse_data(7038329) == b'key' #Enteros
	
	cypher_text = "\x28\x31\x3f\x24\x00\x5b\x1a\x07\x34\x0c\x0a\x00\x00\x5b\x40\x2b\x0d\x09\x4d\x38\x2b\x5c\x11\x00\x0a\x0c\x17\x6c\x10\x6c\x11\x0d\x34\x0e\x17\x30\x03\x5d\x2c\x00\x58\x1d\x0d\x00\x40\x47\x07\x40\x08\x0e\x04"
	key = "key_t3st"
	assert encrypt_decrypt(cypher_text, key) == b'CTF{this_is_th3_fl4g_obtain3d_by_known_t3xt_4tt4ck}'
	cypher_text = "\x08\x11\x1f\x24\x20\x5b\x3a\x27\x14\x2c\x2a\x00\x20\x5b\x60\x0b\x2d\x29\x6d\x38\x0b\x5c\x31\x20\x2a\x2c\x37\x6c\x30\x6c\x31\x2d\x14\x2e\x37\x30\x23\x5d\x0c\x20\x78\x3d\x2d\x00\x60\x47\x27\x60\x28\x2e\x24"

	assert add_null_byte(b'Hola') == b'Hola\x00'
	assert len(add_null_byte("Hola")) == 5

	assert check_legible_byte(b'\x20'[0]) == True #Bytes works as arrays and integeres as their indexed positions
	assert check_legible_byte(b'Hola'[2]) == True
	assert "Hola"[2] == 'l'
	assert b'Hola'[2] == 108

	assert substr_bytes(b'Hola Mundo',0,4) == b'Hola'
	assert substr_bytes(b'Hola Mundo',5,5) == b'Mundo'
	assert substr_bytes(b'Hola Mundo',5, 10) == b'Mundo'
	try:
		substr_bytes(b'Hola Mundo', 15, 3)
		assert False, "Se esperaba ValueError por índice fuera de rango"
	except ValueError as e:
		assert str(e) == "Out of Range"

	assert check_legible_bytearray(b'Hola Mundo') == True
	assert check_legible_bytearray(b'Hola\x1cMundo') == False

	#iterate_bytes test
	iterate_bytes(b'Esto es un texto de prueba', 5)
	
	#count_legible_bytes test
	cypher_text = "\x08\x11\x1f\x00\x60\x01\x28\x20\x23\x2c\x2a\x00\x3d\x40\x0c\x20\x23\x76\x06\x39\x38\x07\x34\x0b\x24\x27\x2d\x3e\x3d\x5d\x60\x30\x14\x27\x20\x00\x3f\x5d\x3c\x23\x25\x1a\x2d\x6c\x2c\x47\x0c\x60\x3f\x31\x6d\x3c\x3f\x4e"
	key = "CTF_42{"
	count_legible_bytes(parse_data(cypher_text))
	print(parse_data(parse_data(cypher_text)))

	print(known_text_attack(cypher_text, key))
	print("Unit Test OK")


unit_test()



