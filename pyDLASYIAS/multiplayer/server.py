import socketserver
import threading
import time

from socketserver import *

global data, clients, usage, leftdoor, rightdoor, leftlight, rightlight, guardScene, time, power, guardSelected, bearSelected, rabbitSelected, chickenSelected, foxSelected

clients = []

data = None

time = 0

power = 100
usage = 1

leftdoor = False
rightdoor = False

leftlight = False
rightlight = False

guardScene = "office"

guardSelected = False
bearSelected = False
rabbitSelected = False
chickenSelected = False
foxSelected = False

class client():
    '''Class for the client.'''
    def __init__(self, request, client_address):
        self.request = request
        self.client_address = client_address
        self.character = "None"

    def __str__(self):
        return "(%s, %s)" %(self.client_address, self.character)

    def __repr__(self):
        return "(%s, %s)" %(self.client_address, self.character)

    def kick(self):
        self.request.close()

    def send(self, data):
        self.request.send(bytes(str(data), "utf-8"))

class requestHandler(socketserver.BaseRequestHandler):
    '''Handles the requests.'''
    def setup(self):
        '''When a new client connects to the server, this function gets called.'''

        global data, clients, usage, leftdoor, rightdoor, leftlight, rightlight, guardScene, time, power, guardSelected, bearSelected, rabbitSelected, chickenSelected, foxSelected

        clients.append(client(self.request, self.client_address))


    def handle(self):
        '''Handles requests.'''

        global data, clients, usage, leftdoor, rightdoor, leftlight, rightlight, guardScene, time, power, guardSelected, bearSelected, rabbitSelected, chickenSelected, foxSelected

        while 1:
            data = self.request.recv(1024)

            if str(data) == "guard -> leftdoor true":
                leftdoor = True
                print("leftdoor %s" % (leftdoor))
                usage += 1

            if str(data) == "guard -> leftdoor false":
                leftdoor = False
                usage -= 1

            if str(data) == "guard -> rightdoor true":
                rightdoor = True
                usage += 1

            if str(data) == "guard -> rightdoor false":
                rightdoor = False
                usage -= 1


            if str(data) == "guard -> leftlight false":
                leftlight = False
                usage -= 1

            if str(data) == "guard -> leftlight true":
                leftlight = True
                usage += 1

                if rightlight:
                    rightlight = False
                    usage -= 1

            if str(data) == "guard -> rightlight false":
                rightlight = False
                usage -= 1

            if str(data) == "guard -> rightlight true":
                rightlight = True
                usage += 1

                if leftlight:
                    leftlight = False
                    usage -= 1


            if str(data) == "guard -> cam":
                if guardScene == "office":
                    guardScene == "cam"
                    usage += 1

            if str(data) == "guard -> office":
                if guardScene == "cam":
                    guardScene = "office"
                    usage -= 1

            if str(data) == "guard -> 6AM":
                guardScene == "6AM"

            if str(data) == "guard -> end":
                guardScene = "end"
                sendToAll("server -> shutdown")

            if str(data) == "bear selected" and not bearSelected:
                bearSelected = True

            if str(data) == "rabbit selected" and not rabbitSelected:
                rabbitSelected = True

            if str(data) == "chicken selected" and not chickenSelected:
                chickenSelected = True

            if str(data) == "fox selected" and not foxSelected:
                foxSelected = True

            if str(data) == "guard selected" and not guardSelected:
                guardSelected = True

            print(str(data) + ' ' + str(self.client_address) + '\n')

    def finish(self):
        '''When a clients disconnects this function gets called.'''

        clients.remove(self.request)
        print(self.client_address, 'disconnected!')

def sendData():
    '''Sends received data to all connected clients.'''

    global data, clients, usage, leftdoor, rightdoor, leftlight, rightlight, guardScene, time, power

    while 1:
        if data != None and data != b'':
            for client in clients:
                client.send(bytes(data))
                print("Sent " + str(data) + " to %s" % (client))

            data = None

def sendToAll(text):
    '''Send text to all connected clients.'''

    global data, clients, usage, leftdoor, rightdoor, leftlight, rightlight, guardScene, time, power

    for client in clients:
        client.send(text)

def powerTimer():
    global data, clients, usage, leftdoor, rightdoor, leftlight, rightlight, guardScene, time, power

    if len(clients) > 2:
        power -= 1

    sendToAll("server -> power - 1")

    if usage == 1:
        threading.Timer(9.6, powerTimer).start()

    elif usage == 2:
        threading.Timer(4.8, powerTimer).start()

    elif usage == 3:
        threading.Timer(random.choice([2.8, 2.9, 3.9]), powerTimer).start()

    elif usage >= 4:
        threading.Timer(random.choice([1.9, 2.9]), powerTimer).start()

def hourTimer():

    global data, clients, usage, leftdoor, rightdoor, leftlight, rightlight, guardScene, time, power

    time += 1

    sendToAll("time -> %s" %(time))

    threading.Timer(86, hourTimer).start()


def cmd():

    global data, clients, usage, leftdoor, rightdoor, leftlight, rightlight, guardScene, time, power

    print()
    print("Power left: %s, Usage: %s" % (power,usage))
    print("Time %s" % (time))
    print()
    command = input("> ")
    print()

    if command.lower() == "power":

        power += 0
        usage += 0

        print("Power left: %s, Usage: %s" % (power,usage))

    if command.lower() == "time":

        time += 0

        print("Time: %s" % (time))

    if command.lower() == "state":
        print("Left Door: %s" % (leftdoor))
        print("Right Door: %s" % (rightdoor))
        print("Left Light: %s" % (leftlight))
        print("Right Light: %s" % (rightlight))

    if command.lower() == "clients":
        for client in clients:
            print(str(client))

    if command.lower() == "send":
        toSend = input("Send> ")
        for client in clients:
            client.send(bytes(toSend, "utf-8"))

    if command.lower() == "exec":
        exec(input("Exec> "))

    cmd()

class pyDLASYIAS_Server(ThreadingMixIn, TCPServer): pass

if __name__ == "__main__":
    #threading.Timer(0.1, powerTimer).start()
    #threading.Timer(86, hourTimer).start()
    threading.Thread(target=cmd).start()
    threading.Thread(target=sendData).start()
    server = pyDLASYIAS_Server(('localhost', 1987), requestHandler)
    server.serve_forever()

else:
    print("Server.py must be executed...")
