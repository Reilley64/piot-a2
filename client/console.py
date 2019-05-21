from classlib import database
from classlib import socket
import json


def main():
    users = database.Database()
    host = socket.Socket()
    username = None

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
                host.connect()

                message = json.dumps({"request": "credentials", "username": username, "name": name})
                response = host.sendMessage(message)

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

                                message = json.dumps({"request": "search", "column": "title", "query": userInput})
                                response = host.sendMessage(message)

                                if not response:
                                    print("Error searching for " + userInput)
                                    continue

                                for book in response:
                                    print("ID: %-3s Title: %-50s Author: %-25s Published: %-10s Status: %-9s" % (
                                        book["id"], book["title"], book["author"], book["publishedDate"],
                                        book["status"]))

                            elif userInput == "2":
                                userInput = input("Insert author: ")

                                message = json.dumps({"request": "search", "column": "author", "query": userInput})
                                response = host.sendMessage(message)

                                if not response:
                                    print("Error searching for " + userInput)
                                    continue

                                for book in response:
                                    print("ID: %-3s Title: %-50s Author: %-25s Published: %-10s Status: %-9s" % (
                                        book["id"], book["title"], book["author"], book["publishedDate"],
                                        book["status"]))

                            elif userInput == "3":
                                userInput = input("Insert date: ")

                                message = json.dumps({"request": "search", "column": "date", "query": userInput})
                                response = host.sendMessage(message)

                                if not response:
                                    print("Error searching for " + userInput)
                                    continue

                                for book in response:
                                    print("ID: %-3s Title: %-50s Author: %-25s Published: %-10s Status: %-9s" % (
                                        book["id"], book["title"], book["author"], book["publishedDate"],
                                        book["status"]))

                            elif userInput == "4":
                                continue

                        elif userInput == "2":
                            userInput = input("Insert id: ")

                            message = json.dumps({"request": "borrow", "id": userInput})
                            response = host.sendMessage(message)

                            if type(response) is str:
                                print("Error borrowing book: " + response)
                            elif response:
                                print("Book borrowed")


                        elif userInput == "3":
                            userInput = input("Insert id: ")

                            message = json.dumps({"request": "return", "id": userInput})
                            response = host.sendMessage(message)

                            if type(response) is str:
                                print("Error returning book: " + response)
                            elif response:
                                print("Book returned")

                        elif userInput == "4":
                            response = host.sendMessage(None)
                            if response:
                                break
                else:
                    print("Connection failure")
            else:
                print("You must login first")
        else:
            print("That command doesn't exist")


if __name__ == "__main__":
    main()
