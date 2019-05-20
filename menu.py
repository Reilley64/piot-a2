import dbconnection as dbconnection
import socket
import json

def check_if_user_doesnt_exist(user):
    sql = "SELECT * FROM lmsUser WHERE username = '{}'".format(user)
    result = dbconnection.cloudConnection('GET', sql)
    if(result.length == 1):
        return True
    else: 
        return False

def create_user(user, name):
    sql = "INSERT INTO lmsUser (username, name) VALUES ('{}', '{}')".format(user, name)
    result = dbconnection.cloudConnection('POST', sql)
    return result

def book_unavailable(bookID):
    sql = "select * from bookBorrowed where bookID = {} AND status = \'BORROWED\'".format(bookID)
    db = dbconnection.dbconnection('GET', sql)
    result = db.cloudConnection()
    for r in result:
        if(r['status'] == None or r['status'] == 'RETURNED'):
            return False
        else:
            return True

def borrow_book(user, name, bookID):
    ## get user
    if (check_if_user_doesnt_exist(user)):
        create_user(user, name)
    sql = "SELECT id FROM lmsUser WHERE username = '{}'".format(user)
    userID = dbconnection.cloudConnection('GET', sql)

    if(book_unavailable(bookID)):
        return {"response": "400", "error": "book unavailable"}

    ## update book table
    sql3 = "INSERT INTO bookBorrowed (lmsUserID, bookID, status, borrowDate, returnDate) VALUES ({}, {}, 'BORROWED', NOW(), null)".format(userID,bookID)
    db3 = dbconnection.dbconnection('POST', sql3)
    result = db3.cloudConnection()
    return {"response": "200"}

def return_book(bookID):
    sql = "UPDATE bookBorrowed SET status = \'RETURNED\', returnDate = NOW() WHERE bookID = {} and ".format(bookID)
    db = dbconnection.dbconnection('POST', sql)
    result = db.cloudConnection()
    return {"response": "200"}

def search_book(column, query):
    sql = "SELECT  book.bookID, book.title, book.author, book.publishedDate, borrowed.status FROM book INNER JOIN ( SELECT bookID, status FROM bookBorrowed WHERE status=\'BORROWED\') AS borrowed ON book.bookID = borrowed.bookIDWHERE book.{} LIKE \'%{}%\'".format(column, query)
    print (sql)
    db = dbconnection.dbconnection('GET', sql)
    result = db.cloudConnection()
    print(result)
    formatted = []
    for r in result:
        if(r['status'] == None):
            formatted.append({'title':r['title'],'author':r['author'],'publishedDate':r['publishedDate'].strftime('%Y-%m-%d'), 'status': 'AVAILABLE'})
        else:
            formatted.append({'title':r['title'],'author':r['author'],'publishedDate':r['publishedDate'].strftime('%Y-%m-%d'), 'status': r['status']})
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
            print("yeet")
            data = conn.recv(4096)
            if(data):
                jsondata = json.loads(data.decode())
                print("Received {} bytes of data decoded to: '{}'".format(
                    len(data), data.decode()))
                jsondata = json.loads(data.decode())
                if(jsondata["request"] == 'credentials'):
                    user = jsondata["username"]
                    name = jsondata["name"]
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
                print("Sending data back.")
                conn.sendall(json.dumps(response).encode())
            else:
                break
        print("Disconnecting from client.")
    print("Closing listening socket.")
print("Done.")

    
