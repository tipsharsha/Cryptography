

class Railfence:
    def __init__(self,key):
        self.key = key
    def decode(self,ciphertext):
        #Decode the ciphertext
        ciphertext = ciphertext.upper()
        plaintext = ""
        #Create the railfence
        railfence = []
        for i in range(self.key):
            railfence.append([])
        #Fill the railfence
        index = 0
        direction = 1
        for i in range(len(ciphertext)):
            railfence[index].append(0)
            if direction == 1:
                index += 1
            else:
                index -= 1
            if index == self.key-1:
                direction = -1
            elif index == 0:
                direction = 1
        #Fill the railfence with the ciphertext
        index = 0
        for i in range(self.key):
            for j in range(len(railfence[i])):
                railfence[i][j] = ciphertext[index]
                index += 1
        #Read the railfence
        index = 0
        direction = 1
        for i in range(len(ciphertext)):
            plaintext += railfence[index][0]
            railfence[index].pop(0)
            if direction == 1:
                index += 1
            else:
                index -= 1
            if index == self.key-1:
                direction = -1
            elif index == 0:
                direction = 1
        return plaintext

class StrafflingCheckerboard:
    def __init__(self,key,digits):
        self.key = key
        self.digits = digits
        self.checkerboard = {}
        self.letter_dict = {}
    def prepare_checkerboard(self):
        temp =[]
        j = 0
        for i in range(10):
            if(i != self.digits[0] and i != self.digits[1]):
                temp.append(self.key[j])
                j+=1
            else:
                temp.append(' ')
        self.checkerboard[' '] = temp
        self.checkerboard[self.digits[0]] = []
        self.checkerboard[self.digits[1]] = []
        #Fill the rest of the checkerboard
        key_left = self.key[8:]
        count = 0
        for digit in self.digits:
            temp = []
            for i in range(10):
                try:
                    temp.append(key_left[count*10+i])
                except:
                    temp.append(' ')
            count += 1
            self.checkerboard[digit] = temp
    def make_letter_dict(self):
        for check in self.checkerboard:
            for i in range(10):
                if self.checkerboard[check][i] != ' ' and check!=' ':
                    self.letter_dict["{}{}".format(check,i)] =  self.checkerboard[check][i]
                elif check == ' ':
                    self.letter_dict["{}".format(i) ] = self.checkerboard[check][i]
    def decode(self,ciphertext):
        plaintext = ""
        i = 0
        while i < len(ciphertext):
            if ciphertext[i] == f"{self.digits[0]}" or ciphertext[i] == f"{self.digits[1]}":
                plaintext += self.letter_dict[ciphertext[i:i+2]]
                i += 2
            else:
                plaintext += self.letter_dict[ciphertext[i]]
                i += 1
        return plaintext
                
       
        


def main():
    key = input() #key for straddling checkerboard
    digits = input() #digits excluded from the checkerboard
    digits = list(map(int,digits.split()))
    ciphertext = input() #ciphertext to decode
    key_rail = input() #key for railfence
    rail = Railfence(int(key_rail))
    checker = StrafflingCheckerboard(key,digits)
    checker.prepare_checkerboard()
    checker.make_letter_dict()
    intermediate = rail.decode(ciphertext)
    plaintext = checker.decode(intermediate)
    print(plaintext)



if __name__ == "__main__":
    main()