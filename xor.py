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

def unit_test():
	assert parse_data("Hola Mundo") == b'Hola Mundo' #String
	assert parse_data("\x48\x6f\x6c\x61\x20\x4d\x75\x6e\x64\x6f") == b'Hola Mundo' #Byte Strings
	assert parse_data("Hola\x20Mundo") == b'Hola Mundo' #Hibrido
	assert parse_data(7038329) == b'key' #Enteros
	
	cypher_text = "\x28\x31\x3f\x24\x00\x5b\x1a\x07\x34\x0c\x0a\x00\x00\x5b\x40\x2b\x0d\x09\x4d\x38\x2b\x5c\x11\x00\x0a\x0c\x17\x6c\x10\x6c\x11\x0d\x34\x0e\x17\x30\x03\x5d\x2c\x00\x58\x1d\x0d\x00\x40\x47\x07\x40\x08\x0e\x04"
	key = "key_t3st"
	assert encrypt_decrypt(cypher_text, key) == b'CTF{this_is_th3_fl4g_obtain3d_by_known_t3xt_4tt4ck}'
	print("Unit Test OK")


unit_test()



