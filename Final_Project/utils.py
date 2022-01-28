from base64 import decode
import json
import socket

from cypher import decrypt, encrypt
# file to hold extra functions and constant
TRACKER_PORT = 8080
TRACKER_IP = "localhost"


# define peer states

RECEIVING = "receive"
IDLE = "IDLE"
UPLOADING = "send"
EXITING = "EXITING"

BUFFER = 2**16-1

# chunks
CHUNK_SIZE = 32 * 2**10  # 32 KByte chunk size


def make_connection(address, socket):
    socket.connect(address)


def new_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send_message(message, socket) -> bool:
    message = json.dumps(message)
    print(message)
    # encrypt string
    message = encrypt(message, 10)
    data = message.encode("utf-8")
    try:
        socket.sendall(data)
        return True
    except Exception as e:
        print(e)
        return False


def receive_byte(socket) -> bytes:
    return socket.recv(1)


def receive_data(socket) -> bytes:
    d = socket.recv(BUFFER)
    return d


def receive_message(socket) -> dict:
    data = receive_data(socket).decode('utf-8')
    # decrypt string
    data = decrypt(data, 10)
    return json.loads(data)
