import socket

class connectClient:
    def __init__(self):
        self.address = ("", 65000)

    def receiveMessage(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.address)
            s.listen()
            conn, addr = s.accept()
            print ('got connection from ', conn)
            with conn:
                while True:
                    message = conn.recv(4096)
                    data = 'a'.encode()
                    print('a')
                    conn.sendall(data)
                    print('n')
                    return message.decode()

    def sendMessage(self, address, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.address)
            s.sendall(message.encode())
            data = s.recv(4096)
            return data;