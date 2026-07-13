alphabet = "abcdefghijklmnopqrstuvwxyz"

# Caesar Cipher
def caesar_encrypt(message, shift):
    result = ""
    for letter in message.lower():
        if letter in alphabet:
            old_position = alphabet.index(letter)
            new_position = (old_position + shift) % 26
            result += alphabet[new_position]
        else:
            result += letter
    return result


def caesar_decrypt(message, shift):
    return caesar_encrypt(message, -shift)


# Monoalphabetic (Keyword) Cipher
def build_key_alphabet(keyword):
    keyword = keyword.lower()
    seen = []
    for letter in keyword:
        if letter.isalpha() and letter not in seen:
            seen.append(letter)
    for letter in alphabet:
        if letter not in seen:
            seen.append(letter)
    return "".join(seen)


def mono_encrypt(message, keyword):
    key_alphabet = build_key_alphabet(keyword)
    result = ""
    for letter in message.lower():
        if letter in alphabet:
            position = alphabet.index(letter)
            result += key_alphabet[position]
        else:
            result += letter
    return result


def mono_decrypt(message, keyword):
    key_alphabet = build_key_alphabet(keyword)
    result = ""
    for letter in message.lower():
        if letter in key_alphabet:
            position = key_alphabet.index(letter)
            result += alphabet[position]
        else:
            result += letter
    return result

# Simple menu-based CLI
print("=== Classical Cipher Toolkit ===")
print("1. Caesar Cipher - Encrypt")
print("2. Caesar Cipher - Decrypt")
print("3. Monoalphabetic Cipher - Encrypt")
print("4. Monoalphabetic Cipher - Decrypt")

choice = input("Choose 1, 2, 3 or 4: ")
message = input("Enter your message: ")

if choice == "1":
    shift = int(input("Enter shift number (e.g. 3): "))
    print("Encrypted message:", caesar_encrypt(message, shift))
elif choice == "2":
    shift = int(input("Enter shift number (e.g. 3): "))
    print("Decrypted message:", caesar_decrypt(message, shift))
elif choice == "3":
    keyword = input("Enter keyword (e.g. SECURITY): ")
    print("Encrypted message:", mono_encrypt(message, keyword))
elif choice == "4":
    keyword = input("Enter keyword (e.g. SECURITY): ")
    print("Decrypted message:", mono_decrypt(message, keyword))
else:
    print("Invalid choice. Please enter 1, 2, 3 or 4.")
