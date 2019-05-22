import mysql.connector


class Database():
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="35.201.1.71",
            database="librarylms",
            user="root",
        )

    def getAllBooks(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM book;")
        return cursor.fetchall()

    def addBook(self, title, author, publishedDate):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO book (title, author, publishedDate) VALUES (%s, %s, %s)",
                       (title, author, publishedDate))
        self.connection.commit()

    def removeBook(self, bookID):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM book WHERE bookID=%s", (bookID,))
        self.connection.commit()

    def getOneBook(self, bookID):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM book WHERE bookID=%s;", (bookID,))
        return cursor.fetchone()
