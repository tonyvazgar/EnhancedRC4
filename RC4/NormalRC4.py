from time import time

class RC4(object):
    def ksa(self, key):
        # Create permutation
        S, T = [], []
        for i in range(0, 256):
            S.append(i)
            T.append(ord(key[i % len(key)]))

        j = 0
        for i in range(0, 256):
            j = (j + S[i] + T[i]) % 256
            S[i], S[j] = S[j], S[i]

        return S

    def prga(self, S, length):
        i, j = 0, 0
        keystream = []

        # Generate keystream
        for i in range(0, length):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            t = (S[i] + S[j]) % 256

            keystream.append((hex(S[t])[2:].zfill(2)))

        return keystream

    def encrypt(self, secret, key):
        cipher = []

        # Get keystream
        p = self.ksa(key)
        keystream = self.prga(p, len(secret))

        # print(keystream)

        # Secret to hex
        for s in list(secret):
            cipher.append(hex(ord(s))[2:])

        # Create ciphertext
        for i in range(len(cipher)):
            cipher[i] = xor(cipher[i], keystream[i])

        return list_to_string(cipher)

    def decrypt(self, cipher, key):
        message = []

        # Split message to hex per 2 character
        s = [cipher[i:i + 2] for i in range(0, len(cipher), 2)]

        # Get keystream
        p = self.ksa(key)
        keystream = self.prga(p, len(cipher))

        # XOR to get original message from ciphertext
        for i in range(len(s)):
            message.append(xor(s[i], keystream[i]))

        return list_to_string(message)



def xor(m, n):
    return hex(int(m, 16) ^ int(n, 16))[2:].zfill(2)

def list_to_string(l):
    return ''.join(str(x) for x in l)

def decode_from_hex(h):
    return bytearray.fromhex(h).decode()



def main():
    plaintext, key = 'meet me at the toga party', 'Llave'
    print("Text =", plaintext)
    print("Key  = ", key, "\n")

    rc4 = RC4()

    start_time = time()
    cipher = rc4.encrypt(plaintext, key)
    elapsed_time = time() - start_time
    print("Resultado = " , cipher)
    print("--->Tiempo en encriptar: [%0.10f] seconds.\n" % elapsed_time)

    start_time = time()
    message = decode_from_hex(rc4.decrypt(cipher, key))
    elapsed_time = time() - start_time
    print("Resultado = " , message)
    print("--->Tiempo en desencriptar: [%0.10f] seconds.\n" % elapsed_time)

    
main()