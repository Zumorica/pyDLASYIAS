import pyDLASYIAS
import socketserver
import pickle

class Client(object):
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.character = None
        self.isReady = False

class pyDLASYIAS_UDPHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.request = request
        if self.request[0] != b"testing_connection":
            self.client_address = client_address
            self.server = server
            if self.client_address not in self.server.clients and not self.server.isFull:
                self.server.clients[client_address] = Client(request, client_address, server)
                self.client = self.server.clients[self.client_address]
            if not self.client_address not in self.server.clients and not self.server.isFull:
                try:
                    self.handle()
                finally:
                    self.finish()
            else:
                self.request.close()
        else:
            self.request[1].sendto(b"connection_okay", client_address)
            self.request.close()

    def handle(self):
        for address, client in self.server.clients.items():
            if address != self.client_address:
                client.request[1].sendto(self.request[0], address)
                print(address, client, self.request[0])

class Server(socketserver.UDPServer):
    def __init__(self, host=(), handler=pyDLASYIAS_UDPHandler):
        self.clients = {}
        self.isFull = False


        super().__init__(host, handler)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = Server((HOST, PORT), pyDLASYIAS_UDPHandler)
    server.serve_forever()


# class client():
#     '''Class for the client.'''
#     def __init__(self, request, client_address, server):
#         self.request = request
#         self.client_address = client_address
#
#         self.server = server
#
#         self.isClosed = False
#         self.data = b''
#
#         self.character = "None"
#         self.location = "None"
#         self.lastcam = "None"
#         self.scene = "None"
#         self.status = 0
#
#         self.isReady = False
#
#         threading.Thread(target=self.update).start()
#
#     def __str__(self):
#         return "(%s, %s)" %(self.client_address, self.character)
#
#     def __repr__(self):
#         return "(%s, %s)" %(self.client_address, self.character)
#
#     def setup(self):
#         if self.character != "guard":
#             if self.character != "fox":
#                 self.location = "cam1a"
#                 del self.status
#             else:
#                 self.location = "cam1c"
#                 self.status = 1
#                 del self.lastcam
#                 del self.scene
#         else:
#             self.lastcam = "cam1a"
#             self.scene = "office"
#             del self.location
#             del self.status
#
#     def receive(self):
#         if not self.isClosed:
#             return self.request.recv(1024)
#
#     def send(self, data):
#         if not self.isClosed:
#             self.request.send(bytes(str(data), "utf-8"))
#
#     def update(self):
#         try:
#             self.data = self.receive()
#         except:
#             self.kick()
#
#         if not self.isClosed and self.server.isRunning:
#             self.update()
#
#     def kick(self):
#         self.request.close()
#         self.isClosed = True
#
# class requestHandler(socketserver.BaseRequestHandler):
#     '''Handles the requests.'''
#     def setup(self):
#         '''When a new client connects to the server, this function gets called.'''
#         self.server.clients.append(client(self.request, self.client_address, self.server))
#
#
#     def handle(self):
#         '''Handles requests.'''
#         while self.server.isRunning:
#             pass
#
#     def finish(self):
#         '''When a clients disconnects this function gets called.'''
#         print(self.client_address, 'disconnected!')
#
# class pyDLASYIAS_Server(ThreadingMixIn, TCPServer):
#
#     def __init__(self, server_Address, request_Handler):
#
#         super(pyDLASYIAS_Server, self).__init__(server_Address, request_Handler)
#
#         self.clients = []
#
#         self.time = 0
#         self.power = 100
#         self.usage = 1
#
#         self.leftdoor = False
#         self.rightdoor = False
#
#         self.leftlight = False
#         self.rightlight = False
#
#         self.bearSelected = False
#         self.rabbitSelected = False
#         self.chickenSelected = False
#         self.foxSelected = False
#         self.guardSelected = False
#
#         self.bear = None
#         self.rabbit = None
#         self.chicken = None
#         self.fox = None
#         self.guard = None
#
#         self.stage = "multihall"
#
#         self.isRunning = True
#
#         self.cmdThread = threading.Thread(target=self.cmd)
#         self.updateThread = threading.Thread(target=self.update)
#         self.timeThread = threading.Thread(target=self.timeUpdate)
#         self.powerThread = threading.Thread(target=self.powerUpdate)
#
#         self.cmdThread.setDaemon(True)
#         self.updateThread.setDaemon(True)
#         self.timeThread.setDaemon(True)
#         self.powerThread.setDaemon(True)
#
#         self.cmdThread.start()
#         self.updateThread.start()
#
#     def update(self):
#         for client in self.clients:
#
#             if self.stage == "multihall":
#                 if client.data == b"bear selected" and not self.bearSelected:
#                     client.character = "bear"
#                     self.bearSelected = True
#                     self.bear = client
#                     self.bear.isReady = True
#                     self.broadcast("bear selected")
#
#                 if client.data == b"rabbit selected" and not self.rabbitSelected:
#                     client.character = "rabbit"
#                     self.rabbitSelected = True
#                     self.rabbit = client
#                     self.rabbit.isReady = True
#                     self.broadcast("rabbit selected")
#
#                 if client.data == b"chicken selected" and not self.chickenSelected:
#                     client.character = "chicken"
#                     self.chickenSelected = True
#                     self.chicken = client
#                     self.chicken.isReady = True
#                     self.broadcast("chicken selected")
#
#                 if client.data == b"fox selected" and not self.foxSelected:
#                     client.character = "fox"
#                     self.foxSelected = True
#                     self.fox = client
#                     self.fox.isReady = True
#                     self.broadcast("fox selected")
#
#                 if client.data == b"guard selected" and not self.guardSelected:
#                     client.character = "guard"
#                     self.guardSelected = True
#                     self.guard = client
#                     self.guard.isReady = True
#                     self.broadcast("guard selected")
#
#                 try:
#                     if self.bear.isReady and self.rabbit.isReady and self.chicken.isReady and self.fox.isReady and self.guard.isReady:
#                         self.stage = "game"
#                         self.broadcast("game start")
#
#                         self.timeThread.start()
#                         self.powerThread.start()
#
#                 except:
#                     pass
#
#             if self.stage == "game":
#                 for client in self.clients:
#                     bdata = client.data()
#
#                     try:
#                         data = pickle.loads(bdata)
#
#                     except:
#                         pass
#
#                     else:
#                         if data.type == "Animatronic":
#                             client.location = data.location
#                             client.name = data.name
#                             client.kind = data.kind
#                             client.status = data.status
#                             self.broadcast(bdata, exclude=[client])
#
#                         if data.type == "Guard":
#                             client.name = data.name
#                             client.scene = data.scene
#                             client.lastcam = data.lastcam
#                             client.usage = data.usage
#                             client.leftdoor = data.leftdoor
#                             client.leftlight = data.leftlight
#                             client.rightdoor = data.rightdoor
#                             client.rightlight = data.rightlight
#                             self.broadcast(bdata, exclude=[client])
#
#                         if data.type == "Message":
#                             print("%s: %s" %(data.name, data.message))
