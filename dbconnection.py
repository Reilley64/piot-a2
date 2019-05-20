import pymysql.cursors
import pymysql
import time
from datetime import date

class connection:
    def __init__(self):
        self.pymysql = pymysql

    def connect(self):
        return self.pymysql.connect(user='root',
            password='',
            host='35.201.1.71',
            db='librarylms',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def cloudConnection(self, method, sql):
        connection = self.connect()
        if(method == 'GET'):
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    result = cursor.fetchall()
            finally:
                connection.close
                return result
        elif(method =='POST'):
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    connection.commit
            finally:
                connection.close()
                return 'true'
        else:
            connection.close()
            return 'false'

    