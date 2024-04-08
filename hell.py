class ADFGVX:
    def __init__(self, key, transpose_key):
        self.polybius_row = "CRYPTO"
        self.polybius_col = "GRAPHY"
        self.transpose_key = transpose_key
        self.key = key
        self.polybius = self.fill_polybius()

    def fill_polybius(self):
        polybius = {}
        key_index = 0
        for row in self.polybius_row:
            for col in self.polybius_col:
                if key_index < len(self.key):
                    polybius[self.key[key_index]] = row + col
                    key_index += 1
        return polybius

    def encode(self, plaintext):
        plaintext = plaintext.upper()
        ciphertext = ""
        for letter in plaintext:
            if letter in self.polybius:
                ciphertext += self.polybius[letter]
        return self.transpose(ciphertext)

    def transpose(self,ciphertext):
        dict_transpose = {}
        for i in range(len(self.transpose_key)):
            dict_transpose[self.transpose_key[i]] = i
        #Fill cipher text in a matrix with column size of the transpose key
        matrix = []
        temp = []
        for i in range(len(ciphertext)):
            if(i%len(self.transpose_key) == 0 and i != 0):
                matrix.append(temp)
                temp = []
            temp.append(ciphertext[i])
        #Fill the last row with "X" if the matrix is not filled
        if(len(temp) != len(self.transpose_key)):
            for i in range(len(temp),len(self.transpose_key)):
                temp.append("X")
        matrix.append(temp)
        ciphertext_new = ""
        #Sort the transpose key
        sorted_transpose = sorted(self.transpose_key)
        for i in sorted_transpose:
            columnadd = dict_transpose[i]
            for j in range(len(matrix)):
                    ciphertext_new += matrix[j][columnadd]
        return ciphertext_new


def main():
    transpose = input().upper()
    key = input().upper()
    plaintext = input().upper()
    adfgvx = ADFGVX(key, transpose)
    print(adfgvx.encode(plaintext))


if __name__ == "__main__":
    main()
