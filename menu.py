import dbconnection  
def print_menu():
    print 30 * "-" , "MENU" , 30 * "-"
    print "1. Seach Book catalogue"
    print "2. Borrow"
    print "3. Return"
    print "4. Logout"
    print 67 * "-"    

def check_if_user_exists(user):
    sql = "select * from lmsUser where username = '{user}'"
    result = dbconnection.cloudConnection('GET', sql)
    if(result.length == 1):
        return True
    else: 
        return False

def create_user(user, name):
    sql = "insert into lmsUser (username, name) values ('{user}', '{name}')"
    result = dbconnection.cloudConnection('POST', sql)


def borrow_book():
    ## get user

    ## get book

    ## update book table
    sql = "insert into bookBorrowed values (1, 1, 1, 'BORROWED', NOW(), null)"


def return_book():
    ## get user

    ## get book

    ## update book

def search_book():
    ## full text serach or like search based on fields.
    ## check assignment


def logout():
    ## send socket back to RP
    
    
  
while true:
    print_menu()
    choice = input("Enter your choice [1-4]: ")
     
    if choice==1:     
        print "search has been selected"
    elif choice==2:
        print "borrow book has been selected"
    elif choice==3:
        print "return book has been selected"
    elif choice==4:
        print "logout has been selected"
        break
    else:
        raw_input("Wrong option selection. Enter any key to try again..")