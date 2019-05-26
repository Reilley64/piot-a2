from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json, requests

api = Blueprint("api", __name__)
db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    published_date = db.Column(db.Date, nullable=False)

    def __init__(self, title, author, published_date):
        self.title = title
        self.author = author
        self.published_date = published_date

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "published_date": self.published_date,
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(256), nullable=False)
    name = db.Column(db.Text, nullable=False)

    def __init__(self, username, name):
        self.username = username
        self.name = name

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
        }


class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.CHAR(32), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    status = db.Column(db.Boolean, nullable=True, default=0)
    borrow_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)

    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id

    def serialize(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "status": self.status,
            "borrow_date": self.borrow_date,
            "return_date": self.return_date,
        }

#API with Flask this is used to talk to Google Cloud database 


#Route to get json object of all book
@api.route("/api/book", methods=["GET"])
def getBooks():
    books = Book.query.all()
    return jsonify([book.serialize() for book in books])

#Route to add json object for a book
@api.route("/api/book", methods=["POST"])
def addBook():
    title = request.json["title"]
    author = request.json["author"]
    published_date = request.json["published_date"]
    book = Book(title, author, published_date)
    db.session.add(book)
    db.session.commit()
    return jsonify(book.serialize())

#Route for that specific book object
@api.route("/api/book/<id>", methods=["GET"])
def getBook(id):
    book = Book.query.get(id)
    return jsonify(book.serialize())

#Route to delete book from the database
@api.route("/api/book/<id>", methods=["DELETE"])
def deleteBook(id):
    response = requests.get("http://127.0.0.1:5000/api/borrow/book_id/" + id)
    borrows = json.loads(response.text)

    if len(borrows) > 0:
        if borrows[len(borrows) - 1]["status"]:
            book = Book.query.get(id)
            for borrow in borrows:
                db.session.delete(Borrow.query.get(borrow["id"]))
            db.session.delete(book)
            db.session.commit()
            return jsonify(book.serialize())
        else:
            return False
    else:
        book = Book.query.get(id)
        db.session.delete(book)
        db.session.commit()
        return jsonify(book.serialize())

#Route to get specific user id
@api.route("/api/user/<id>", methods=["GET"])
def getUser(id):
    user = User.query.get(id)
    return jsonify(user.serialize())

#Route to borrow book by its ID
@api.route("/api/borrow/book_id/<book_id>", methods=["GET"])
def getBorrowsByBookID(book_id):
    borrows = Borrow.query.filter_by(book_id=book_id)
    return jsonify([borrow.serialize() for borrow in borrows])

#Route to find borrowed books
@api.route("/api/borrow", methods=["GET"])
def getBorrows():
    borrows = Borrow.query.all()
    return jsonify([borrow.serialize() for borrow in borrows])

#Route to find borrowed books by date borrowed
@api.route("/api/borrow/borrow_date/<date>", methods=["GET"])
def getBorrowsByBorrowDate(date):
    borrows = Borrow.query.filter_by(borrow_date=date)
    return jsonify([borrow.serialize() for borrow in borrows])

#Route to find borrowed books filtered by their return date
@api.route("/api/borrow/return_date/<date>", methods=["GET"])
def getBorrowsByReturnDate(date):
    borrows = Borrow.query.filter_by(return_date=date)
    return jsonify([borrow.serialize() for borrow in borrows])
