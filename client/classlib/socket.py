import socket
import json


class Socket:
    #Socketing between client and host pi's
    def __init__(self):
        #Initialize socket
        self.address = ("101.116.1.55", 65000)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.connect(self.address)

    def sendRequest(self, request):
        self.s.sendall(request.encode())

        while True:
            #If statements for decoding
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
