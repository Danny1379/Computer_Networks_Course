import socket
import base64
import ssl


def handShake(conn):
    #clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(mailServer)
    recv = clientSocket.recv(1024)
    return recv


SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "dannyhosna@gmail.com"
RECEIVER_EMAIL = "dazza1379@gmail.com"
SENDER_PASS = "123456net"


def sendHelo(conn):
    sendHelo = f"HELO dan \r\n"
    conn.send(sendHelo.encode("utf-8"))
    recv = clientSocket.recv(1024)
    return recv


def sendMailFrom(conn):
    sendMailFrom = f"MAIL FROM: <{SENDER_EMAIL}>\r\n"
    conn.send(sendMailFrom.encode())
    recv = conn.recv(1024)
    return recv


def sendAuthLOGIN(conn):

    # send user name
    username = base64.b64encode(
        SENDER_EMAIL.encode()) + "\r\n".encode()
    conn.send(username)

    recv = conn.recv(1024)
    recv = recv.decode()
    recv = recv.split(" ")
    print(base64.b64decode(recv[1]))

    # send password
    password = base64.b64encode(
        SENDER_PASS.encode()) + "\r\n".encode()
    conn.send(password)
    recv = conn.recv(1024)
    recv = recv.decode("ascii")
    print(recv)


def sendRCP(conn):
    rcp = f"RCPT TO: <{RECEIVER_EMAIL}>\r\n".encode()
    conn.send(rcp)
    recv = conn.recv(1024)
    return recv


def sendData(conn):
    conn.send("DATA\r\n".encode())
    recv = conn.recv(1024)
    print(recv.decode())

    # send data
    conn.send("Do you like ketchup?\r\n".encode())
    conn.send("i know i do\r\n".encode())
    conn.send(".\r\n".encode())
    recv = conn.recv(1024)
    print(recv.decode())


def sendQuit(conn):
    conn.send(b"QUIT\r\n")
    recv = conn.recv(1024)
    print(recv.decode())


mailServer = (SMTP_SERVER, 587)

# hand shake
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recv = handShake(clientSocket)
recv = recv.decode()
print(recv)
recieve = recv.split(" ")
if int(recieve[0]) != 220:
    print("did not receive correct response from server")
    exit()
# send HELO
recv = sendHelo(clientSocket)
recv = recv.decode()
print(recv)
receive = recv.split(" ")
code = int(receive[0])
if code != 250:
    print("did not receive correct response from server")
    exit()

# send authentication
# sendAuthPlain(clientSocket)
# start ttls
clientSocket.send(b"STARTTLS \r\n")
recv = clientSocket.recv(1024)
recv = recv.decode()
print(recv)


# wrap ssl
secureClientSocket = ssl.wrap_socket(
    clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)
secureClientSocket.send(b"AUTH login \r\n")
recv = secureClientSocket.recv(1024)
recv = recv.decode("utf-8")
recv = recv.split(" ")
print(base64.b64decode(recv[1]))

#
sendAuthLOGIN(secureClientSocket)
# send mail from
recv = sendMailFrom(secureClientSocket)
recv = recv.decode()
print(recv)
recv = recv.split(" ")
if recv[0] != "250":
    print("error ")
    exit()

recv = sendRCP(secureClientSocket)
print(recv.decode())

sendData(secureClientSocket)

sendQuit(secureClientSocket)
