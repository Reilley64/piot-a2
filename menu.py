import dbconnection  
def print_menu():
    print 30 * "-" , "MENU" , 30 * "-"
    print "1. Seach Book catalogue"
    print "2. Borrow"
    print "3. Return"
    print "4. Logout"
    print 67 * "-"

def print_search():
    print 30 * "-" , "Search By" , 30 * "-"
    print "1. Title"
    print "2. Author"
    print "3. Date"
    print "4. Back"
    print 67 * "-"
        

def check_if_user_doesnt_exist(user):
    sql = "select * from lmsUser where username = '{user}'"
    result = dbconnection.cloudConnection('GET', sql)
    if(result.length == 1):
        return True
    else: 
        return False

def create_user(user, name):
    sql = "insert into lmsUser (username, name) values ('{user}', '{name}')"
    result = dbconnection.cloudConnection('POST', sql)
    return result


def borrow_book(user, name, bookTitle):
    ## get user
    if (check_if_user_doesnt_exist(user)):
        create_user(user, name)
    sql = "select id from lmsUser where username = '{user}'"
    userID = dbconnection.cloudConnection('GET', sql)
    ## get book
    sql2 = "select id from book where title = {bookTitle}"
    bookID = dbconnection.cloudConnection('GET', sql2)

    ## update book table
    sql3 = "insert into bookBorrowed values (1, 1, {bookID}, 'BORROWED', NOW(), null)"
    result = dbconnection.cloudConnection('POST', sql3)

def return_book(bookTitle):
    ## get book
    sql1 = "select id from book where title = {bookTitle}"
    bookID = dbconnection.cloudConnection('GET', sql1)
    ## update book
    sql2 = "update bookBorrowed set status = 'RETURNED', returnDate = NOW() where bookID = {bookID} "
    result = dbconnection.cloudConnection('POST', sql2)

def search_book(column, query):
    sql = "SELECT * FROM book WHERE {column} LIKE '%{query}%'"
    result = dbconnection.cloudConnection('GET', sql)
    return result

def logout():
    ## send socket back to RP
    
    
  
while true:
    print_menu()
    choice = input("Enter your choice [1-4]: ")
     
    if choice==1:     
        print "search has been selected"
        while true:
            print_search()
            search = input("Enter your choice [1-4]: ")
            if search == 1:
                print "search by title selected"
                query = input("Enter your search for title")
                search_book('title', query)
            elif search == 2:
                print "search by author selected"
                query = input("Enter your search for author")
                search_book('author', query)
            elif search == 3:
                print "search by date selected"
                query = input("Enter your search for date")
                search_book('date', query)
            elif search == 4:
                break
                print "back selected"
            else:
                raw_input("Wrong option selection. Enter any key to try again..")
    elif choice==2:
        print "borrow book has been selected"
    elif choice==3:
        print "return book has been selected"
    elif choice==4:
        print "logout has been selected"
        break
    else:
        raw_input("Wrong option selection. Enter any key to try again..")