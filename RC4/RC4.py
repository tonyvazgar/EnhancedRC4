from random import sample

N = 256
half_n = round(N / 2)

""" Key-Scheduling Algorithm
    Recibe las dos llaves para hacer permutaciones """
def KSA(key1, key2):
    # Generar ambas S-Boxes
    # S1 va de 0 hasta N / 2.
    # S2 va de N / 2 hasta N.
    s1 = [i for i in range(half_n)]
    s2 = [i for i in range(half_n, N)]

    # Generación y permutacion de ambas S-Boxes.
    j = 0
    for i in range(half_n):
        j = (j + s1[i] + key1[i % len(key1)]) % half_n
        s1[i], s1[j] = s1[j], s1[i]  # Swap

    for i in range(half_n):
        j = (j + s2[i] + key2[i % len(key2)]) % half_n
        s2[i], s2[j] = s2[j], s2[i]  # Swap

    return [s1, s2]


""" Pseudo Random Number Generation Algorithm
    Recibe las dos s-boxes y el plaintext 
    para hacer operaciones sobre la longitud del 
    plaintext """
def PRGA(s1, s2, PT):
    # Inicializacion de los componentes en 0
    # y tomar la longitud del plain text
    i = 0
    x = 0
    j1 = 0
    j2 = 0
    key_stream = []
    size_pt = len(PT)

    while i < size_pt:
        j1 = (j1 + s1[i + 1]) % half_n
        # Hacer swap entre s-box 1 y s-box 2
        s1[i], s2[j1] = s2[j1], s1[i]

        # Generar t1 y t2 de acuerdo al algoritmo
        t1 = s1[(s1[i] + s1[j1]) % (half_n)] + 1

        j2 = (j2 + s2[i]) % (half_n)

        # Hacer swap entre s-box 1 y s-box 2
        s2[i], s1[j2] = s1[j2], s2[i]

        t2 = s2[(s2[i] + s2[j2]) % (half_n)] + 1

        # Insertar al arreglo key_stream un XOR entre t1 y t2
        key_stream.insert(x, (t1 ^ t2) % N)

        # Aumentar i con modulo half_n
        i = (i + 1) % half_n

    return key_stream


""" Rivest Code 4
    Recibe la llave, el tamaño la llave y el plaintext """
def RC4(key, k, pt):
    # s_boxes contiene las dos S-Boxes.
    s_boxes = KSA(key[:k//2], key[k//2:])
    s_one = s_boxes[0]
    s_two = s_boxes[1]

    key_stream = PRGA(s_one, s_two, pt)

    return "".join(map(lambda x, y: chr(ord(x) ^ y), pt, key_stream)), key_stream


def showStatus(process, plain_text, key, key_stream, crypt):
    print(process)
    print("Text =", plain_text)
    print("Key =", key)
    print("Key Stream =", key_stream)
    print("Resultado ==", crypt)


def main():
    text = "texto plano"
    K = "Llave"
    k = 4
    secret_key = list(map(lambda x: ord(x), sample(K, k)))
    # Sample obtiene k numeros al azar de la N = 256
    initial_vector = sample(range(N), k)
    key = secret_key + initial_vector    # Definicion de las llaves

    encrypt, key_stream = RC4(key, k, text)  # Encriptado
    showStatus("Encryption", text, key, key_stream, encrypt)  # Proceso encripcion

    decrypt, key_stream = RC4(key, k, encrypt)  # Desencriptado
    showStatus("Decryption", encrypt, key, key_stream, decrypt)  # Proceso desencriptado


main()
