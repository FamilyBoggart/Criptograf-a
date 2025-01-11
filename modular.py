from utils import *


def check_function():
	correct = input("¿Es correcto? (Y/N)")
	if correct == 'Y' or correct == 'y':
		return 1
	else:
		correct = input("¿Volver a intentar? (Y/N)")
		if correct == 'Y' or correct == 'y':
			return 2
	return 0

def basic_mod_ecuation_solve_x(a=0,m=0):
	check = 2
	while check != 0:
		print("Para A = x mod m")
		if a == 0:
			a = int(input("introduce A"))
		if m == 0:
			m = int(input("introduce m"))
		print(a," = x mod",m)
		check = check_function()
		if check == 1:
			return(a % m)
	return None

def fermat_theorem_demonstration():
	print(Color.yellow,"Para demostrar el Pequeño Teorema de Fermat, se necesita que m sea un número primo y que a sea un número entero positivo",Color.end)
	a = int(input("Introduce a: "))
	m = int(input("Introduce m: "))
	print("\na^(m-1) = 1 mod m\n")
	print(Color.cyan,a,"^",m-1," = 1 mod ",m,Color.end)
	print(Color.green,a,"^",m-1," = ",a**(m-1),Color.end)
	print(Color.green,a**(m-1),"% ",m," = ",a**(m-1) % m,Color.end)
	if a**(m-1) % m == 1:
		print(Color.green,"El Pequeño Teorema de Fermat se cumple",Color.end)
	else:
		print(Color.red,"El Pequeño Teorema de Fermat no se cumple. m no es primo",Color.end)

def menu():
	print(Color.red+"0)"+Color.white+" Salir"+Color.end)
	print(Color.red+"1)"+Color.white+" A = x mod m. Resolver x"+Color.end)
	print(Color.red+"2)"+Color.white+" Pequeño Teorema de Fermat. Demostración"+Color.end)

menu()
opt = int(input("Elige tu opcion: "))
if opt == 0:
	exit()
if opt == 1:
	x = basic_mod_ecuation_solve_x()
	print("La solucion sería: ",x)
elif opt == 2:
	fermat_theorem_demonstration()
if opt == 3007:
	rainbow()