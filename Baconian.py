class Baconian:
    SC1 = ""
    SC2 = ""
    
    def __init__(self,Sc1,Sc2):
        self.SC1 = Sc1
        self.SC2 = Sc2
    def encode(self,plaintext):
        plaintext = plaintext.lower()
        plainlist = []
        #add integer equivalent elements to list
        for i in plaintext:
            plainlist.append(ord(i)-97)
        #Convert to binary
        binarylist = []
        for i in plainlist:
            binarylist.append(format(i, '05b'))
        #Convert to Baconian
        baconianlist = []
        for i in binarylist:
            temp = ""
            for j in i:
                if j == "0":
                    temp += self.SC1
                else:
                    temp += self.SC2
            baconianlist.append(temp)
        #Print the cipher
        ciphertext = ""
        for i in baconianlist:
            ciphertext += i
        return ciphertext
    def decode(self,ciphertext):
        #Convert to binary
        binarylist = []
        temp = ""
        for i in ciphertext:
            if i == self.SC1:
                temp += "0"
            else:
                temp += "1"
            if len(temp) == 5:
                binarylist.append(temp)
                temp = ""
        #Convert to integer
        intlist = []
        for i in binarylist:
            intlist.append(int(i,2))
        #Convert to plaintext
        plaintext = ""
        for i in intlist:
            plaintext += chr(i+97)
        return plaintext
def main():
    
    Sc1,Sc2 = input("").split()
    
    ciphertext = input("")
    
    bac = Baconian(Sc1,Sc2)
    plain = bac.decode(ciphertext)
    
    print(plain.upper())
    
    

if __name__ == "__main__":
    main()