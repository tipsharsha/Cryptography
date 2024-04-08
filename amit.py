class ADFGVX_Cipher:
    def __init__(self, substitution, keyword):
        alphabet1='CRYPTO'
        alphabet2='GRAPHY'
        self.substitution = list(substitution.upper())
        self.keyword = list(keyword)
        self.keyword_length = len(self.keyword)
        self.alphabet1 = list(alphabet1)
        self.alphabet2 = list(alphabet2)

        pairs = [a + b for a in self.alphabet1 for b in self.alphabet2]
        self.encode_dict = dict(zip(self.substitution, pairs))
        self.decode_dict = {v: k for k, v in self.encode_dict.items()}

    def encrypt(self, message):
        encoded_chars = ''.join([self.encode_dict[char] for char in message.upper() if char in self.substitution])
        columns = [(letter, encoded_chars[i::self.keyword_length]) for i, letter in enumerate(self.keyword)]
        columns.sort(key=lambda x: x[0])
        max_length = len(max(columns, key=lambda x: len(x[1]))[1])
        for i in range(len(columns)):
            columns[i] = (columns[i][0], columns[i][1] + 'X' * (max_length - len(columns[i][1])))
        return ''.join([''.join(column[1]) for column in columns])

substitution = input()
keyword = input()
message = input()
cipher = ADFGVX_Cipher(substitution, keyword)
cipher_text = cipher.encrypt(message)
print(cipher_text)
