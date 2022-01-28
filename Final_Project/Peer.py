import socket
import threading

from file import assemble_file
from file import get_file_bytes
from utils import RECEIVING, UPLOADING
from utils import *
from threading import Thread


class Peer(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True)
        self.mode = IDLE
        self.sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.peers = []
        self.current_file = {}
        self.file_size = 0
        self.current_file_name = ""

    def uploading(self, name):
        if self.mode != UPLOADING:
            return
        self.receiver_socket.bind(('localhost', 0))
        s_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_test.connect((TRACKER_IP, TRACKER_PORT))
        self.current_file = get_file_bytes(name)
        self.current_file_name = name
        self.file_size = len(self.current_file)  # number of chunks
        data = {"name": name, "type": UPLOADING, "size": self.file_size,
                "port": self.receiver_socket.getsockname()[1]}
        send_message(data, s_test)
        s_test.close()
        self.listen_for_request()

    def downloading(self, name):
        socket = self.receiver_socket
        socket.connect((TRACKER_IP, TRACKER_PORT))
        self.current_file_name = name
        data = {"name": name, "type": RECEIVING}
        send_message(data, socket)
        message = receive_message(socket)
        self.file_size = message["size"]
        ports = message["ports"]
        needed_chunks = set(range(self.file_size))
        for port in ports:
            socket = new_socket()
            print(port)
            make_connection(('localhost', port), socket)
            send_message({"name": name, "type": "list_chunk"}, socket)
            message = receive_message(socket)
            print("fuck")
            print("message", message)
            available_chunks = message["chunks"]
            for chunk in available_chunks:
                send_message(
                    {"name": name, "type": "get_chunk", "chunk_number": chunk}, socket)
                message = receive_message(socket)
                self.current_file[chunk] = message["chunk"]
            needed_chunks = self.get_needed_chunks(
                needed_chunks, available_chunks)
            if len(needed_chunks) == 0:
                break
        assemble_file(self.current_file, name)
        socket.close()

    def get_needed_chunks(self, needed_chunks, available_chunks):
        return needed_chunks.symmetric_difference(available_chunks)

    def listen_for_request(self):
        while True:
            self.receiver_socket.listen()
            print(self.receiver_socket.getsockname())
            socket, address = self.receiver_socket.accept()
            print("FUCK")
            Thread(target=self.handle_download, args=(
                socket, address), daemon=True).start()

    def handle_download(self, socket, address):
        print("hello")
        message = receive_message(socket)
        if message["type"] == "get_chunk":
            name = message["name"]
            chunk_number = message["chunk_number"]
            if self.current_file_name == name:
                if chunk_number in self.current_file:
                    send_message(
                        {"type": "chunk", "chunk": self.current_file[chunk_number]}, socket)
            else:
                send_message({"type": "not found"}, socket)
        elif message["type"] == "list_chunks":
            message = {"chunks": self.current_file.keys()}
            send_message(message, socket)
        socket.close()

    def run(self):
        while True:
            command = input()
            name = command.split(" ")[3]
            self.mode = command.split(" ")[2]
            print(name)
            if self.mode == RECEIVING:
                Thread(target=self.downloading, args=(
                    name,), daemon=True).start()
            elif self.mode == UPLOADING:
                Thread(target=self.uploading, args=(
                    name,), daemon=True).start()
            elif self.mode == IDLE:
                pass
            else:
                break


def main():
    node = Peer()
    node.start()
    node.join()


main()
