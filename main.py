import socket
import json
import functions as Functions
import calendar as Calendar
import datetime

class Main():
    def __init__(self):
        self.HOST = ""
        self.PORT = 65000 
        self.ADDRESS = (HOST, PORT)
        self.user = ""
        self.name = ""
        self.response = ""

    def listener(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.ADDRESS)
            s.listen()
            print("Listening on {}...".format(ADDRESS))
            conn, addr = s.accept()
            with conn:
                print("Connected to {}".format(addr))
                connection = True
                while connection:
                    data = conn.recv(4096)
                    if(data):
                        jsondata = json.loads(data.decode())
                        print("Received {} bytes of data decoded to: '{}'".format(
                            len(data), data.decode()))
                        jsondata = json.loads(data.decode())
                        if(jsondata["request"] == 'credentials'):
                            self.user = jsondata["username"]
                            self.name = jsondata["name"]
                            if (Functions.check_if_user_doesnt_exist(self.user)):
                                Functions.create_user(self.user, self.name)
                            response = {"response": "200"}
                        if(jsondata["request"] == 'logout'):
                            connection = False
                            response = {"response": "200"}
                        if(jsondata["request"] == 'search'):
                            column = jsondata["column"]
                            query = jsondata["query"]
                            result = Functions.search_book(column, query)
                            print(result)
                            response = {"response": "200", "search": result}
                        if(jsondata["request"] == 'borrow'):
                            bookID = jsondata['id']
                            response = Functions.borrow_book(self.user, bookID)
                            if(response['response'] == "200"):
                                summary = 'ID: {} BORROWED BY: {}'.format(bookID, self.user)
                                now = datetime.datetime.now()
                                due_date = now + datetime.timedelta(days=7)
                                description = 'return by this day: {}'.format(due_date.strftime('%Y-%m-%d'))
                                Calendar.GoogleCalendar().borrow_book(due_date.strftime('%Y-%m-%d'),summary, description)
                        if(jsondata['request'] == 'return'):
                            bookID = jsondata['id']
                            Calendar.GoogleCalendar().return_book(bookID)
                            response = Functions.return_book(bookID)
                        print("Sending response.")
                        conn.sendall(json.dumps(response).encode())
                    else:
                        break
                print("Disconnecting from client.")
            print("Closing listening socket.")
        print("Done.")

if __name__ == '__main__':
    Main().listener()    
