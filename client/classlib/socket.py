import socket
import json


class Socket:
    def __init__(self):
        self.address = ("101.116.1.55", 65000)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.connect(self.address)

    def sendMessage(self, message):
        self.s.sendall(message.encode())

        while True:
            data = self.s.recv(4096)
            if data:
                decode = data.decode()
                decode = json.loads(decode)
                if decode["response"] == "200":
                    if "search" in decode:
                        return decode["search"]
                    return True
                elif decode["response"] == "400":
                    return False
            else:
                return True
