from pycipher import ColTrans


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
        print(polybius)
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
        col = ColTrans(self.transpose_key)
        return col.encipher(ciphertext)
        
        

def main():
    transpose = input().upper()
    key = input()
    plaintext = input().upper()
    adfgvx = ADFGVX(key,transpose)
    print(adfgvx.encode(plaintext))
    
if __name__ == "__main__":
    main()