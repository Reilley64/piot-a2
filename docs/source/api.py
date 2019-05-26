class api:
    """The database class initialises and connects to the sql database, grabs all books, adds and delete books for the flask website"""
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="35.201.1.71",
            database="librarylms",
            user="root",
        )

    def getAllBooks(self):
        """Grabs all books from the database to use in graphing"""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT book.*, a.status FROM book LEFT JOIN bookBorrowed a ON a.bookBorrowedID = (SELECT b.bookBorrowedID FROM bookBorrowed AS b WHERE b.bookID = book.bookID ORDER BY b.borrowDate DESC LIMIT 1)")
        return cursor.fetchall()

    def addBook(self, title, author, publishedDate):
        """Adds a book to the database with title author and published date values entered"""
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO book (title, author, publishedDate) VALUES (%s, %s, %s)",
                       (title, author, publishedDate))
        self.connection.commit()

    def deleteBook(self, bookID):
        """Deletes a book from the database based on bookID and if not returned"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT status FROM bookBorrowed WHERE bookID=%s ORDER BY borrowDate DESC;", (bookID,))
        row = cursor.fetchone()
        borrowed = row[0]
        if borrowed == "BORROWED":
            return False
        if borrowed == "RETURNED":
            cursor.execute("DELETE FROM bookBorrowed WHERE bookID=%s;", (bookID,))
            cursor.execute("DELETE FROM book WHERE bookID=%s;", (bookID,))
            self.connection.commit()
            return True

    def getOneBook(self, bookID):
        """Grabs singular book for graphing"""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT book.*, COUNT(bookBorrowed.bookID) as borrowedAmount FROM book LEFT JOIN bookBorrowed ON bookBorrowed.bookID = book.bookID WHERE book.bookID=%s GROUP BY book.bookID;",
            (bookID,))
        return cursor.fetchone()

    def getBookAverageBorrowData(self, bookID):
        """Querys the database for book average borrowed for potential graph data"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT borrowDate FROM bookBorrowed WHERE bookID=%s", (bookID,))
        rows = cursor.fetchall()
        counter = Counter()

        for row in rows:
            if row[0].weekday() == 0:
                counter["monday"] += 1
            elif row[0].weekday() == 1:
                counter["tuesday"] += 1
            elif row[0].weekday() == 2:
                counter["wednesday"] += 1
            elif row[0].weekday() == 3:
                counter["thursday"] += 1
            elif row[0].weekday() == 4:
                counter["friday"] += 1
            elif row[0].weekday() == 5:
                counter["saturday"] += 1
            elif row[0].weekday() == 6:
                counter["sunday"] += 1

        return counter

    def getBorrowedDates(self):
        """Querys the database for borrowed dates of all books for potential graphing"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT borrowDate FROM bookBorrowed ORDER BY borrowDate DESC;")
        rows = cursor.fetchall()
        return rows

    def getReturnedDates(self):
        """Querys the database for returned dates of all books for potential graphing"""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT DISTINCT returnDate FROM bookBorrowed WHERE returnDate IS NOT NULL ORDER BY returnDate DESC;")
        rows = cursor.fetchall()
        return rows

    def getBorrowsByDate(self, date):
        """Querys the database for borrowed dates of all books for potential graphing"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM bookBorrowed WHERE borrowDate=%s;", (date,))
        rows = cursor.fetchall()
        return rows

    def getReturnsByDate(self, date):
        """Querys the database for returned dates of all books for potential graphing"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM bookBorrowed WHERE returnDate=%s;", (date,))
        rows = cursor.fetchall()
        return rows

    def getBorrowedWeeks(self):
        """Querys the database for borrowed dates of all books sorted by weeks for potential graphing"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT YEARWEEK(borrowDate) FROM bookBorrowed ORDER BY YEARWEEK(borrowDate) DESC;")
        rows = cursor.fetchall()
        return rows

    def getReturnedWeeks(self):
        """Querys the database for returned dates of all books sorted by weeks for potential graphing"""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT DISTINCT YEARWEEK(returnDate) FROM bookBorrowed WHERE returnDate IS NOT NULL ORDER BY YEARWEEK(returnDate) DESC;")
        rows = cursor.fetchall()
        return rows

    def getBorrowsByWeek(self, week):
        """Querys the database for borrowed dates of all books sorted by weeks for potential graphing"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM bookBorrowed WHERE YEARWEEK(borrowDate)=%s;", (week,))
        rows = cursor.fetchall()
        return rows

    def getReturnsByWeek(self, week):
        """Querys the database for returned dates of all books sorted by weeks for potential graphing"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM bookBorrowed WHERE YEARWEEK(returnDate)=%s;", (week,))
        rows = cursor.fetchall()
        return rows

    def getAverageBorrowDurationData(self, bookID):
        """Querys the database for borrow duration and averages the data for potential graphing"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT borrowDate, returnDate FROM bookBorrowed WHERE bookID=%s AND returnDate IS NOT NULL;",
                       (bookID,))
        rows = cursor.fetchall()
        y = []
        for row in rows:
            y.append(
                (datetime.combine(row[1], datetime.now().time()) - datetime.combine(row[0],
                                                                                    datetime.now().time())).days)
        return y
