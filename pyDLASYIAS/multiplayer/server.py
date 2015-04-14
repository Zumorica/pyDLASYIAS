import socketserver
import socket
import threading
import time
import sys
import random
from socketserver import *

class client():
    '''Class for the client.'''
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address

        self.server = server

        self.isClosed = False
        self.data = b''

        self.character = "None"
        self.location = "None"
        self.lastcam = "None"
        self.scene = "None"
        self.status = 0

        self.isReady = False

        threading.Thread(target=self.update).start()

    def __str__(self):
        return "(%s, %s)" %(self.client_address, self.character)

    def __repr__(self):
        return "(%s, %s)" %(self.client_address, self.character)

    def setup(self):
        if self.character != "guard":
            if self.character != "fox":
                self.location = "cam1a"
                del self.status
            else:
                self.location = "cam1c"
                self.status = 1
                del self.lastcam
                del self.scene
        else:
            self.lastcam = "cam1a"
            self.scene = "office"
            del self.location
            del self.status

    def receive(self):
        if not self.isClosed:
            return self.request.recv(1024)

    def send(self, data):
        if not self.isClosed:
            self.request.send(bytes(str(data), "utf-8"))

    def update(self):
        try:
            self.data = self.receive()
        except:
            self.kick()

        if not self.isClosed and self.server.isRunning:
            self.update()

    def kick(self):
        self.request.close()
        self.isClosed = True

class requestHandler(socketserver.BaseRequestHandler):
    '''Handles the requests.'''
    def setup(self):
        '''When a new client connects to the server, this function gets called.'''
        self.server.clients.append(client(self.request, self.client_address, self.server))


    def handle(self):
        '''Handles requests.'''
        while self.server.isRunning:
            pass

    def finish(self):
        '''When a clients disconnects this function gets called.'''
        print(self.client_address, 'disconnected!')

class pyDLASYIAS_Server(ThreadingMixIn, TCPServer):

    def __init__(self, server_Address, request_Handler):

        super(pyDLASYIAS_Server, self).__init__(server_Address, request_Handler)

        self.clients = []

        self.time = 0
        self.power = 100
        self.usage = 1

        self.leftdoor = False
        self.rightdoor = False

        self.leftlight = False
        self.rightlight = False

        self.bearSelected = False
        self.rabbitSelected = False
        self.chickenSelected = False
        self.foxSelected = False
        self.guardSelected = False

        self.bear = None
        self.rabbit = None
        self.chicken = None
        self.fox = None
        self.guard = None

        self.stage = "multihall"

        self.isRunning = True

        self.cmdThread = threading.Thread(target=self.cmd)
        self.updateThread = threading.Thread(target=self.update)
        self.timeThread = threading.Thread(target=self.timeUpdate)
        self.powerThread = threading.Thread(target=self.powerUpdate)

        self.cmdThread.setDaemon(True)
        self.updateThread.setDaemon(True)
        self.timeThread.setDaemon(True)
        self.powerThread.setDaemon(True)

        self.cmdThread.start()
        self.updateThread.start()

    def update(self):
        for client in self.clients:

            if self.stage == "multihall":
                if client.data == b"bear selected" and not self.bearSelected:
                    client.character = "bear"
                    self.bearSelected = True
                    self.bear = client
                    self.bear.isReady = True
                    self.broadcast("bear selected")

                if client.data == b"rabbit selected" and not self.rabbitSelected:
                    client.character = "rabbit"
                    self.rabbitSelected = True
                    self.rabbit = client
                    self.rabbit.isReady = True
                    self.broadcast("rabbit selected")

                if client.data == b"chicken selected" and not self.chickenSelected:
                    client.character = "chicken"
                    self.chickenSelected = True
                    self.chicken = client
                    self.chicken.isReady = True
                    self.broadcast("chicken selected")

                if client.data == b"fox selected" and not self.foxSelected:
                    client.character = "fox"
                    self.foxSelected = True
                    self.fox = client
                    self.fox.isReady = True
                    self.broadcast("fox selected")

                if client.data == b"guard selected" and not self.guardSelected:
                    client.character = "guard"
                    self.guardSelected = True
                    self.guard = client
                    self.guard.isReady = True
                    self.broadcast("guard selected")

                try:
                    if self.bear.isReady and self.rabbit.isReady and self.chicken.isReady and self.fox.isReady and self.guard.isReady:
                        self.stage = "game"
                        self.broadcast("game start")

                        self.timeThread.start()
                        self.powerThread.start()

                except:
                    pass

            if self.stage == "game":
                for client in self.clients:
                    data = str(client.data(), "utf-8").split()

                    if client.character == "bear":
                        pass

                    if client.character == "rabbit":
                        pass

                    if client.character == "chicken":
                        if data[0] == "goto":

                            if data[1] == "cam1b" and self.chicken.location in ["cam1a", "cam7", "cam6"]:
                                self.chicken.location = "cam1b"
                                self.broadcast("chicken goto cam1b")

                            if data[1] == "cam4a" and self.chicken.location in ["cam6", "cam7"]:
                                self.chicken.location = "cam4a"
                                self.broadcast("chicken goto cam4a")

                            if data[1] == "cam4b" and self.chicken.location in ["cam4a"]:
                                self.chicken.location = "cam4b"
                                self.broadcast("chicken goto cam4b")

                            if data[1] == "cam6" and self.chicken.location in ["cam1b", "cam7"]:
                                self.chicken.location = "cam6"
                                self.broadcast("chicken goto cam6")

                            if data[1] == "cam7" and self.chicken.location in ["cam1b", "cam6"]:
                                self.chicken.location = "cam7"
                                self.broadcast("chicken goto cam7")

                            if data[1] == "rightdoor" and self.chicken.location in ["cam4b"]:
                                self.chicken.location = "rightdoor"
                                self.broadcast("chicken goto rightdoor")

                    if client.character == "fox":

                        if data[0] == "status":

                            if data[1] == "up":
                                client.status += 1
                                self.broadcast("fox status %s" %(client.status))

                            if data[1] == "down":
                                client.status -= 1
                                self.broadcast("fox status %s" %(client.status))

                            if data[1] == "0":
                                client.status = 0
                                self.broadcast("fox status %s" %(client.status))

                            if data[1] == "1":
                                client.status = 1
                                self.broadcast("fox status %s" %(client.status))

                            if data[1] == "2":
                                client.status = 2
                                self.broadcast("fox status %s" %(client.status))

                            if data[1] == "3":
                                client.status = 3
                                self.broadcast("fox status %s" %(client.status))

                            if data[1] == "4":
                                client.status = 4
                                self.broadcast("fox status %s" %(client.status))

                            if data[1] == "5":
                                client.status = 5
                                self.broadcast("fox status %s" %(client.status))

                    if client.character == "guard":

                        if data[0] == "scene":

                            if data[1] == "office":
                                client.scene = "office"
                                self.broadcast("guard scene office")

                            if data[1] == "cam":
                                client.scene = "cam"
                                self.broadcast("guard scene cam")

                        if data[0] == "check":

                            if data[1] in ["cam1a", "cam1b", "cam1c", "cam2a",
                                           "cam2b", "cam3", "cam4a", "cam4b",
                                           "cam5", "cam6", "cam7"]:
                                client.lastcam = data[1]
                                self.broadcast("guard check %s" %(client.lastcam))

                        if data[0] == "leftdoor":

                            if data[1] == "true":
                                if not self.leftdoor:
                                    self.leftdoor = True
                                    self.usage += 1
                                    self.broadcast("guard leftdoor true")

                            if data[1] == "false":
                                if self.leftdoor:
                                    self.leftdoor = False
                                    self.usage += 1
                                    self.broadcast("guard leftdoor false")

                        if data[0] == "rightdoor":

                            if data[1] == "true":
                                if not self.rightdoor:
                                    self.rightdoor = True
                                    self.usage += 1
                                    self.broadcast("guard rightdoor true")

                            if data[1] == "false":
                                if self.rightdoor:
                                    self.rightdoor = False
                                    self.usage -= 1
                                    self.broadcast("guard rightdoor false")

                        if data[0] == "leftlight":

                            if data[1] == "true":
                                if not self.leftlight:
                                    if self.rightlight:

                                        self.rightlight = False
                                        self.leftlight = True

                                        self.broadcast("guard rightlight false")
                                        self.broadcast("guard leftlight true")

                                        self.usage += 1
                                        self.usage -= 1
                                    else:
                                        self.leftlight = True
                                        self.usage += 1
                                        self.broadcast("guard leftlight true")

                            if data[1] == "false":
                                if self.leftlight:
                                    self.leftlight = False
                                    self.usage -= 1
                                    self.broadcast("guard leftlight false")

                        if data[0] == "rightlight":

                            if data[1] == "true":
                                if not self.rightlight:
                                    if self.rightlight:
                                        self.leftlight = False
                                        self.rightlight = True

                                        self.broadcast("guard rightlight true")
                                        self.broadcast("guard leftlight false")

                                        self.usage += 1
                                        self.usage -= 1

                                    else:
                                        self.rightlight = True
                                        self.usage += 1

                                        self.broadcast("guard rightlight true")

                            if data[1] == "false":
                                if self.rightlight:
                                    self.rightlight = False
                                    self.usage -= 1

                                    self.broadcast("guard rightlight false")

                        if data[0] == "scene":

                            if data[1] == "office":
                                client.scene = "office"
                                self.broadcast("guard scene office")

                            if data[1] == "cam":
                                client.scene = "cam"
                                self.broadcast("guard scene cam")







        time.sleep(1.987)
        if self.isRunning:
            self.update()

    def broadcast(self, data, exclude=[]):
        for client in self.clients:
            if client not in exclude:
                client.send(data)


    def cmd(self):

        print()

        print("Power left: %s, Usage: %s" % (self.power, self.usage))
        print("Time %s" % (self.time))

        print()

        command = input("> ").lower()

        print()

        if command == "state":
            print("Left Door: %s" % (self.leftdoor))
            print("Right Door: %s" % (self.rightdoor))
            print("Left Light: %s" % (self.leftlight))
            print("Right Light: %s" % (self.rightlight))
            print("Freddy selected: %s" %(self.bearSelected))
            print("Bonnie selected: %s" %(self.rabbitSelected))
            print("Chica selected: %s" %(self.chickenSelected))
            print("Foxy selected: %s" %(self.foxSelected))
            print("Guard selected: %s" %(self.guardSelected))
            print("Power: %s" %(self.power))
            print("Usage: %s" %(self.usage))
            print("Time: %s" %(self.time))
            print("Stage: %s" %(self.stage))

        if command == "clients":
            for client in self.clients:
                print(str(client))

        if command == "send":
            self.broadcast(input("Send> "))

        if command == "exec":
            print("BE CAREFUL AROUND THIS ONE! You could break the server...")
            print()
            exec(input("Exec> "))

        if command == "close":
            print("Closing down...")
            time.sleep(1)
            for client in self.clients:
                client.kick()
            self.isRunning = False
            sys.exit(0)

        self.cmd()

    def powerUpdate(self):

        if self.stage == "game":
            self.power -= 1
            if self.usage == 1:
                time.sleep(9.6)

            elif self.usage == 2:
                time.sleep(4.8)

            elif self.usage == 3:
                time.sleep(random.choice([2.8, 2.9, 3.9]))

            elif self.usage >= 4:
                time.sleep(random.choice([1.9, 2.9]))

        self.powerUpdate()


    def timeUpdate(self):

        time += 1

        time.sleep(86)

        self.hourUpdate()


if __name__ == "__main__":
    server = pyDLASYIAS_Server(('localhost', 1987), requestHandler).serve_forever()

else:
    print("Server.py must be executed...")
