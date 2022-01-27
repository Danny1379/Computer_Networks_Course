
import socket
from utils import TRACKER_IP, TRACKER_PORT, send_message


def main():
    s_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_test.connect((TRACKER_IP, TRACKER_PORT))
    name = 'the fellowship of attar'.encode("utf-8")
    length = int.to_bytes(len(name), 1, "little")
    data = int.to_bytes(0, 1, "little") + length + name
    send_message(data, s_test)
    receive_ports(socket, length)


main()
