from passlib.hash import pbkdf2_sha256
import logging
import sqlite3


class Database: 
    #User database setup
    def __init__(self): 
        #Sql Database initialisation
        try:
            self.connection = sqlite3.connect("database/sqlite.db")
        except sqlite3.Error as e:
            logging.basicConfig(filename="db.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s")
            logging.warning(e)

    def createUser(self, username, password, firstName, lastName, email):
        passwordHash = pbkdf2_sha256.hash(password)
        #Password hashing for privacy and user creation via insert into details below
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users (username, password, firstName, lastName, email) VALUES (?, ?, ?, ?, ?);",
                           (username, passwordHash, firstName, lastName, email))
        except sqlite3.Error as e:
            return e

        self.connection.commit()
        return True

    def getName(self, username):
        #Getting user
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT firstName FROM users WHERE username=?;", (username,))
            rows = cursor.fetchone()
        except sqlite3.Error as e:
            return e

        return rows[0]

    def login(self, username, password):
        #Logging in user via username and password in database
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT username, password FROM users WHERE username=?;", (username,))
            rows = cursor.fetchone()
        except sqlite3.Error as e:
            return e

        if not rows:
            return False

        if pbkdf2_sha256.verify(password, rows[1]):
            return rows[0]
        else:
            return False
