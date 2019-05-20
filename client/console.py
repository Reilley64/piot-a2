from classlib import database
from classlib import socket
from pprint import pprint


def main():
    users = database.Database()
    host = socket.Socket()
    username = None

    while True:
        while True:
            userInput = input("")
            userInput = userInput.split()

            if userInput[0] == "login":
                if len(userInput) is not 3:
                    print("Command login takes 2 arguments")
                elif username is None:
                    result = users.login(userInput[1], userInput[2])
                    if not result:
                        print("Username or password wrong")
                    else:
                        username = result
                        print("Welcome " + str(username))
                else:
                    print(username + " is already logged in")
            elif userInput[0] == "signup":
                if len(userInput) is not 6:
                    print("Command signup takes 5 arguments")
                else:
                    result = users.createUser(userInput[1], userInput[2], userInput[3], userInput[4], userInput[5])
                    if not result:
                        print("Error creating account: " + result)
                    else:
                        print("Account created")
            elif userInput[0] == "connect":
                if len(userInput) > 1:
                    print("Too many arguments for command connect")
                elif username is not None:
                    name = users.getName(username)
                    print("Connecting...")
                    host.sendMessage(username + ", " + name)
                    break
                else:
                    print("You must login first")
            else:
                print("That command doesn't exist")

        while True:
            message = host.receieveMessage()
            if message == "logout":
                print("Logging out...")
                break;


if __name__ == "__main__":
    main()
