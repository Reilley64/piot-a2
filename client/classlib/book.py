class Book:
    def __init__(self, bookID, title, author, publishedDate, status):
        self.bookID = bookID
        self.title = title
        self.author = author
        self.publishedDate = publishedDate
        self.status = status

    def __str__(self):
        return "ID: %-3s Title: %-50s Author: %-25s Published: %-10s Status: %-9s" % (
            self.id, self.title, self.author, self.publishedDate, self.status)
