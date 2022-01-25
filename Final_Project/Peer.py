
from audioop import add
import socket
import threading
from utils import IDLE, receive_data


class Peer():
    def __init__(self):
        self.mode = IDLE
        self.sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.peers = []

    def receive():
        pass

    def upload():
        pass

    def broadcast_question(self):
        for i in range(1024, 2**16-1):
            try:
                self.sender_socket.connect(("localhost", 8080))
                self.sender_socket.send(
                    b'hello')
                d = self.sender_socket.recv(1024)
                # print(d)
                break
            except Exception as e:
                print(e)
                pass


def main():
    pass


main()
