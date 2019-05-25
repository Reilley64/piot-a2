class Request:
    """The request class requests all the library features form the database such as borrow, search, return and user credentials"""
    request = None
    bookID = None
    column = None
    name = None
    query = None
    username = None

    def bookBorrow(self, bookID):
        """Borrow book function with request for bookID"""
        self.request = "borrow"
        self.bookID = bookID

    def bookReturn(self, bookID):
        """Return book function with request for bookID"""
        self.request = "return"
        self.bookID = bookID

    def bookSearch(self, column, query):
        """Search book function with request for column and query"""
        self.request = "search"
        self.column = column
        self.query = query

    def credentials(self, username, name):
        """Request for user credentials including Username and name"""
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
