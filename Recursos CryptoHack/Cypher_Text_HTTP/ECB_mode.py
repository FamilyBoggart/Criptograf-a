import requests
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

BASE_URL = "https://aes.cryptohack.org/ecb_oracle/"
PADDING_LENGTH = 16
DATA_SENT_OPTIONS = {"HEXSTRING" : 0, "BYTES" : 1, "BYTEARRAY" : 2}


def parse_data(data):
    if isinstance(data, str):
        return data.encode('utf-8').decode('unicode_escape').encode('latin1')
    elif isinstance(data, bytes):
        return data
    elif isinstance(data, int):
        length = (data.bit_length() + 7) // 8 or 1
        return data.to_bytes(length, byteorder = 'big')
    elif isinstance(data, bytearray):
        return bytes(data)
    else:
        raise TypeError(f"Tipo de dato no soportado : {type(data)}")

def bytes_to_hexstring(data):
    return data.hex().upper()
#plaintext = b'abcdefghiklm'
#flag = "1234"
#Cuando el cifrado es multiplo de 16 bytes, pad() añade un bloque completo de bytes \x10 para indicar donde ha finalizado el mensaje
#print(pad(plaintext+flag.encode(),16)) #b'abcdefghiklm1234\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'

def send_to_server(data, send_option):
    if(send_option == 0):
        r = requests.get(f"{BASE_URL}/encrypt/{data}/")
        response = r.json()
        ciphertext = response['ciphertext']
    return ciphertext

def check_match (possible_ct, ct):
    return possible_ct[:32] == ct[:32]  # Compara los primeros 32 caracteres (16 bytes) del ciphertext

def pad_iterate(data, data_format, ct):
    if data_format == 0:
        data = bytes.fromhex(data)
    for i in range(256):
        padded = data + parse_data(i)
        padded = bytes_to_hexstring(padded)
        possible_ct = send_to_server(padded,data_format)
        if check_match(possible_ct, ct):
            print(f"\33[92mCoincide el padding con el byte {i}\33[0m")
            return padded[-2:] # # Retorna el byte que se ha añadido
    print(f"\33[91mNo se encontró coincidencia\33[0m")
    return None

def byte_to_byte_attack(padding_length, key = None):
    flag_byte = ""
    aux_length = padding_length - 1
    while aux_length >= 0:
        byte_to_byte = "00" * (aux_length)
        print(f"Byte a enviar:\t{byte_to_byte}.\tLongitud:\t{len(byte_to_byte)}")
        ciphertext = send_to_server(byte_to_byte, DATA_SENT_OPTIONS["HEXSTRING"])
        print(f"Ciphertext:\t{ciphertext}\n")
        byte_to_byte += flag_byte
        flag_byte += pad_iterate(byte_to_byte, DATA_SENT_OPTIONS["HEXSTRING"], ciphertext)
        if flag_byte is None:
            print("Error: No se pudo encontrar el byte correspondiente.")
            return
        print(f"Byte encontrado:\t{bytes.fromhex(flag_byte)}")
        aux_length -= 1
    

byte_to_byte_attack(PADDING_LENGTH)

    