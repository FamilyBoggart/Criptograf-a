def cifrar_cesar(texto, desplazamiento):
    """
    Función para cifrar un texto usando el cifrado César con un desplazamiento específico.
    """
    resultado = ""
    
    # Iteramos cada carácter del texto
    for caracter in texto:
        # Si es una letra mayúscula
        if caracter.isupper():
            # Calculamos el nuevo carácter usando módulo 26 para rotar el alfabeto
            nuevo_caracter = chr((ord(caracter) - ord('A') + desplazamiento) % 26 + ord('A'))
            resultado += nuevo_caracter
        # Si es una letra minúscula
        elif caracter.islower():
            # Calculamos el nuevo carácter usando módulo 26 para rotar el alfabeto
            nuevo_caracter = chr((ord(caracter) - ord('a') + desplazamiento) % 26 + ord('a'))
            resultado += nuevo_caracter
        # Para caracteres especiales o espacios, los mantenemos sin cambios
        else:
            resultado += caracter
            
    return resultado

def show_caesar(texto):
    """
    Función para mostrar todas las combinaciones posibles del cifrado César.
    """
    print("\nTexto original:", texto)
    print("\nCombinaciones posibles:")
    
    # Mostramos todas las combinaciones de 0 a 26
    for i in range(26):
        texto_cifrado = cifrar_cesar(texto, i)
        print(f"\nDesplazamiento {i}:")
        print(texto_cifrado)

# Ejemplo de uso
texto_ejemplo = "Inserte Texto"
show_caesar(texto_ejemplo)

