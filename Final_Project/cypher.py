# caesars cipher implementation for base64 encoded strings
def encrypt(data, shift):
    encrypted_data = ""
    for c in data:
        if not c.isalpha():
            encrypted_data += c
        elif c.isupper():
            encrypted_data += chr((ord(c) + shift - 65) % 26 + 65)
        else:
            encrypted_data += chr((ord(c) + shift - 97) % 26 + 97)
    return encrypted_data


# decryption is the inversion of encryption
def decrypt(data, shift):
    return encrypt(data, 26 - shift)
