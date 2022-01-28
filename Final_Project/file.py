

from genericpath import isfile
from utils import CHUNK_SIZE

# chunk size is 32KByte


def get_file_bytes(name):
    byte_array = {}
    chunk_number = 0
    with open(name, "rb") as f:
        byte = f.read(CHUNK_SIZE)
        byte_array[chunk_number] = byte
        while byte:
            chunk_number += 1
            byte = f.read(CHUNK_SIZE)
            byte_array[chunk_number] = byte
    return byte_array


def assemble_file(file_chunks, name):
    file_bytes = b''
    for i in range(len(file_chunks)):
        file_bytes += file_chunks[i]
    if isfile(name):
        name = name.split('.')
        name = name[0]+"2"+"."+name[1]

    with open(name, 'wb') as fp:
        fp.write(file_bytes)
    print("file_created")
