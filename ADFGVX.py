

class ADFGVX:
    def __init__(self,key,transpose_key):
        self.polybius_row =["C","R","Y","P","T","O"]
        self.polybius_col =["G","R","A","P","H","Y"]
        self.transpose_key = transpose_key
        self.key = key
        self.polybius = self.fill_polybius()
    def fill_polybius(self):
        #Fill the polybius square
        polybius = []
        #Fill the matrix with the key left to right and top to bottom
        temp =[]
        for i in range(len(self.key)):
            if(i%6 == 0 and i != 0):
                polybius.append(temp)
                temp =[]
            temp.append(self.key[i])
        polybius.append(temp)
        #if matrix is not filled to 6*6 fill the rest with the alphabet
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        for i in range(len(alphabet)):
            if(alphabet[i] not in self.key):
                temp.append(alphabet[i])
                if(len(temp) == 6):
                    polybius.append(temp)
                    temp = []
        return polybius
    def encode(self,plaintext):
        #Encode the plaintext
        plaintext = plaintext.upper()
        ciphertext = ""
        for letter in plaintext:
            #find in polybius
            for i in range(len(self.polybius)):
                for j in range(len(self.polybius[i])):
                    if self.polybius[i][j] == letter:
                        ciphertext += self.polybius_row[i] + self.polybius_col[j]
        ciphertext = self.transpose(ciphertext)
        return ciphertext
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
    key = input()
    plaintext = input().upper()
    adfgvx = ADFGVX(key,transpose)
    print(adfgvx.encode(plaintext))
    
if __name__ == "__main__":
    main()