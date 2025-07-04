import time

class Color:
	red = "\033[91m"
	green = "\033[92m"
	yellow = "\033[93m"
	blue = "\033[94m"
	purple = "\033[95m"
	cyan = "\033[96m"
	white = "\033[97m"
	end = "\033[0m"



def rainbow():
	colored = [Color.red, Color.green, Color.yellow, Color.blue, Color.purple, Color.cyan, Color.white]
	i = 0
	while True:
		if i == 7:
			i = 0
		print(colored[i] + "Hello World!" + Color.end)
		i += 1
		time.sleep(0.1)

#Parsing Tools
""" Parsing  4x4 matrix from/to  16-Bytes Array"""
def bytes2matrix(text):
    """ Converts a 16-byte array into a 4x4 matrix.  """
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]

def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    return bytes([matrix[row][col] for row in range(4) for col in range(4)])

#Basic Encriptings

#XOR
def xor_encrypt(data: bytes, key: bytes) -> bytes:
    key = (key * (len(data) // len(key) + 1))[:len(data)]  # Repite la clave para igualar la longitud
    return bytes([b ^ k for b, k in zip(data, key)])

#Cesar
