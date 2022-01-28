from threading import Lock
import socket
from threading import Thread

from numpy import byte
from utils import *
import json


class Tracker(Thread):
    def __init__(self) -> None:
        Thread.__init__(self, daemon=True)
        self.files = {}
        self.port = TRACKER_PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((TRACKER_IP, TRACKER_PORT))
        self.mutex_lock = Lock()

    def handle_request(self, handler_socket, address):
        self.handle_messages(handler_socket, address)
        print("handled")

    def run(self):
        while True:
            self.socket.listen()
            handler, address = self.socket.accept()
            t1 = Thread(target=self.handle_request, args=(
                handler, address), daemon=True)
            t1.start()

    def handle_upload_message(self, socket, message, address):
        port = message["port"]
        name = message["name"]
        size = message["size"]
        self.add_uploader(name, port, size)
        socket.close()

    def find_ports(self, name) -> list:
        self.mutex_lock.acquire()
        ports = []
        size = 0
        if name in self.files:
            size = self.files[name]['size']
            for port in self.files[name]['ports']:
                ports.append(port)
        self.mutex_lock.release()
        print(size)
        return ports, size

    def add_uploader(self, name, port, size) -> None:
        self.mutex_lock.acquire()
        if not (name in self.files):
            self.files[name] = {"ports": {port}, "size": size}
        self.files[name]['ports'].add(port)
        self.mutex_lock.release()

    def handle_receive_message(self, socket, message, address) -> None:
        port = address[1]
        name = message["name"]
        ports, size = self.find_ports(name)
        message = {"ports": ports, "size": size}
        send_message(message, socket)

    def handle_peer_leaving(self, message, address):
        port = message["port"]
        file = message["file"]
        self.files[file]["ports"].remove(port)
        print(f"port {port} has been remove from {file} list")

    def handle_messages(self, socket, address) -> None:
        message = receive_message(socket)  # self.read_type(socket, address)
        type = message['type']
        if type == UPLOADING:
            self.handle_upload_message(socket, message, address)
        elif type == RECEIVING:
            self.handle_receive_message(socket, message, address)
        elif type == EXITING:
            self.handle_peer_leaving(message, address)
        return


def main():
    tracker = Tracker()
    tracker.start()
    while input("Do you wish to continue master ?") != "n":
        continue


main()
