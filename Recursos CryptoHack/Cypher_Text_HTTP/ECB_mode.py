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

def send_to_server(data, send_option):
    if(send_option == 0):
        r = requests.get(f"{BASE_URL}/encrypt/{data}/")
        response = r.json()
        ciphertext = response['ciphertext']
    return ciphertext

# En el caso del ultimo byte, comparamos con el siguiente bloque de texto
def check_match (possible_ct, ct, block_number, last_byte):
    start = (block_number -1)* PADDING_LENGTH * 2; #De 32 en 32 bytes
    end = start + (PADDING_LENGTH * 2)
    if not last_byte:
        print(f"Comprobando texto:\t{ct[start:end]} con {possible_ct[start:end]}")
        return possible_ct[start:end] == ct[start:end]
    else:
        print(f"Comprobando texto:\t{ct[start+PADDING_LENGTH*2:end+PADDING_LENGTH*2]} con {possible_ct[start:end]}")
        return possible_ct[start:end] == ct[start+PADDING_LENGTH*2:end+PADDING_LENGTH*2]

def pad_iterate(data, data_format, ct, bn, last_byte = False):
    if data_format == 0:
        data = bytes.fromhex(data)
    for i in range(256):
        padded = data + parse_data(i)
        padded = bytes_to_hexstring(padded)
        possible_ct = send_to_server(padded,data_format)
        if check_match(possible_ct, ct, bn, last_byte):
            return padded[-2:] # # Retorna el byte que se ha añadido
    return None

def how_many_blocks(data, block_size):
    ciphertext = send_to_server(data, DATA_SENT_OPTIONS["HEXSTRING"])
    return len(ciphertext) // (block_size * 2)  # Cada byte se representa por 2 caracteres hexadecimales

def byte_to_byte_attack(padding_length, key = None):
    flag_byte = ""
    blocks = how_many_blocks("00" * padding_length, padding_length)  # Verifica el número de bloques
    for i in range(1, blocks + 1):
        aux_length = padding_length - 1
        while aux_length >= 0: 
            if aux_length == 0:
                byte_to_byte = "00" * (padding_length) # EL ultimo byte lo vamos a sacar desde el segundo bloque
            else:
                byte_to_byte = "00" * (aux_length)
            ciphertext = send_to_server(byte_to_byte, DATA_SENT_OPTIONS["HEXSTRING"])
            if aux_length == 0:
                byte_to_byte = flag_byte # El ultimo byte vamos a interar los bytes que ya hemos encontrado
                flag_byte += pad_iterate(byte_to_byte, DATA_SENT_OPTIONS["HEXSTRING"], ciphertext, i, True)
            else:
                byte_to_byte += flag_byte
                flag_byte += pad_iterate(byte_to_byte, DATA_SENT_OPTIONS["HEXSTRING"], ciphertext, i)
            if flag_byte is None:
                print("Error: No se pudo encontrar el byte correspondiente.")
                return
            print(f"Byte encontrado:\t{bytes.fromhex(flag_byte)}")
            aux_length -= 1
        
    

byte_to_byte_attack(PADDING_LENGTH)

def split_in_blocks(hash, block_size):
    return [hash[i:i + block_size] for i in range(0, len(hash), block_size)]
