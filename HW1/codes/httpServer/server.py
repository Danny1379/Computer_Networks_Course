import socket
import os
import mimetypes
SERVER_NAME = 'localhost'
SERVER_PORT = 80


class Request():
    def __init__(self, method, path, version) -> None:
        self.method = method
        self.version = version
        self.path = path
        self.headers = {}
        self.body = ""

    def __str__(self) -> str:
        return self.method + " " + self.path


class Response():
    def __init__(self, request) -> None:
        self.request = request
        self.headers = {}
        self.body = ""

    def getResponse(self, conn) -> str:
        if self.request.path == "/":
            self.request.path = "/index.html"
        self.request.path = '.' + self.request.path

        resp = ""
        try:
            content_type, _ = mimetypes.guess_type(self.request.path)
            file = open(self.request.path)

            self.body = file.read()

            statusLine = "HTTP/1.1" + " " + \
                "200" + " " + "OK" + "\r\n"
            headerlines = f"Content-Type: {content_type}\r\n"
            headerlines += f"Content-Length: {len(self.body.encode('utf-8'))}\r\n"

            resp = statusLine + headerlines + "\r\n" + self.body + "\r\n"

        except Exception as e:
            self.body = "<h1>FILE NOT FOUND</h1>"
            statusLine = self.request.version + " " + "404" + " " + "NOT FOUND" + "\r\n"
            headerlines = "Content-Type: text/html\r\n"
            headerlines += f"Content-Length: {18}\r\n"
            resp = statusLine + headerlines + "\r\n" + self.body

        return resp


RESPONSE = b"""\
HTTP/1.1 200 OK
Content-type: text/html
Content-length: 15

<h1>test!</h1>""".replace(b"\n", b"\r\n")


RESPONSE_BAD_REQUEST = b"""\
HTTP/1.1 400 BAD REQUEST
Content-type: text/html
Content-length: 15

<h1>BAD REQUEST</h1>""".replace(b"\n", b"\r\n")


def readLine(socket) -> str:
    line = b""
    while True:
        data = socket.recv(1)  # read one byte from recv
        if(data == b"\n"):
            line += data
            break
        line += data
    return line


# get request first line and return request object
def getRequestLine(socket) -> Request:
    try:
        requestLine = str(readLine(socket))    # read request line
        requestLine = requestLine.split(" ")
        requestLine[2] = requestLine[2].replace("\\r\\n", "")
        return Request(requestLine[0], requestLine[1], requestLine[2])
    except:
        print('err')


def getRequestHeaders(socket, request) -> Request:  # extract header values from request
    headers = {}
    while True:
        headerLine = readLine(socket)
        if headerLine == b'\r\n':  # check if headers are finished ?
            request.headers = headers
            return request
        headerLine = str(headerLine)
        headerName = headerLine.split(":")[0]
        headerValues = headerLine.split(':')[1:]
        headers[headerName] = headerValues


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:  # same as try catch
    # define socket for server
    serverSocket.bind((SERVER_NAME, SERVER_PORT))
    while True:
        print('listening')  # log
        serverSocket.listen()  # listen for tcp connection
        conn, addr = serverSocket.accept()  # accept connection

        request = getRequestLine(conn)
        request = getRequestHeaders(conn, request)
        try:
            response = Response(request)
            response_string = response.getResponse(conn)
            print(response_string)
            conn.sendall(bytes(response_string, 'ascii'))  # send response
            # conn.sendfile(file)
        except Exception as e:
            conn.sendall(RESPONSE_BAD_REQUEST)
            print(e)
        finally:
            conn.close()
