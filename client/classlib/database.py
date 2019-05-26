from passlib.hash import pbkdf2_sha256
import logging
import sqlite3


class Database:
    """Database Class for talking with SQLITE database"""
    def __init__(self):
        """Initialize the database connection"""
        try:
            self.connection = sqlite3.connect("database/sqlite.db")
        except sqlite3.Error as e:
            logging.basicConfig(filename="db.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s")
            logging.warning(e)

    def createUser(self, username, password, firstName, lastName, email):
        """Creates a user in the user table"""
        passwordHash = pbkdf2_sha256.hash(password)
        """Password hashing"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users (username, password, firstName, lastName, email) VALUES (?, ?, ?, ?, ?);",
                           (username, passwordHash, firstName, lastName, email))
        except sqlite3.Error as e:
            return e

        self.connection.commit()
        return True

    def getName(self, username):
        """Gets a user based on their username"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT firstName FROM users WHERE username=?;", (username,))
            rows = cursor.fetchone()
        except sqlite3.Error as e:
            return e

        return rows[0]

    def login(self, username, password):
        """Test username and password to see if they match the database"""
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
