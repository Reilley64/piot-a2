from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["TEMPLATES_AUTO_RELOAD"] = True

username = None


@app.route("/")
def index():
    global username

    if not username:
        return redirect(url_for("login"))
    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    global username

    if request.method == "POST":
        if request.form["username"] == "jaqen" and request.form["password"] == "hghar":
            username = "jaqen"
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login"))
    else:
        return render_template("login.html")
