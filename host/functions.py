import dbconnection as dbconnection
import time
import datetime
import uuid

class Functions:
    #All basic functions for library system
    def check_if_user_doesnt_exist(user):
        #Checks database for username
        sql = "SELECT * FROM user WHERE username = '{}'".format(user)
        db = dbconnection.dbconnection()
        result = db.cloudConnection('GET', sql)
        if(len(result) == 0):
            return True
        else: 
            return False

    def create_user(user, name):
        #Adds user to database via username and name
        sql = "INSERT INTO user (username, name) VALUES ('{}', '{}')".format(user, name)
        db = dbconnection.dbconnection()
        result = db.cloudConnection('POST', sql)
        return result

    def book_unavailable(bookID):
        #Sets book to borrowed
        sql = "select * from borrow where id = {} AND status = 0".format(bookID)
        db = dbconnection.dbconnection()
        result = db.cloudConnection('GET', sql)
        for r in result:
            print(r['status'])
            if(r['status'] == None or r['status'] == 0):
                return False
            else:
                return True

    def borrow_book(user, bookID):
        #Book borrowing for user via UserID
        sql = "SELECT id FROM user WHERE username = '{}'".format(user)
        db = dbconnection.dbconnection()
        userID = db.cloudConnection('GET', sql)
        if(Functions.book_unavailable(bookID)):
            return {"response": "400", "error": "book unavailable"}
        sql2 = "INSERT INTO borrow (user_id, book_id) VALUES ('{}',{})".format(int(userID[0]['id']),bookID)
        db2 = dbconnection.dbconnection()
        result = db2.cloudConnection('POST', sql2)
        sql3 = "SELECT uuid FROM borrow where user_id = {} and book_id = {} order by borrow_date asc limit 1".format(int(userID[0]['id']),bookID)
        db3 = dbconnection.dbconnection()
        result3 = db.cloudConnection('GET', sql3)
        return {"response": "200", "id": result3[0]['uuid']}

    def return_book(bookID):
        #Return book for user via bookID
        sql1= "select uuid from borrow WHERE book_id={} and status = 0".format(bookID)
        db1 = dbconnection.dbconnection()
        borrowedID = db1.cloudConnection('GET',sql1)
        sql2 = "UPDATE borrow SET status = 1, return_date = CURDATE() WHERE book_id = {} and status = 0 ".format(bookID)
        db2 = dbconnection.dbconnection()
        result = db2.cloudConnection('POST', sql2)
        return {"response": "200", "id": borrowedID[0]['uuid']}

    def search_book(column, query):
        #search for book in database via bookID, book title, book author, book published date and status
        sql = "SELECT book.id, book.title, book.author, book.published_date, borrowed.status FROM book LEFT JOIN ( SELECT book_id, status FROM borrow WHERE status=0) AS borrowed ON book.id = borrowed.book_id WHERE book.{} LIKE \'%{}%\'".format(column, query)
        db = dbconnection.dbconnection()
        result = db.cloudConnection('GET', sql)
        formatted = []
        for r in result:
            if(r['status'] == None):
                formatted.append({'bookID':r['id'],'title':r['title'],'author':r['author'],'publishedDate':r['published_date'].strftime('%Y-%m-%d'), 'status': 'AVAILABLE'})
            else:
                formatted.append({'bookID':r['id'],'title':r['title'],'author':r['author'],'publishedDate':r['published_date'].strftime('%Y-%m-%d'), 'status': 'BORROWED'})
        return formatted