import math

# Rail Fence Cipher
def rail_encrypt(text, key):
    rail = [['\n' for i in range(len(text))] for j in range(key)]

    row, col = 0, 0
    direction = False

    for ch in text:
        if row == 0 or row == key - 1:
            direction = not direction

        rail[row][col] = ch
        col += 1

        if direction:
            row += 1
        else:
            row -= 1

    result = ""
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result += rail[i][j]

    return result

def rail_decrypt(cipher, key):
    rail = [['\n' for i in range(len(cipher))] for j in range(key)]

    row, col = 0, 0
    direction = None

    for i in range(len(cipher)):
        if row == 0:
            direction = True
        if row == key - 1:
            direction = False

        rail[row][col] = '*'
        col += 1

        if direction:
            row += 1
        else:
            row -= 1

    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1

    result = ""
    row, col = 0, 0

    for i in range(len(cipher)):
        if row == 0:
            direction = True
        if row == key - 1:
            direction = False

        result += rail[row][col]
        col += 1

        if direction:
            row += 1
        else:
            row -= 1

    return result

# Columnar Cipher
def columnar_encrypt(message, key):
    col = len(key)
    row = math.ceil(len(message) / col)

    fill = row * col - len(message)
    message += '_' * fill

    matrix = []
    index = 0

    for i in range(row):
        matrix.append(list(message[index:index + col]))
        index += col

    order = sorted(list(enumerate(key)), key=lambda x: x[1])

    cipher = ""

    for index, _ in order:
        for r in range(row):
            cipher += matrix[r][index]

    return cipher


def columnar_decrypt(cipher, key):
    col = len(key)
    row = math.ceil(len(cipher) / col)

    matrix = [['' for i in range(col)] for j in range(row)]

    order = sorted(list(enumerate(key)), key=lambda x: x[1])

    index = 0

    for col_index, _ in order:
        for r in range(row):
            matrix[r][col_index] = cipher[index]
            index += 1

    plain = ""

    for r in range(row):
        for c in range(col):
            plain += matrix[r][c]

    return plain.replace('_', '')

# Main Program 
print("1. Rail Fence Cipher")
print("2. Columnar Transposition Cipher")

choice = int(input("Enter your choice (1/2): "))

if choice == 1:
    text = input("Enter Plain Text: ").replace(" ", "").upper()
    key = int(input("Enter Number of Rails: "))

    cipher = rail_encrypt(text, key)
    print("Encrypted Text:", cipher)

    plain = rail_decrypt(cipher, key)
    print("Decrypted Text:", plain)

elif choice == 2:
    text = input("Enter Plain Text: ").replace(" ", "").upper()
    key = input("Enter Keyword: ").upper()

    cipher = columnar_encrypt(text, key)
    print("Encrypted Text:", cipher)

    plain = columnar_decrypt(cipher, key)
    print("Decrypted Text:", plain)

else:
    print("Invalid Choice")
