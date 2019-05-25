import pymysql.cursors
import pymysql

class dbconnection:
    def __init__(self):
        self.pymysql = pymysql

    def connect(self):
        #Connect sql database
        return self.pymysql.connect(user='root',
            password='',
            host='35.201.1.71',
            db='librarylms',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def cloudConnection(self, method, sql):
        #Connect sql database to cloud database
        connection = self.connect()
        if('GET' == method):
            #Gets database results
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
            finally:
                connection.close()
        elif('POST' == method):
            #Sends database results
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    connection.commit()
            finally:
                connection.close()
        else:
            connection.close()
            return 'false'


    