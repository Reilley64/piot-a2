from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from classlib.database import Database

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["TEMPLATES_AUTO_RELOAD"] = True

database = Database()
username = None


@app.route("/", methods=["GET", "POST"])
def index():
    global database
    global username

    if request.method == "POST":
        database.addBook(request.form["title"], request.form["author"], request.form["publishedDate"])

        books = database.getAllBooks()
        return render_template("index.html", books=books)
    else:
        if not username:
            return redirect(url_for("login"))
        else:
            books = database.getAllBooks()
            return render_template("index.html", books=books)


@app.route("/login", methods=["GET", "POST"])
def login():
    global username

    if request.method == "POST":
        if request.form["username"] == "jaqen" and request.form["password"] == "hghar":
            username = request.form["username"]
            return redirect(url_for("index"))
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    global username

    username = None
    return redirect(url_for("index"))


@app.route("/book/<bookID>")
def book(bookID):
    global database

    if not username:
        return redirect(url_for("login"))
    else:
        book = database.getOneBook(bookID)
        return render_template("book.html", book=book)
