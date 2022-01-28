
import socket
from utils import RECEIVING
from utils import receive_message
from utils import UPLOADING
from utils import TRACKER_IP, TRACKER_PORT, send_message
import json


def main():
    s_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_test.connect((TRACKER_IP, TRACKER_PORT))
    name = 'the fellowship of attar'
    size = 64
    data = {"name": name, "type": RECEIVING}
    send_message(data, s_test)
    ports = receive_message(s_test)["ports"]
    print(ports)


main()
