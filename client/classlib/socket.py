import socket
import json


class Socket:
    """Socket class to handle opening of sockets between the host and client pis"""
    def __init__(self):
        """Sets up the sockets parameters"""
        self.address = ("101.116.1.55", 65000)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Connects to the socket outlined in parameters"""
        self.s.connect(self.address)

    def sendRequest(self, request):
        """Sends a request to the host pi"""
        self.s.sendall(request.encode())

        while True:
            """Statements for decoding the response"""
            data = self.s.recv(4096)
            if data:
                decode = data.decode()
                decode = json.loads(decode)
                if decode["response"] == "200":
                    if "search" in decode:
                        return decode["search"]
                    return True
                elif decode["response"] == "400":
                    if "error" in decode:
                        return decode["error"]
                    return False
            else:
                return True
