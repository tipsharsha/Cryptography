
class Playfair:
    def __init__(self,key):
        self.key = key
        self.matrix = []
    def fill_matrix(self):
        #Fill the matrix with the key
        count = 0
        temp =[]
        dict = {}
        for i in range(26):
            dict[chr(65+i)] = False
        for letter in self.key:
            if count%5 == 0 and count != 0:
                self.matrix.append(temp)
                temp = []
            if dict[letter] == False:
                temp.append(letter)
                dict[letter] = True
                count += 1
        for i in range(26):
            if dict[chr(65+i)] == False and chr(65+i) != 'J':
                if count%5 == 0 and count != 0:
                    self.matrix.append(temp)
                    temp = []
                temp.append(chr(65+i))
                count += 1

        self.matrix.append(temp)
        
    def find_position(self,letter):
        for i in range(5):
            for j in range(5):
                if self.matrix[i][j] == letter:
                    return (i,j)
    def decode(self,ciphertext):
        #Remove the letter J from the ciphertext
        ciph = ciphertext.upper()
        ciph = ciph.replace('J','I')
        #Fill the matrix with the key
        self.fill_matrix()
        #Fill the matrix with the key
        plaintext = ""
        # for i in range(0,len(ciph),2):
        #     if ciph[i] == ciph[i+1]:
        #         ciph = ciph[:i+1] + 'X' + ciph[i+1:]
        # if len(ciph)%2 != 0:
        #     ciph += 'X'
        for i in range(0,len(ciph),2):
            pos1 = self.find_position(ciph[i])
            pos2 = self.find_position(ciph[i+1])
            if pos1[0] == pos2[0]:
                plaintext += self.matrix[pos1[0]][(pos1[1]-1)%5]
                plaintext += self.matrix[pos2[0]][(pos2[1]-1)%5]
            elif pos1[1] == pos2[1]:
                plaintext += self.matrix[(pos1[0]-1)%5][pos1[1]]
                plaintext += self.matrix[(pos2[0]-1)%5][pos2[1]]
            else:
                plaintext += self.matrix[pos1[0]][pos2[1]]
                plaintext += self.matrix[pos2[0]][pos1[1]]
        return plaintext
        

class Vigenere:
    def __init__(self,key):
        self.key = key
    def decode(self,ciphertext):
        ciph = ciphertext.upper()
        mapping = {chr(65+i):i for i in range(26)}
        plaintext_list = [mapping[x] for x in ciph]
        key_list = [mapping[x] for x in self.key]
        for i in range(len(plaintext_list)):
            plaintext_list[i] = (plaintext_list[i] - key_list[i%len(self.key)])%26
        plaintext = ''.join([chr(65+x) for x in plaintext_list])
        return plaintext

class Columnar:
    def __init__(self,key):
        self.transpose_key = key
    def reverse_transpose(self,ciphertext):
        #Sort the transpose key
        original = self.transpose_key
        self.transpose_key = sorted(self.transpose_key)
        dict_transpose = {}
        for i in range(len(self.transpose_key)):
            dict_transpose[self.transpose_key[i]] = i
    
        #Fill cipher text in a matrix with column size of the transpose key
        num_rows = len(ciphertext)//len(self.transpose_key)
        matrix = []
        temp = []
        for i in range(len(ciphertext)):
            if(i%num_rows == 0 and i != 0):
                matrix.append(temp)
                temp = []
            (temp).append(ciphertext[i])
        matrix.append(temp)

        ciphertext_new = ""
        for i in range(num_rows):
            for j in original:
                pos = dict_transpose[j]
                ciphertext_new += matrix[pos][i]
        #remove X from the end
        while ciphertext_new[-1] == 'X':
            ciphertext_new = ciphertext_new[:-1]
        return ciphertext_new

def main():
    key_playfair = input()
    key_vigenere = input()
    key_columnar = input()
    ciphertext = input()
    vig = Vigenere(key_vigenere)
    col = Columnar(key_columnar)
   
    int2 = col.reverse_transpose(ciphertext)
    int1 = vig.decode(int2)
    plain = Playfair(key_playfair)
    print(plain.decode(int1))
    


if __name__ =="__main__":
    main()