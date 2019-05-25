class dbconnection:
    """The Main class initiates and connects the sql library, and establishes a cloud db connection"""
    def __init__(self):
        self.pymysql = pymysql

    def connect(self):
        """Connect to the sql database."""
        return self.pymysql.connect(user='root',
            password='',
            host='35.201.1.71',
            db='librarylms',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def cloudConnection(self, method, sql):
        """Connect to the cloud database. If Get then fetch all results. If POST then send all results."""
        connection = self.connect()
        if('GET' == method):
            
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
            finally:
                connection.close()
        elif('POST' == method):
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    connection.commit()
            finally:
                connection.close()
        else:
            connection.close()
            return 'false'


    