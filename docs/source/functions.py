class Functions:
    def check_if_user_doesnt_exist(user):
        sql = "SELECT * FROM lmsUser WHERE username = '{}'".format(user)
        db = dbconnection.dbconnection()
        result = db.cloudConnection('GET', sql)
        if(len(result) == 0):
            return True
        else: 
            return False

    def create_user(user, name):
        sql = "INSERT INTO lmsUser (username, name) VALUES ('{}', '{}')".format(user, name)
        db = dbconnection.dbconnection()
        result = db.cloudConnection('POST', sql)
        return result

    def book_unavailable(bookID):
        sql = "select * from bookBorrowed where bookID = {} AND status = \'BORROWED\'".format(bookID)
        db = dbconnection.dbconnection()
        result = db.cloudConnection('GET', sql)
        for r in result:
            if(r['status'] == None or r['status'] == 'RETURNED'):
                return False
            else:
                return True

    def borrow_book(user, bookID):
        sql = "SELECT lmsUserID FROM lmsUser WHERE username = '{}'".format(user)
        db = dbconnection.dbconnection()
        userID = db.cloudConnection('GET', sql)
        if(Functions.book_unavailable(bookID)):
            return {"response": "400", "error": "book unavailable"}
        key = str(uuid.uuid4()).replace("-","")
        sql2 = "INSERT INTO bookBorrowed (bookBorrowedID,lmsUserID, bookID, status, borrowDate, returnDate) VALUES ('{}',{}, {}, 'BORROWED', CURDATE(), null)".format(key,int(userID[0]['lmsUserID']),bookID)
        db2 = dbconnection.dbconnection()
        result = db2.cloudConnection('POST', sql2)
        return {"response": "200", "id": key}

    def return_book(bookID):
        sql1= "select bookBorrowedID from bookBorrowed WHERE bookID={} and status = \'BORROWED\'".format(bookID)
        db1 = dbconnection.dbconnection()
        borrowedID = db1.cloudConnection('GET',sql1)
        sql2 = "UPDATE bookBorrowed SET status = \'RETURNED\', returnDate = CURDATE() WHERE bookID = {} and status = \'BORROWED\' ".format(bookID)
        db2 = dbconnection.dbconnection()
        result = db2.cloudConnection('POST', sql2)
        return {"response": "200", "id": borrowedID[0]['bookBorrowedID']}

    def search_book(column, query):
        sql = "SELECT book.bookID, book.title, book.author, book.publishedDate, borrowed.status FROM book LEFT JOIN ( SELECT bookID, status FROM bookBorrowed WHERE status=\'BORROWED\') AS borrowed ON book.bookID = borrowed.bookID WHERE book.{} LIKE \'%{}%\'".format(column, query)
        db = dbconnection.dbconnection()
        result = db.cloudConnection('GET', sql)
        formatted = []
        for r in result:
            if(r['status'] == None):
                formatted.append({'bookID':r['bookID'],'title':r['title'],'author':r['author'],'publishedDate':r['publishedDate'].strftime('%Y-%m-%d'), 'status': 'AVAILABLE'})
            else:
                formatted.append({'bookID':r['bookID'],'title':r['title'],'author':r['author'],'publishedDate':r['publishedDate'].strftime('%Y-%m-%d'), 'status': r['status']})
        return formatted