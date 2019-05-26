class dbconnection:
    """This is the dbconnection class for the cloud connection."""
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
        """Connect to the cloud database. If Get then fetch all results. If POST then send all results.

        :param self: Initiates the pymysql
        
        :param method: Used for POST AND GET of sql fetches and commits

        :param sql: sql database connection
        """
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


    