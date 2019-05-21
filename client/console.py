from classlib.database import Database
from classlib.request import Request
from classlib.socket import Socket
from tabulate import tabulate


def printSearchResponse(response):
    responseTable = []
    for book in response:
        responseTable.append([book["id"], book["title"], book["author"], book["publishedDate"], book["status"]])
    print(tabulate(responseTable, headers=["ID", "Title", "Author", "Published", "Status"]))


def main():
    users = Database()
    host = Socket()
    username = None

    while True:
        print("login | logout | signup | connect | exit")

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

        elif userInput[0] == "logout":
            if len(userInput) > 1:
                print("Too many arguments for command connect")
            elif username is not None:
                username = None
                print("Logged out")
            else:
                print("No one to logout")

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
                host.connect()

                sendable = Request()
                sendable.credentials(username, name)
                response = host.sendRequest(sendable.send)

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
                                response = host.sendRequest(sendable.send)

                                if not response:
                                    print("Error searching for " + userInput)
                                    continue

                                printSearchResponse(response)

                            elif userInput == "2":
                                userInput = input("Insert author: ")

                                sendable = Request()
                                sendable.bookSearch("author", userInput)
                                response = host.sendRequest(sendable.send)

                                if not response:
                                    print("Error searching for " + userInput)
                                    continue

                                printSearchResponse(response)

                            elif userInput == "3":
                                userInput = input("Insert date: ")

                                sendable = Request()
                                sendable.bookSearch("date", userInput)
                                response = host.sendRequest(sendable.send)

                                if not response:
                                    print("Error searching for " + userInput)
                                    continue

                                printSearchResponse(response)

                            elif userInput == "4":
                                continue

                        elif userInput == "2":
                            userInput = input("Insert id: ")

                            sendable = Request()
                            sendable.bookBorrow(userInput)
                            response = host.sendRequest(sendable.send)

                            if type(response) is str:
                                print("Error borrowing book: " + response)
                            elif response:
                                print("Book borrowed")

                        elif userInput == "3":
                            userInput = input("Insert id: ")

                            sendable = Request()
                            sendable.bookReturn(userInput)
                            response = host.sendRequest(sendable.send)

                            if type(response) is str:
                                print("Error returning book: " + response)
                            elif response:
                                print("Book returned")

                        elif userInput == "4":
                            response = host.sendRequest(None)
                            if response:
                                break
                else:
                    print("Connection failure")
            else:
                print("You must login first")

        elif userInput[0] == "exit":
            break

        else:
            print("That command doesn't exist")


if __name__ == "__main__":
    main()
