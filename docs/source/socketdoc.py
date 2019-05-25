class SocketDoc:
    """The Socket class connects with the host pi and sends request between eachother"""
    def __init__(self):
        self.address = ("101.116.1.55", 65000)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Connects the pi to the other pi"""
        self.s.connect(self.address)

    def sendRequest(self, request):
        """Sends a request for data to the other pi"""
        self.s.sendall(request.encode())

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
                    if "error" in decode:
                        return decode["error"]
                    return False
            else:
                return True
