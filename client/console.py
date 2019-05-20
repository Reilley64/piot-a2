from lib.database import database
from pprint import pprint

def main():
    database = Database()
    username = None;

    while True:
        input = input()
        input = input.split()

        if input[0] == "login":
            if len(input) != 3:
                print("Wrong number of arguments")
            if username is None:
                result = database.login(input[1], input[2])
                if not result:
                    print("Username or password wrong")
                else:
                    result = result.split()
                    if len(result) > 1:
                        print("Error logging in: ")
                        pprint(result)
                    else:
                        username = result[0]
                        print("Welcome " + username)
            else:
                print("You are already logged in")

if __name__ == "__main__":
    main()