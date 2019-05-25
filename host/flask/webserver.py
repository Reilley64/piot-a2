import json

import csv
import plotly
import plotly.graph_objs as go
from classlib.database import Database
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_bootstrap import Bootstrap

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
        if request.form["request"] == "add":
            database.addBook(request.form["title"], request.form["author"], request.form["publishedDate"])

        if request.form["request"] == "delete":
            result = database.deleteBook(request.form["bookID"])
            if not result:
                books = database.getAllBooks()
                specificBook = None
                for book in books:
                    if str(book[0]) == request.form["bookID"]:
                        specificBook = book
                error = specificBook[1] + " can not be deleted, it is currently being borrowed"
                return render_template("index.html", books=books, error=error)

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


def averageBorrowDayGraph(bookID):
    global database

    counter = database.getBookAverageBorrowData(bookID)
    data = [
        go.Bar(
            x=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            y=[counter["monday"], counter["tuesday"], counter["wednesday"], counter["thursday"], counter["friday"],
               counter["saturday"], counter["sunday"]]
        )
    ]
    return json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)


@app.route("/book/<bookID>")
def book(bookID):
    global database

    if not username:
        return redirect(url_for("login"))
    else:
        book = database.getOneBook(bookID)
        barGraph = averageBorrowDayGraph(bookID)
        return render_template("book.html", book=book, plot=barGraph)


@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        if request.form["request"] == "borrowsByDate":
            rows = database.getBorrowsByDate(request.form["date"])
            csvData = [["id", "userID", "bookID"]]
            for row in rows:
                csvData.append([row[0], row[1], row[2]])
            with open("pendingReport.csv", "w", newline="") as report:
                writer = csv.writer(report)
                writer.writerows(csvData)
            return send_file("pendingReport.csv", mimetype="text/csv",
                             attachment_filename="borrowsOn" + request.form["date"] + ".csv", as_attachment=True)

        if request.form["request"] == "returnsByDate":
            rows = database.getReturnsByDate(request.form["date"])
            csvData = [["id", "userID", "bookID"]]
            for row in rows:
                csvData.append([row[0], row[1], row[2]])
            with open("pendingReport.csv", "w", newline="") as report:
                writer = csv.writer(report)
                writer.writerows(csvData)
            return send_file("pendingReport.csv", mimetype="text/csv",
                             attachment_filename="returnsOn" + request.form["date"] + ".csv", as_attachment=True)

        if request.form["request"] == "borrowsByWeek":
            rows = database.getBorrowsByWeek(request.form["week"])
            csvData = [["id", "userID", "bookID"]]
            for row in rows:
                csvData.append([row[0], row[1], row[2]])
            with open("pendingReport.csv", "w", newline="") as report:
                writer = csv.writer(report)
                writer.writerows(csvData)
            return send_file("pendingReport.csv", mimetype="text/csv",
                             attachment_filename="returnsIn" + request.form["week"] + ".csv", as_attachment=True)

        if request.form["request"] == "returnsByWeek":
            rows = database.getReturnsByWeek(request.form["week"])
            csvData = [["id", "userID", "bookID"]]
            for row in rows:
                csvData.append([row[0], row[1], row[2]])
            with open("pendingReport.csv", "w", newline="") as report:
                writer = csv.writer(report)
                writer.writerows(csvData)
            return send_file("pendingReport.csv", mimetype="text/csv",
                             attachment_filename="returnsIn" + request.form["week"] + ".csv", as_attachment=True)

    else:
        borrowDates = database.getBorrowedDates()
        returnDates = database.getReturnedDates()
        borrowWeeks = database.getBorrowedWeeks()
        returnWeeks = database.getReturnedWeeks()
        return render_template("report.html", borrowDates=borrowDates, returnDates=returnDates, borrowWeeks=borrowWeeks,
                               returnWeeks=returnWeeks)
