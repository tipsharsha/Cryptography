
class ADFGVX:
    def __init__(self,key,transpose_key):
        self.polybius_row =["C","R","Y","P","T","O"]
        self.polybius_col =["G","R","A","P","H","Y"]
        self.transpose_key = transpose_key
        self.key = key
        self.polybius = self.fill_polybius()
    def fill_polybius(self):
        dict_alpha = {}
        polybius = {}
        for i in range(26):
            dict_alpha[chr(65+i)] = False
        for i in range(10):
            dict_alpha[str(i)] = False
        row_num =0
        col_num = 0
        for i in self.key:
            if(dict_alpha[i] == False):
                dict_alpha[i] = True
                polybius[i] = self.polybius_row[row_num]+self.polybius_col[col_num]
                col_num += 1
            if(col_num == 6):
                row_num += 1
                col_num = 0
        return polybius
            
    def encode(self,plaintext):
        #Encode the plaintext
        plaintext = plaintext.upper()
        ciphertext = ""
        for letter in plaintext:
            #find in polybius
            ciphertext += self.polybius[letter]
        ciphertext = self.transpose(ciphertext)
        return ciphertext
    def transpose(self,ciphertext):
        letters = list(ciphertext)
        matrix = {x: letters[i:len(letters):len(self.transpose_key)] for i, x in enumerate(self.transpose_key)}
        # print(matrix)       
        letters = sorted(self.transpose_key)
        ciphertext = ""
        max_length = len(matrix[letters[0]])
        for letter in letters:
            for i in range(len(matrix[letter])):
                ciphertext += matrix[letter][i]
            for i in range(max_length -len(matrix[letter])):
                ciphertext += "X"
        return ciphertext
            
        

def main():
    transpose = input().upper()
    key = input().upper()
    plaintext = input().upper()
    adfgvx = ADFGVX(key,transpose)
    print(adfgvx.encode(plaintext).upper())
    
if __name__ == "__main__":
    main()