class Playfair:
    def __init__(self, key):
        self.key = key
        self.matrix = []

    def fill_matrix(self):
        # Initialize the matrix with zeros
        self.matrix = [['' for _ in range(5)] for _ in range(5)]

        # Fill the matrix with the key
        key_index = 0
        for row in range(5):
            for col in range(5):
                if key_index < len(self.key):
                    self.matrix[row][col] = self.key[key_index]
                    key_index += 1
                else:
                    # Fill remaining matrix positions with the remaining alphabet letters
                    for i in range(26):
                        letter = chr(65 + i)
                        if letter != 'J' and letter not in self.key:
                            self.matrix[row][col] = letter
                            break

    def find_position(self, letter):
        for i in range(5):
            for j in range(5):
                if self.matrix[i][j] == letter:
                    return (i, j)

    def decode(self, ciphertext):
        # Remove 'J' and replace it with 'I' in the ciphertext
        ciph = ciphertext.upper().replace('J', 'I')
        self.fill_matrix()
        plaintext = ""
        for i in range(0, len(ciph), 2):
            
            pos1 = self.find_position(ciph[i])
            pos2 = self.find_position(ciph[i + 1])
            if pos1[0] == pos2[0]:
                plaintext += self.matrix[pos1[0]][(pos1[1] - 1) % 5]
                plaintext += self.matrix[pos2[0]][(pos2[1] - 1) % 5]
            elif pos1[1] == pos2[1]:
                plaintext += self.matrix[(pos1[0] - 1) % 5][pos1[1]]
                plaintext += self.matrix[(pos2[0] - 1) % 5][pos2[1]]
            else:
                plaintext += self.matrix[pos1[0]][pos2[1]]
                plaintext += self.matrix[pos2[0]][pos1[1]]
        return plaintext


class Vigenere:
    def __init__(self, key):
        self.key = key.upper()

    def decode(self, ciphertext):
        ciph = ciphertext.upper()
        plaintext = ""
        key_index = 0
        for char in ciph:
            if char.isalpha():
                key_char = self.key[key_index % len(self.key)]
                key_index += 1
                shift = ord(key_char) - ord('A')
                plaintext += chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            else:
                plaintext += char
        return plaintext


class Columnar:
    def __init__(self, key):
        self.transpose_key = key

    def decrypt(self, ciphertext):
        num_cols = len(self.transpose_key)
        num_rows = -(-len(ciphertext) // num_cols)  # Ceiling division
        sorted_key_indices = sorted(range(num_cols), key=lambda k: self.transpose_key[k])

        plaintext = ""
        for col in range(num_cols):
            for row in range(num_rows):
                index = sorted_key_indices.index(col)
                position = index * num_rows + row
                if position < len(ciphertext):
                    plaintext += ciphertext[position]
        return plaintext


def main():
    try:
        key_playfair = input()
        key_vigenere = input()
        key_columnar = input()
        ciphertext = input()

        vig = Vigenere(key_vigenere)
        col = Columnar(key_columnar)
        int2 = col.decrypt(ciphertext)
        int1 = vig.decode(int2)
        print(int1)
    #     plain = Playfair(key_playfair)
    #     print(plain.decode(int1))
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    main()
