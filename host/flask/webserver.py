import os

from api import api, db
from flask import Flask
from pages import site
from flask_bootstrap import Bootstrap

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

bootstrap = Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@35.201.1.71/librarylms"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
db.init_app(app)

app.register_blueprint(api)
app.register_blueprint(site)
