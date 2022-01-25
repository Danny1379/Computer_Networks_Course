from http import server
import socket
from threading import Thread
from utils import *
from _thread import *


class Tracker(Thread):
    def __init__(self) -> None:
        Thread.__init__(self)
        self.peers = {}
        self.port = TRACKER_PORT

    def handle_request(c, addr):
        print("request received from:", addr[0], addr[1])
        c.close()

    def run(self):
        while True:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((TRACKER_IP, self.port))
            if "n" == input("\ncontinue ?\n"):
                break
            server_socket.listen()
            c, addr = server_socket.accept()
            Thread(Tracker.handle_request, (c, addr))


def get_length(socket):
    return int.from_bytes(receive_data(1, socket), 'little')


def get_file_name(length, socket) -> str:
    data = receive_data(length, socket)
    return data.decode("utf-8")


def handle_upload_message(socket):
    length = get_length(socket)
    name = get_file_name(length, socket)
    print(name)
    socket.close()


def handle_receive_message():
    print("receive")


def read_type(socket, address) -> int:
    type = receive_data(1, socket)
    return int.from_bytes(type, "little")


def read_message(socket, address):
    type = read_type(socket, address)
    print(type)
    if type == 1:
        handle_upload_message(socket)
    elif type == 0:
        handle_receive_message()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TRACKER_IP, TRACKER_PORT))
    s.listen()
    sock, add = s.accept()
    read_message(sock, add)


main()
