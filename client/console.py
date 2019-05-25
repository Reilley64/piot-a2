import os

from classlib.database import Database
from classlib.request import Request
from classlib.socket import Socket
from tabulate import tabulate


def printSearchResponse(response):
    responseTable = []
    for book in response:
        responseTable.append([book["bookID"], book["title"], book["author"], book["publishedDate"], book["status"]])

    os.system("clear")
    print(tabulate(responseTable, headers=["ID", "Title", "Author", "Published", "Status"]) + "\n")


def main():
    users = Database()
    host = Socket()
    username = None

    while True:
        print("login | face | logout | signup | connect | exit | help")

        userInput = input("")
        userInput = userInput.split()

        if userInput[0] == "login":
            if len(userInput) is not 3:
                print("Command login takes 2 arguments; example \"login {username} {password}\"\n")
            elif username is None:
                result = users.login(userInput[1], userInput[2])
                if not result:
                    print("Username or password wrong \n")
                else:
                    username = result
                    print("Welcome " + str(username) + "\n")
            else:
                print(username + " is already logged in \n")

        elif userInput[0] == "face":
            if len(userInput) > 1:
                print("Too many arguments for command logout; example \"face\"\n")

        elif userInput[0] == "logout":
            if len(userInput) > 1:
                print("Too many arguments for command logout; example \"logout\"\n")
            elif username is not None:
                username = None
                print("Logged out \n")
            else:
                print("No one to logout \n")

        elif userInput[0] == "signup":
            if len(userInput) is not 6:
                print("Command signup takes 5 arguments; example \"signup {username} {password} {first name} {last "
                      "name} {email}\"\n")
            else:
                result = users.createUser(userInput[1], userInput[2], userInput[3], userInput[4], userInput[5])
                if not result:
                    print("Error creating account: " + result + "\n")
                else:
                    print("Account created \n")

        elif userInput[0] == "connect":
            if len(userInput) > 1:
                print("Too many arguments for command connect; example \"connect\"\n")
            elif username is not None:
                name = users.getName(username)
                print("Connecting...\n")
                host.connect()

                sendable = Request()
                sendable.credentials(username, name)
                response = host.sendRequest(str(sendable))

                if response:
                    while True:
                        print(30 * "-", "MENU", 30 * "-")
                        print("1. Search Book Catalogue")
                        print("2. Borrow")
                        print("3. Return")
                        print("4. Logout")
                        print(66 * "-")

                        userInput = input("")

                        if userInput == "1":
                            print(30 * "-", "SEARCH", 30 * "-")
                            print("1. Title")
                            print("2. Author")
                            print("3. Date")
                            print("4. Back")
                            print(68 * "-")

                            userInput = input("")

                            if userInput == "1":
                                userInput = input("Insert title: ")

                                sendable = Request()
                                sendable.bookSearch("title", userInput)
                                response = host.sendRequest(str(sendable))

                                if not response:
                                    print("Error searching for " + userInput + "\n")
                                    continue

                                printSearchResponse(response)

                            elif userInput == "2":
                                userInput = input("Insert author: ")

                                sendable = Request()
                                sendable.bookSearch("author", userInput)
                                response = host.sendRequest(str(sendable))

                                if not response:
                                    print("Error searching for " + userInput + "\n")
                                    continue

                                printSearchResponse(response)

                            elif userInput == "3":
                                userInput = input("Insert date: ")

                                sendable = Request()
                                sendable.bookSearch("date", userInput)
                                response = host.sendRequest(str(sendable))

                                if not response:
                                    print("Error searching for " + userInput + "\n")
                                    continue

                                printSearchResponse(response)

                            elif userInput == "4":
                                continue

                        elif userInput == "2":
                            userInput = input("Insert id: ")

                            sendable = Request()
                            sendable.bookBorrow(userInput)
                            response = host.sendRequest(str(sendable))

                            if type(response) is str:
                                print("Error borrowing book: " + response + "\n")
                            elif response:
                                print("Book borrowed\n")

                        elif userInput == "3":
                            userInput = input("Insert id: ")

                            sendable = Request()
                            sendable.bookReturn(userInput)
                            response = host.sendRequest(str(sendable))

                            if type(response) is str:
                                print("Error returning book: " + response + "\n")
                            elif response:
                                print("Book returned\n")

                        elif userInput == "4":
                            response = host.sendRequest(None)
                            if response:
                                break
                else:
                    print("Connection failure\n")
            else:
                print("You must login first \n")

        elif userInput[0] == "exit":
            if len(userInput) > 1:
                print("Too many arguments for command exit; example \"exit\"\n")
            else:
                break

        elif userInput[0] == "help":
            print("This is the command console for the Library LMS system\n"
                  "login: Logs into the system; example \"login {username} {password}\"\n"
                  "logout: Logs out of the system; example \"logout\"\n"
                  "signup: Signup to the system; example "
                  "\"signup {username} {password} {first name} {last name} {email}\"\n"
                  "connect: Connects to the master server; example \"connect\"\n"
                  "exit: Exits out of this console; example \"exit\"\n"
                  "help: Shows this\n")

        else:
            print("That command doesn't exist \n")


if __name__ == "__main__":
    main()
