import os

from classlib.database import Database
from classlib.request import Request
from classlib.socket import Socket
from tabulate import tabulate
from opencv.recognise import Recognise
import textwrap
import speech_recognition as sr


def printSearchResponse(response):
    """Organizes the response in a tabulate table, clears the console, and then prints it"""
    responseTable = []
    for book in response:
        title = textwrap.shorten(book["title"], width=30)
        responseTable.append([book["bookID"], title, book["author"], book["publishedDate"], book["status"]])

    os.system("clear")
    print(tabulate(responseTable, headers=["ID", "Title", "Author", "Published", "Status"]) + "\n")


def main():
    """Console interface for the Pi"""
    users = Database()
    host = Socket()
    username = None

    while True:
        print("login | face | logout | signup | connect | exit | help")
        """Home Screen"""
        userInput = input("")
        userInput = userInput.split()

        if userInput[0] == "login":
            """Login handling"""
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
            if len(userInput) != 2:
                print("Command face takes 2 arguments; example \"face {username}\"\n")
            elif username is None:
                print(userInput[1])
                result = Recognise().run(userInput[1])
                if not result:
                    print("Failed to verify you please try again\n")
                else:
                    username = result
                    print("Welcome " + str(username) + "\n")
            else:
                print(username + " is already logged in\n")

        elif userInput[0] == "logout":
            """Logout handling"""
            if len(userInput) > 1:
                print("Too many arguments for command logout; example \"logout\"\n")
            elif username is not None:
                username = None
                print("Logged out \n")
            else:
                print("No one to logout \n")

        elif userInput[0] == "signup":
            """Signup handling"""
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
            """Connect handling"""
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
                        """Interface after connected to host pi"""
                        print(30 * "-", "MENU", 30 * "-")
                        print("1. Search Book Catalogue")
                        print("2. Borrow")
                        print("3. Return")
                        print("4. Voice")
                        print("5. Logout")
                        print(66 * "-")

                        userInput = input("")

                        if userInput == "1":
                            """Book search interface"""
                            print(30 * "-", "SEARCH", 30 * "-")
                            print("1. Title")
                            print("2. Author")
                            print("3. Date")
                            print("4. Back")
                            print(68 * "-")

                            userInput = input("")

                            if userInput == "1":
                                """Title handling"""
                                userInput = input("Insert title: ")

                                sendable = Request()
                                sendable.bookSearch("title", userInput)
                                response = host.sendRequest(str(sendable))

                                if not response:
                                    print("Error searching for " + userInput + "\n")
                                    continue

                                printSearchResponse(response)

                            elif userInput == "2":
                                """Author handling"""
                                userInput = input("Insert author: ")

                                sendable = Request()
                                sendable.bookSearch("author", userInput)
                                response = host.sendRequest(str(sendable))

                                if not response:
                                    print("Error searching for " + userInput + "\n")
                                    continue

                                printSearchResponse(response)

                            elif userInput == "3":
                                """Date handling"""
                                userInput = input("Insert date: ")

                                sendable = Request()
                                sendable.bookSearch("date", userInput)
                                response = host.sendRequest(str(sendable))

                                if not response:
                                    print("Error searching for " + userInput + "\n")
                                    continue

                                printSearchResponse(response)

                            elif userInput == "4":
                                """Bank handling"""
                                continue

                        elif userInput == "2":
                            """Borrowing interface"""
                            userInput = input("Insert id: ")

                            sendable = Request()
                            sendable.bookBorrow(userInput)
                            response = host.sendRequest(str(sendable))

                            if type(response) is str:
                                print("Error borrowing book: " + response + "\n")
                            elif response:
                                print("Book borrowed\n")

                        elif userInput == "3":
                            """Returning interface"""
                            userInput = input("Insert id: ")

                            sendable = Request()
                            sendable.bookReturn(userInput)
                            response = host.sendRequest(str(sendable))

                            if type(response) is str:
                                print("Error returning book: " + response + "\n")
                            elif response:
                                print("Book returned\n")

                        elif userInput == "4":
                            MIC_NAME = "Microsoft® LifeCam HD-3000: USB Audio (hw:1,0)"
                            for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
                                if microphone_name == MIC_NAME:
                                    device_id = i
                                    break
                            r = sr.Recognizer()
                            with sr.Microphone(device_index=device_id) as source:
                                r.adjust_for_ambient_noise(source)
                                print("Say something")
                                while True:
                                    try:
                                        audio = r.listen(source, timeout=1.5)
                                    except sr.WaitTimeoutError:
                                        print("Listening timed out whilst waiting for phrase to start")
                                        quit()
                                    print("You said: " + r.recognize_google(audio))
                                    userInput = input("Correct? (Y/N)")
                                    if userInput == "Y":
                                        break
                                    else:
                                        continue
                                voiceTokens = r.recognize_google.split()

                                if voiceTokens[0] == "search":
                                    if len(voiceTokens) == 3:
                                        sendable = Request()
                                        sendable.bookSearch(voiceTokens[1], voiceTokens[2])
                                        response = host.sendRequest(str(sendable))

                                        if not response:
                                            print("Error searching for " + userInput + "\n")
                                            continue

                                        printSearchResponse(response)
                                    else:
                                        continue

                                if voiceTokens[0] == "borrow":
                                    if len(voiceTokens) == 2:
                                        sendable = Request()
                                        sendable.bookBorrow(voiceTokens[1])
                                        response = host.sendRequest(str(sendable))

                                        if type(response) is str:
                                            print("Error borrowing book: " + response + "\n")
                                        elif response:
                                            print("Book borrowed\n")

                                if voiceTokens[0] == "return":
                                    if len(voiceTokens) == 2:
                                        sendable = Request()
                                        sendable.bookReturn(voiceTokens[1])
                                        response = host.sendRequest(str(sendable))

                                        if type(response) is str:
                                            print("Error returning book: " + response + "\n")
                                        elif response:
                                            print("Book borrowed\n")

                        elif userInput == "5":
                            response = host.sendRequest(None)
                            if response:
                                break
                else:
                    print("Connection failure\n")
            else:
                print("You must login first \n")
        elif userInput[0] == "exit":
            """Exit handling"""
            if len(userInput) > 1:
                print("Too many arguments for command exit; example \"exit\"\n")
            else:
                break

        elif userInput[0] == "help":
            """Help handling"""
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
