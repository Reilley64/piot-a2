import dbconnection  
def print_menu():
    print 30 * "-" , "MENU" , 30 * "-"
    print "1. Seach Book catalogue"
    print "2. Borrow"
    print "3. Return"
    print "4. Logout"
    print 67 * "-"
  
loop=True      
  
while loop:
    print_menu()
    choice = input("Enter your choice [1-4]: ")
     
    if choice==1:     
        print "search has been selected"
    elif choice==2:
        print "borrow book has been selected"
        ## You can add your code or functions here
    elif choice==3:
        print "return book has been selected"
        ## You can add your code or functions here
    elif choice==4:
        print "logout has been selected"
        loop=False 
    else:
        raw_input("Wrong option selection. Enter any key to try again..")