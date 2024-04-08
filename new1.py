def construct_polybius_square(permutation):
    polybius_square = {}
    characters = "CRYPTOGRAPHY"
    for i, char in enumerate(characters):
        polybius_square[char] = permutation[i * 2: (i + 1) * 2]
    return polybius_square

def substitute_with_polybius(plaintext, polybius_square):
    substituted_text = ""
    for char in plaintext:
        if char in polybius_square:
            substituted_text += polybius_square[char]
    return substituted_text

def columnar_transposition(keyword, substituted_text):
    keyword_sorted = sorted(keyword)
    keyword_indices = {char: i for i, char in enumerate(keyword)}
    num_cols = len(keyword)
    num_rows = -(-len(substituted_text) // num_cols)  # ceiling division
    matrix = [['X'] * num_cols for _ in range(num_rows)]
    
    for i, char in enumerate(substituted_text):
        row = i % num_rows
        col = keyword_indices[keyword_sorted[i // num_rows]]
        matrix[row][col] = char
    
    transposed_text = ""
    for col in range(num_cols):
        for row in range(num_rows):
            transposed_text += matrix[row][col]
    
    return transposed_text

def adfgvx_cipher(keyword, permutation, plaintext):
    polybius_square = construct_polybius_square(permutation)
    substituted_text = substitute_with_polybius(plaintext, polybius_square)
    print(substituted_text)
    ciphertext = columnar_transposition(keyword, substituted_text)
    return ciphertext

# Sample Input
keyword = "CIPHER"
permutation = "J9I1E8D2Z6Y3M0C7K5LQOX4SFTUAGHNRWPBV"
plaintext = "TEXTTOENCRYPT"

# Encrypt the plaintext
ciphertext = adfgvx_cipher(keyword, permutation, plaintext)
print("Cipher text:", ciphertext)
