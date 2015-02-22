import socketserver
import threading
import time

global data, clients, usage, leftdoor, rightdoor, leftlight, rightlight, guardScene, time, power

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

class requestHandler(socketserver.BaseRequestHandler):
    def setup(self):

        global data, clients, usage, leftdoor, rightdoor, leftlight, rightlight, guardScene, time, power

        print(self.client_address, 'connected!')

        self.request.send(bytes("time -> %s" % (time), "utf-8"))

    def handle(self):

        global data, clients, usage, leftdoor, rightdoor, leftlight, rightlight, guardScene, time, power

        while 1:
            if self.request not in clients:
                clients.append(self.request)
                print(clients)

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

            print(str(data) + ' ' + str(self.client_address) + '\n')

    def finish(self):
        clients.remove(self.request)
        print(self.client_address, 'disconnected!')

def sendData():

    global data, clients, usage, leftdoor, rightdoor, leftlight, rightlight, guardScene, time, power

    while 1:
        if data != None and data != b'':
            for client in clients:
                client.send(bytes(data))
                print("Sent " + str(data) + " to %s" % (client))

            data = None

def sendToAll(text):

    global data, clients, usage, leftdoor, rightdoor, leftlight, rightlight, guardScene, time, power

    for client in clients:
        client.send(bytes(text, "utf-8"))

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

    command = input("> ")

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

    cmd()

threading.Timer(0.1, powerTimer).start()
threading.Timer(86, hourTimer).start()
threading.Thread(target=cmd).start()
threading.Thread(target=sendData).start()
server = socketserver.ThreadingTCPServer(('localhost', 1987), requestHandler)
server.serve_forever()
