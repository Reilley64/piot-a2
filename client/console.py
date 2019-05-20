from lib.database import database
from pprint import pprint


def main():
    database = Database()
    username = None

    while True:
        while True:
            input = input()
            input = input.split()

            if input[0] is "login":
                if len(input) is not 3:
                    print("Command login takes 2 arguments")
                elif username is None:
                    result = database.login(input[1], input[2])
                    if not result:
                        print("Username or password wrong")
                    else:
                        result = result.split()
                        if len(result) > 1:
                            print("Error logging in: ")
                            pprint(result)
                        else:
                            username = result
                            print("Welcome " + username)
                else:
                    print(username + " is already logged in")

            if input[0] is "signup":
                if len(input) is not 6:
                    print("Command signup takes 5 arguments")
                else:
                    result = database.create(input[1], input[2], input[3], input[4])
                    if not result:
                        print("Error creating account: " + result)
                    else:
                        print("Account created")

            if input[0] == "connect":
                if len(input) > 1:
                    print("Too many arguments for command connect")
                elif username is not None:
                    # TODO: Send username to master pi
                    break
                else:
                    print("You must login first")

        # while True:
        #     # TODO: Wait for logout message
        #     if (logout):
        #         username = None;
        #         break;


if __name__ == "__main__":
    main()
