import socket
from threading import Thread

from numpy import byte
from utils import *
import json


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

    def handle_upload_message(self, socket, message, address):
        port = address[1]
        name = message["name"]
        self.add_uploader(name, port)
        # if not (name in self.peers):
        #     self.peers[name] = {port}
        # self.peers[name].add(port)
        socket.close()

    def find_ports(self, name) -> list:
        ports = []
        if name in self.peers:
            for port in self.peers[name]:
                ports.append(port)
        return ports

    def add_uploader(self, name, port) -> None:
        if not (name in self.peers):
            self.peers[name] = {port}
        self.peers[name].add(port)

    def handle_receive_message(self, socket, message, address) -> None:
        port = address[1]
        name = message["name"]
        ports = self.find_ports(name)
        message = {"ports": ports}
        send_message(message, socket)

    def read_type(self, socket, message, address) -> int:
        type = receive_data(1, socket)
        return int.from_bytes(type, "little")

    def read_message(self, socket, address) -> None:
        message = receive_message(socket)  # self.read_type(socket, address)
        type = message['type']
        if type == UPLOADING:
            self.handle_upload_message(socket, message, address)
        elif type == RECEIVING:
            self.handle_receive_message(socket, message, address)
        return


def main():
    tracker = Tracker()
    tracker.start()
    while input("Do you wish to continue master ?") != "n":
        continue


main()
