import json


class Request:
    """Request class to handle interactions with host pi"""
    request = None
    bookID = None
    column = None
    name = None
    query = None
    username = None

    def bookBorrow(self, bookID):
        """Defines the request as a book borrow"""
        self.request = "borrow"
        self.bookID = bookID

    def bookReturn(self, bookID):
        """Defines the request as a book return"""
        self.request = "return"
        self.bookID = bookID

    def bookSearch(self, column, query):
        """Defines the request as a book search"""
        self.request = "search"
        self.column = column
        self.query = query

    def credentials(self, username, name):
        """Defines the request as credentials"""
        self.request = "credentials"
        self.username = username
        self.name = name

    def __str__(self):
        """Handles turning the class into a JSON String for sending to host pi"""
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
