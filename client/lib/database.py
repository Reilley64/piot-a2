import logging
import sqlite3


class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect("dbpath")
        except sqlite3.Error as e:
            logging.basicConfig(filename="db.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s")
            logging.warning(e)

    def login(self, username, password):
        try:
            self.conn.cursor.execute("SELECT * FROM users WHERE username='" + username + "';")
            rows = self.cunn.cursor.fetchall()
        except sqlite3.Error as e:
            return e;

        if rows[0].password == password:
            return username;
        else:
            return False;

    def createUser(self, username, password):
        try:
            self.conn.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?);", (username, password))
        except sqlite3.Error as e:
            return e;
        finally:
            return True;