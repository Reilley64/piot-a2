from collections import Counter
from datetime import datetime

import mysql.connector


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="35.201.1.71",
            database="librarylms",
            user="root",
        )

    def getAllBooks(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT book.*, bookBorrowed.status FROM book LEFT JOIN bookBorrowed ON bookBorrowed.bookID = book.bookID;")
        return cursor.fetchall()

    def addBook(self, title, author, publishedDate):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO book (title, author, publishedDate) VALUES (%s, %s, %s)",
                       (title, author, publishedDate))
        self.connection.commit()

    def deleteBook(self, bookID):
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
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT book.*, COUNT(bookBorrowed.bookID) as borrowedAmount FROM book LEFT JOIN bookBorrowed ON bookBorrowed.bookID = book.bookID WHERE book.bookID=%s GROUP BY book.bookID;",
            (bookID,))
        return cursor.fetchone()

    def getBookAverageBorrowData(self, bookID):
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
