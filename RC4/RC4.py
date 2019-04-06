N = 256
half_n = round(N / 2)

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

def PRGA(s1, s2, PT):
    i = 0
    x = 0
    j1 = 0
    j2 = 0
    size_pt = len(PT)

    while i < size_pt:
        i = ((i + 1) % half_n)
        j1 = ((j1 + s1[i + 1]) % half_n)
        # HACER SWAP ENTRE S1 y S2



def main():
    # s_boxes contiene las dos S-Boxes.
    s_boxes = KSA([2, 5], [2, 5])
    print(s_boxes)
    s_box_one = s_boxes[0]
    s_box_two = s_boxes[1]
    # print(s_box_one)
    # print(s_box_two)

    PRGA(s_box_one, s_box_two, "HI")


main()
