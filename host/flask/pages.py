import csv
import json

import requests
from dateutil import parser
from flask import Blueprint, render_template, url_for, request, redirect, send_file

site = Blueprint("site", __name__)
username = None

#Allows admins with a web interface to delete, add and print reports.

#Route to load Admin suite
@site.route("/", methods=["GET"])
def index():
    if username is None:
        return redirect(url_for("site.login"))
    else:
        response = requests.get("http://127.0.0.1:5000/api/book")
        data = json.loads(response.text)
        return render_template("index.html", books=data)

#Route to render Login page
@site.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

#Route to send login request
@site.route("/login", methods=["POST"])
def doLogin():
    global username

    if request.form["username"] == "jaqen" and request.form["password"] == "hghar":
        username = request.form["username"]
        return redirect(url_for("site.index"))
    else:
        return redirect(url_for("site.login"))

#Route to logout of web interface
@site.route("/logout")
def logout():
    global username

    username = None
    return redirect(url_for("site.login"))

#Route to get book object
@site.route("/", methods=["POST"])
def addBook():
    if request.form["type"] == "add":
        requests.post("http://127.0.0.1:5000/api/book",
                      json={"title": request.form["title"], "author": request.form["author"],
                            "published_date": request.form["published_date"]})

    elif request.form["type"] == "delete":
        response = requests.delete("http://127.0.0.1:5000/api/book/" + request.form["id"])
        if not response:
            response = requests.get("http://127.0.0.1:5000/api/book")
            data = json.loads(response.text)
            return render_template("index.html", books=data,
                                   error="Can not delete that book, it is currently being borrowed")

    return redirect(url_for("site.index"))

#Route 
@site.route("/reports", methods=["GET"])
def reports():
    if username is None:
        return redirect(url_for("site.login"))
    else:
        response = requests.get("http://127.0.0.1:5000/api/borrow")
        borrows = json.loads(response.text)
        borrow_dates = []
        return_dates = []
        for borrow in borrows:
            if parser.parse(borrow["borrow_date"]) not in borrow_dates:
                borrow_dates.append(parser.parse(borrow["borrow_date"]))
            if parser.parse(borrow["return_date"]) not in return_dates:
                return_dates.append(parser.parse(borrow["return_date"]))
        return render_template("report.html", borrow_dates=borrow_dates, return_dates=return_dates)


@site.route("/reports", methods=["POST"])
def downloadReport():
    if request.form["type"] == "borrowsByDate":
        response = requests.get("http://127.0.0.1:5000/api/borrow/borrow_date/" + request.form["date"])
        data = json.loads(response.text)
        csvData = [["id", "userID", "bookID"]]
        for row in data:
            csvData.append([row["uuid"], row["user_id"], row["book_id"]])
        with open("pendingReport.csv", "w", newline="") as report:
            writer = csv.writer(report)
            writer.writerows(csvData)
        return send_file("pendingReport.csv", mimetype="text/csv",
                         attachment_filename="borrowsOn" + request.form["date"] + ".csv", as_attachment=True)

    elif request.form["type"] == "returnsByDate":
        response = requests.get("http://127.0.0.1:5000/api/borrow/return_date/" + request.form["date"])
        data = json.loads(response.text)
        csvData = [["id", "userID", "bookID"]]
        for row in data:
            csvData.append([row["uuid"], row["user_id"], row["book_id"]])
        with open("pendingReport.csv", "w", newline="") as report:
            writer = csv.writer(report)
            writer.writerows(csvData)
        return send_file("pendingReport.csv", mimetype="text/csv",
                         attachment_filename="returnsOn" + request.form["date"] + ".csv", as_attachment=True)
