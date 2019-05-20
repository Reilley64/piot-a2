import socket

class Socket:
    def __init__(self):
        self.address = ("101.116.1.55", 65000)

    def receiveMessage(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.address)
            s.listen()
            conn = s.accept()
            with conn:
                message = conn.recv(4096)
                message = message.decode()
                return message

    def sendMessage(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.address)
            s.sendall(message.encode())
            data = s.recv(4096)
            return data;