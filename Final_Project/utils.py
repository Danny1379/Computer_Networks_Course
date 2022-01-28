import json
# file to hold extra functions and constant
TRACKER_PORT = 8080
TRACKER_IP = "localhost"


# define peer states

RECEIVING = "RECEIVING"
IDLE = "IDLE"
UPLOADING = "UPLOADING"
EXITING = "EXITING"

BUFFER = 2**16-1


def send_message(message, socket) -> bool:
    message = json.dumps(message)
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
    print(data)
    return json.loads(data)
