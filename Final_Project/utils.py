# file to hold extra functions and constant
TRACKER_PORT = 8080
TRACKER_IP = "localhost"


# define peer states

RECEIVING = "RECEIVING"
IDLE = "IDLE"
UPLOADING = "UPLOADING"


def send_message(message, socket) -> bool:
    try:
        print(message)
        socket.sendall(message)
        return True
    except Exception as e:
        print(e)
        return False


def receive_byte(socket) -> bytes:
    return socket.recv(1)


def receive_data(length, socket) -> bytes:
    d = b''
    for i in range(length):
        try:
            d += receive_byte(socket)
        except Exception as e:
            print(e)
            return d
    return d


def receive_ports(socket, length) -> list:
    ports = []
    for i in range(length):
        try:
            ports.append(int.from_bytes(receive_data(2, socket), "little"))
        except Exception as e:
            print(e)
            return ports
    return ports
