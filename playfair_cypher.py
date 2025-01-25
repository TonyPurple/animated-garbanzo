def create_matrix(key):
    key = key.upper()
    matrix = [[0 for i in range(5)] for j in range(5)]
    letters_added = []
    row = 0
    col = 0

    # Add the key to the matrix
    for letter in key:
        if letter not in letters_added and letter.isalpha():  # Ensure only alphabetic letters
            matrix[row][col] = letter
            letters_added.append(letter)
            if col == 4:
                col = 0
                row += 1
            else:
                col += 1

    # Add the rest of the alphabet to the matrix
    for letter in range(65, 91):  # A=65 ... Z=90
        if letter == 74:  # Skip 'J'
            continue
        if chr(letter) not in letters_added:
            letters_added.append(chr(letter))
    
    index = 0
    for i in range(5):
        for j in range(5):
            matrix[i][j] = letters_added[index]
            index += 1
    return matrix

# Add fillers if the same letter appears as a pair
def separate_same_letters(message):
    index = 0
    while index < len(message):
        l1 = message[index]
        if index == len(message) - 1:  # Last character
            message += 'X'
            index += 2
            continue
        l2 = message[index + 1]
        if l1 == l2:  # Insert 'X' between repeated letters
            message = message[:index + 1] + "X" + message[index + 1:]
        index += 2
    return message

# Return the index of a letter in the matrix
def indexOf(letter, matrix):
    for i in range(5):
        try:
            index = matrix[i].index(letter)
            return (i, index)
        except ValueError:
            continue
    return None  # In case the letter is not found (shouldn't happen)

# Implementation of the Playfair cipher
def playfair(key, message, encrypt=True):
    inc = 1 if encrypt else -1
    matrix = create_matrix(key)
    message = message.upper().replace(' ', '')
    message = separate_same_letters(message)
    cipher_text = ''

    for l1, l2 in zip(message[0::2], message[1::2]):
        row1, col1 = indexOf(l1, matrix)
        row2, col2 = indexOf(l2, matrix)
        if row1 == row2:  # Rule 2: Same row
            cipher_text += matrix[row1][(col1 + inc) % 5] + matrix[row2][(col2 + inc) % 5]
        elif col1 == col2:  # Rule 3: Same column
            cipher_text += matrix[(row1 + inc) % 5][col1] + matrix[(row2 + inc) % 5][col2]
        else:  # Rule 4: Rectangle
            cipher_text += matrix[row1][col2] + matrix[row2][col1]

    return cipher_text

# Main application
if __name__ == '__main__':
    print('Type the Key:')
    secret = input().strip()
    print('Type the Message:')
    message = input().strip()
    encrypted_message = playfair(secret, message)
    print('Encrypted Message ->', encrypted_message)
    decrypted_message = playfair(secret, encrypted_message, False)
    print('Decrypted Message ->', decrypted_message)
