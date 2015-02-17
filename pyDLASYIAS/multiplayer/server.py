import socketserver
import threading
import time

data = None

class requestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        print(self.client_address, 'connected!')
        self.request.send(bytes('hi ' + str(self.client_address) + '\n', "utf-8"))
        threading.Thread(target=self.sendData).start()
        self.character = None

    def handle(self):
        while 1:
            global data
            data = self.request.recv(1024)

            if data == b"guard" and not self.character:
                self.character = "guard"

            if data == b"chicken" and not self.character:
                self.character = "chicken"

            if data == b"rabbit" and not self.character:
                self.character = "rabbit"

            if data == b"bear" and not self.character:
                self.character = "bear"

            if data == b"fox" and not self.character:
                self.character = "fox"

            print(str(data) + ' ' + str(self.client_address) + '\n')

    def sendData(self):
        print("Thread started")
        while 1:
            global data
            if not self.character and data != None:
                self.request.send(bytes(str(data), "utf-8"))
                print("sent " + str(data))

            if self.character == "guard" and data != None:
                if b"guard" not in data:
                    self.request.sendall(bytes(str(data), "utf-8"))
                    print("sent " + str(data) + "" + str(self.client_address))

            if self.character == "chicken" and data != None:
                if b"chicken" not in data:
                    self.request.sendall(bytes(str(data), "utf-8"))
                    print("sent " + str(data) + "" + str(self.client_address))

            if self.character == "rabbit" and data != None:
                if b"rabbit" not in data:
                    self.request.sendall(bytes(str(data), "utf-8"))
                    print("sent " + str(data) + "" + str(self.client_address))

            if self.character == "bear" and data != None:
                if b"bear" not in data:
                    self.request.sendall(bytes(str(data), "utf-8"))
                    print("sent " + str(data) + "" + str(self.client_address))

            if self.character == "fox" and data != None:
                if b"fox" not in data:
                    self.request.sendall(bytes(str(data), "utf-8"))
                    print("sent " + str(data) + "" + str(self.client_address))

            print(data)
            time.sleep(1)
            data = None

    def finish(self):
        print(self.client_address, 'disconnected!')

server = socketserver.ThreadingTCPServer(('localhost', 1987), requestHandler)
server.serve_forever()


# import socket
# import threading
#
# class server:
#     def __init__(self):
#
#         self.time = 0
#         self.power = 100
#         self.usage = 1
#
#         self.rabbitLocation = "cam1a"
#         self.chickenLocation = "cam1a"
#         self.bearLocation = "cam1a"
#         self.foxStatus = 0
#
#         self.guardLastCam = "cam1a"
#         self.guardScene = "cam"
#         self.guardLeftDoor = False
#         self.guardRightDoor = False
#
#         self.receivedOne = b""
#         self.receivedTwo = b""
#         self.receivedThree = b""
#         self.receivedFour = b""
#         self.receivedFive = b""
#
#         self.threads = []
#
#         self.running = False
#         self.socket = None
#         self.address = input("Address (Blank for automatic)> ")
#         self.port = input("Port (Blank for default port -1987-)> ")
#
#         threading.Timer(0.01, self.powerTimer).start()
#
#         threading.Timer(0.01, self.hourTimer).start()
#
#         self.run()
#
#     def run(self):
#
#         self.running = True
#         self.socket = socket.socket(socket.AF_INET)
#
#         if self.address == "" and self.port == "":
#             self.socket.bind(("", 1987))
#
#         elif self.address != "" and self.port != "":
#             self.socket.bind((self.address, self.port))
#
#         elif self.address == "" and self.port != "":
#             self.socket.bind(("", self.port))
#
#         elif self.address != "" and self.port == "":
#             self.socket.bind((self.address, 1987))
#
#         if len(self.threads) != 5:
#             self.socket.listen(5)
#
#         while self.running:
#
#             print(len(self.threads), self.threads)
#
#             if len(self.threads) != 5:
#                 client = self.socket.accept()[0]
#
#                 new_thread = clientThread(client)
#
#                 self.threads.append(new_thread)
#
#             if len(self.threads) == 5:
#
#                 self.receivedFirst = self.threads[0].receive()
#                 self.receivedTwo = self.threads[1].receive()
#                 self.receivedThree = self.threads[2].receive()
#                 self.receivedFour = self.threads[3].receive()
#                 self.receivedFive = self.threads[4].receive()
#
#                 print(self.receivedOne, self.receivedTwo, self.receivedThree, self.receivedFour, self.receivedFive)
#
#
#         self.socket.close()
#
#     def hourTimer(self):
#         if self.time != 6:
#             self.time += 1
#             threading.Timer(86, self.hourTimer).start()
#
#     def powerTimer(self):
#         self.power -= 1
#         if self.usage == 1:
#             threading.Timer(9.6, self.powerTimer).start()
#         elif self.usage == 2:
#             threading.Timer(4.8, self.powerTimer).start()
#         elif self.usage == 3:
#             threading.Timer(random.choice([2.8, 2.9, 3.9]), self.powerTimer).start()
#         elif self.usage >= 4:
#             threading.Timer(random.choice([1.9, 2.9]), self.powerTimer).start()
#
# class clientThread(threading.Thread):
#     def __init__(self, socket):
#
#         threading.Thread.__init__(self, target=self.receive)
#         self.socket = socket
#
#         self.start()
#
#     def send(self, text):
#         self.socket.send(bytes(str(text), "utf-8"))
#
#     def receive(self):
#         while True:
#             return self.socket.recv(1024)
#
# s = server()
# s.run()
