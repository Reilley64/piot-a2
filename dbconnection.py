import pymysql.cursors
import pymysql
import time
from datetime import date

class dbconnection:
    def __init__(self, method, sql):
        self.pymysql = pymysql
        self.method = method
        self.sql = sql

    def connect(self):
        return self.pymysql.connect(user='root',
            password='',
            host='35.201.1.71',
            db='librarylms',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def cloudConnection(self):
        connection = self.connect()
        if('GET' == self.method):
            try:
                with connection.cursor() as cursor:
                    cursor.execute(self.sql)
                    result = cursor.fetchall()
                    return result
            finally:
                connection.close()
        elif('POST' ==self.method):
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    connection.commit
            finally:
                connection.close()
        else:
            connection.close()
            return 'false'


    