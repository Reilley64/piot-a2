import json


class Request:
    request = None
    bookID = None
    column = None
    name = None
    query = None
    username = None

    def bookBorrow(self, bookID):
        self.request = "borrow"
        self.bookID = bookID

    def bookReturn(self, bookID):
        self.request = "return"
        self.bookID = bookID

    def bookSearch(self, column, query):
        self.request = "search"
        self.column = column
        self.query = query

    def credentials(self, username, name):
        self.request = "credentials"
        self.username = username
        self.name = name

    def __str__(self):
        if self.request is None:
            return False;

        elif self.request == "credentials":
            returnable = json.dumps({"request": self.request, "username": self.username, "name": self.name})
            return returnable

        elif self.request == "search":
            returnable = json.dumps({"request": self.request, "column": self.column, "query": self.query})
            return returnable

        elif self.request == "borrow":
            returnable = json.dumps({"request": self.request, "id": self.bookID})
            return returnable

        elif self.request == "return":
            returnable = json.dumps({"request": self.request, "id": self.bookID})
            return returnable
