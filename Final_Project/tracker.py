import socket
from threading import Thread

from numpy import byte
from utils import *
#from _thread import *


class Tracker(Thread):
    def __init__(self) -> None:
        Thread.__init__(self, daemon=True)
        self.peers = {}
        self.port = TRACKER_PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((TRACKER_IP, TRACKER_PORT))

    def handle_request(self, handler_socket, address):
        self.read_message(handler_socket, address)
        print("handled")

    def run(self):
        while True:
            self.socket.listen()
            handler, address = self.socket.accept()
            Thread(target=self.handle_request(
                handler, address), daemon=True)
            # if "n" == input("\ncontinue ?\n"):
            #    break

    def get_length(self, socket):
        return int.from_bytes(receive_data(1, socket), 'little')

    def get_file_name(self, length, socket) -> str:
        data = receive_data(length, socket)
        return data.decode("utf-8")

    def handle_upload_message(self, socket, address):
        port = address[1]
        length = self.get_length(socket)
        name = self.get_file_name(length, socket)
        print(name)
        if not (name in self.peers):
            self.peers[name] = {port}
        self.peers[name].add(port)
        socket.close()

    def handle_receive_message(self, socket, address):
        port = address[1]
        length = self.get_length(socket)
        name = self.get_file_name(length, socket)
        self.send_ports(socket, name)
        print(name)

    def read_type(self, socket, address) -> int:
        type = receive_data(1, socket)
        return int.from_bytes(type, "little")

    def read_message(self, socket, address):
        type = self.read_type(socket, address)
        print(type)
        if type == 1:
            self.handle_upload_message(socket, address)
        elif type == 0:
            self.handle_receive_message(socket, address)

        print(self.peers)

    def send_ports(self, socket, movie):
        print(movie in self.peers)
        if movie in self.peers:
            length = len(self.peers[movie])
            message = int.to_bytes(length, length=1, byteorder="little")
            for port in self.peers[movie]:
                message += int.to_bytes(port, length=2, byteorder="little")
        else:
            length = 0
            message = int.to_bytes(length, length=1, byteorder="little")

        send_message(message, socket)


def main():
    tracker = Tracker()
    tracker.start()
    while input("Do you wish to continue master ?") != "n":
        continue


main()
