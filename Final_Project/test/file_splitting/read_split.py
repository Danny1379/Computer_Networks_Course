

byte_string = []
with open("test.txt", "rb") as f:
    byte = f.read(256)
    byte_string.append(byte)
    while byte:
        byte = f.read(256)
        byte_string.append(byte)


print(len(byte_string[len(byte_string)-2]))
