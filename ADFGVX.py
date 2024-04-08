class ADFGVX:
    def __init__(self,key,transpose_key):
        self.polybius_row =["C","R","Y","P","T","O"]
        self.polybius_col =["G","R","A","P","H","Y"]
        self.transpose_key = transpose_key
        self.key = key
        self.keyword_length = len(self.transpose_key)
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
        #fill the rest of the polybius square with the alphabet
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
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
        columns = [(letter, ciphertext[i::len(self.transpose_key)]) for i, letter in enumerate(self.transpose_key)]
        #Sort the columns
        columns.sort(key=lambda col: col[0])
        max_length = len(max(columns, key=lambda x: len(x[1]))[1])
        for i in range(len(columns)):
            columns[i] = (columns[i][0], columns[i][1] + 'X' * (max_length - len(columns[i][1])))
        ciphertext = ""
        for column in columns:
            for i in range(len(column[1])):
                ciphertext += column[1][i]
        return ciphertext

            
        

def main():
    transpose = input().upper()
    key = input()
    plaintext = input().upper()
    adfgvx = ADFGVX(key,transpose)
    print(adfgvx.encode(plaintext))
    
if __name__ == "__main__":
    main()