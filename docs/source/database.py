class Database:
    """The database class initialises the sql database, creates a user, gets the username, name and logs in an existing user"""
    def __init__(self):
        try:
            self.connection = sqlite3.connect("database/sqlite.db")
        except sqlite3.Error as e:
            logging.basicConfig(filename="db.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s")
            logging.warning(e)

    def createUser(self, username, password, firstName, lastName, email):
        """Registers a user using a username, password, firstName, lastName and email and inserts the user into the database
        
        :param self: for connection to sql database connection
        
        :param username: Registered users user name

        :param password: Password entered and hashed

        :param firstName: First name of registered user

        :param lastName: Last name of registered user

        :param email: Email of registered user
        """
        passwordHash = pbkdf2_sha256.hash(password)

        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users (username, password, firstName, lastName, email) VALUES (?, ?, ?, ?, ?);",
                           (username, passwordHash, firstName, lastName, email))
        except sqlite3.Error as e:
            return e

        self.connection.commit()
        return True

    def getName(self, username):
        """Gets the user from the database for the login"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT firstName FROM users WHERE username=?;", (username,))
            rows = cursor.fetchone()
        except sqlite3.Error as e:
            return e

        return rows[0]

    def login(self, username, password):
        """Logs in the user using a username and password"""
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
