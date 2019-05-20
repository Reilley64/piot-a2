import dbconnection as dbconnection
import socket
import json

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

def borrow_book(user, name, bookID):
    ## get user
    sql = "SELECT lmsUserID FROM lmsUser WHERE username = '{}'".format(user)
    db = dbconnection.dbconnection()
    userID = db.cloudConnection('GET', sql)
    print(userID)

    if(book_unavailable(bookID)):
        return {"response": "400", "error": "book unavailable"}
    sql3 = "INSERT INTO bookBorrowed (lmsUserID, bookID, status, borrowDate, returnDate) VALUES ({}, {}, 'BORROWED', CURDATE(), null)".format(int(userID[0]['lmsUserID']),bookID)
    print(sql3)
    db3 = dbconnection.dbconnection()
    result = db3.cloudConnection('POST', sql3)
    return {"response": "200"}

def return_book(bookID):
    sql4 = "UPDATE bookBorrowed SET status = \'RETURNED\', returnDate = CURDATE() WHERE bookID = {} and status = \'BORROWED\' ".format(bookID)
    print(sql4)
    db3 = dbconnection.dbconnection()
    result = db3.cloudConnection('POST', sql4)
    return {"response": "200"}

def search_book(column, query):
    sql = "SELECT book.bookID, book.title, book.author, book.publishedDate, borrowed.status FROM book LEFT JOIN ( SELECT bookID, status FROM bookBorrowed WHERE status=\'BORROWED\') AS borrowed ON book.bookID = borrowed.bookID WHERE book.{} LIKE \'%{}%\'".format(column, query)
    print (sql)
    db = dbconnection.dbconnection()
    result = db.cloudConnection('GET', sql)
    print(result)
    formatted = []
    for r in result:
        if(r['status'] == None):
            formatted.append({'bookID':r['bookID'],'title':r['title'],'author':r['author'],'publishedDate':r['publishedDate'].strftime('%Y-%m-%d'), 'status': 'AVAILABLE'})
        else:
            formatted.append({'bookID':r['bookID'],'title':r['title'],'author':r['author'],'publishedDate':r['publishedDate'].strftime('%Y-%m-%d'), 'status': r['status']})
    return formatted

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 65000 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)
user = ""
name = ""
response = ""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(ADDRESS)
    s.listen()

    print("Listening on {}...".format(ADDRESS))
    conn, addr = s.accept()
    with conn:
        print("Connected to {}".format(addr))
        connection = True
        while connection:
            data = conn.recv(4096)
            if(data):
                jsondata = json.loads(data.decode())
                print("Received {} bytes of data decoded to: '{}'".format(
                    len(data), data.decode()))
                jsondata = json.loads(data.decode())
                if(jsondata["request"] == 'credentials'):
                    user = jsondata["username"]
                    name = jsondata["name"]
                    if (check_if_user_doesnt_exist(user)):
                        create_user(user, name)
                    response = {"response": "200"}
                if(jsondata["request"] == 'logout'):
                    connection = False
                    response = {"response": "200"}
                if(jsondata["request"] == 'search'):
                    column = jsondata["column"]
                    query = jsondata["query"]
                    result = search_book(column, query)
                    print(result)
                    response = {"response": "200", "search": result}
                if(jsondata["request"] == 'borrow'):
                    bookID = jsondata['id']
                    response = borrow_book(user, name, bookID)
                if(jsondata['request'] == 'return'):
                    bookID = jsondata['id']
                    response = return_book(bookID)
                print("Sending data back.")
                conn.sendall(json.dumps(response).encode())
            else:
                break
        print("Disconnecting from client.")
    print("Closing listening socket.")
print("Done.")

    
