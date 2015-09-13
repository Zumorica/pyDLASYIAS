import pyDLASYIAS
import socketserver
import socket
import copy
import traceback
import threading
import time
import pickle
import pyglet
import pyDLASYIAS.networking.netObjects as netObjects
import sys

sys.setrecursionlimit(25000)

class Client(object):
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.character = None
        self.character_object = None
        self.old_character_object = None
        self.isReady = False

class Dummy(object):
    def __init__(self, request=socket.socket(socket.AF_INET, socket.SOCK_DGRAM), client_address=("0.0.0.0", 1987), server=None, character=None):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.character = character

        if character == "guard":
            self.character_object = netObjects.Guard()
            self.old_character_object = netObjects.Guard()
        if character == "chicken":
            self.character_object = netObjects.Chicken()
            self.old_character_object = netObjects.Chicken()
        if character == "rabbit":
            self.character_object = netObjects.Rabbit()
            self.old_character_object = netObjects.Rabbit()
        if character == "bear":
            self.character_object = netObjects.Bear()
            self.old_character_object = netObjects.Bear()
        if character == "fox":
            self.character_object = netObjects.Fox()
            self.old_character_object = netObjects.Fox()
        else:
            self.character_object = None
            self.old_character_object = None

        self.isReady = False

class pyDLASYIAS_UDPHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        obj = pickle.loads(self.request[0])
        if obj.event != "connecting_to_server":
            # if self.client_address not in self.server.clients and not self.server.isFull:
            #     self.server.clients[client_address] = Client(request, client_address, server)
            #     self.client = self.server.clients[self.client_address]
            if self.client_address in self.server.clients.keys():
                self.client = self.server.clients[self.client_address]
                try:
                    self.handle()
                finally:
                    self.finish()
        else:
            if not self.server.isFull:
                self.request[1].sendto(netObjects.Event("connection_okay").get_pickled(), client_address)
                self.server.clients[client_address] = Client(request[1], client_address, server)
                self.client = self.server.clients[self.client_address]

    def handle(self):
        obj = pickle.loads(self.request[0])
        try:
            if self.server.state == "character_select":
                # Can only receive events. No other objects will be received here.
                if obj.event == "connected":
                    for client in self.server.clients.values():
                        if client.character == None:
                            pass

                        elif client.character in ["guard", "rabbit", "chicken", "bear", "fox"]:
                            for i in range(0, 5):
                                self.request[1].sendto(netObjects.Event('%s_locked'%(client.character)).get_pickled(), self.client_address)

                elif obj.event == "guard_locked":
                    self.client.character = "guard"
                    self.client.character_object = netObjects.Guard()
                    for address, client in self.server.clients.items():
                        for i in range(0, 5):
                            if address != self.client_address:
                                client.request.sendto(self.request[0], address)

                elif obj.event == "chicken_locked":
                    self.client.character = "chicken"
                    self.client.character_object = netObjects.Chicken()
                    for address, client in self.server.clients.items():
                        for i in range(0, 5):
                            if address != self.client_address:
                                client.request.sendto(self.request[0], address)

                elif obj.event == "rabbit_locked":
                    self.client.character = "rabbit"
                    self.client.character_object = netObjects.Rabbit()
                    for address, client in self.server.clients.items():
                        for i in range(0, 5):
                            if address != self.client_address:
                                client.request.sendto(self.request[0], address)

                elif obj.event == "bear_locked":
                    self.client.character = "bear"
                    self.client.character_object = netObjects.Bear()
                    for address, client in self.server.clients.items():
                        for i in range(0, 5):
                            if address != self.client_address:
                                client.request.sendto(self.request[0], address)

                elif obj.event == "fox_locked":
                    self.client.character = "fox"
                    self.client.character_object = netObjects.Fox()
                    for address, client in self.server.clients.items():
                        for i in range(0, 5):
                            if address != self.client_address:
                                client.request.sendto(self.request[0], address)

                elif obj.event == "game_start":
                    pass    # Is someone sending events that they shouldn't?


            if self.server.state == "game":
                if obj.kind == "event":
                    print(obj.event)

                elif obj.kind == "guard" and self.client.character == "guard":
                    self.client.old_character_object = copy.copy(self.client.character_object)
                    self.client.character_object = copy.copy(obj)
                    print(self.client.character_object.scene)

                    if self.client.old_character_object.scene != "scarejump" and self.client.character_object.scene == "scarejump":
                        for clt in self.server.clients.values():
                            if clt.character in ["rabbit", "chicken", "bear", "fox"]:
                                if clt.status == 5 or clt.location == "inside":
                                    winner = clt.kind

                                    for address, client in self.server.clients.items():
                                        client.request.sendto(netObjects.Event("scarejump", winner))

                elif obj.kind == "chicken" and self.client.character == "chicken":
                    self.client.old_character_object = copy.copy(self.client.character_object)
                    self.client.character_object = copy.copy(obj)

                elif obj.kind == "rabbit" and self.client.character == "rabbit":
                    self.client.old_character_object = copy.copy(self.client.character_object)
                    self.client.character_object = copy.copy(obj)

                elif obj.kind == "bear" and self.client.character == "bear":
                    self.client.old_character_object = copy.copy(self.client.character_object)
                    self.client.character_object = copy.copy(obj)

                elif obj.kind == "fox" and self.client.character == "fox":
                    self.client.old_character_object = copy.copy(self.client.character_object)
                    self.client.character_object = copy.copy(obj)

        except Exception as err:
            print(traceback.format_exc())

        # if obj.kind == "event" and self.server.state == "character_select":
        #     if obj.event == "connected":
        #         for i in range(0, 5):
        #             for client in self.server.clients.values():
        #                 print(client.character)
        #                 if client.character == None:
        #                     pass
        #                 elif client.character == "guard":
        #                     self.request[1].sendto(netObjects.Event('guard_locked').get_pickled(), self.client_address)
        #                 elif client.character == "rabbit":
        #                     self.request[1].sendto(netObjects.Event('rabbit_locked').get_pickled(), self.client_address)
        #                 elif client.character == "chicken":
        #                     self.request[1].sendto(netObjects.Event('chicken_locked').get_pickled(), self.client_address)
        #                 elif client.character == "bear":
        #                     self.request[1].sendto(netObjects.Event('bear_locked').get_pickled(), self.client_address)
        #                 elif client.character == "fox":
        #                     self.request[1].sendto(netObjects.Event('fox_locked').get_pickled(), self.client_address)
        #
        #     if obj.event == "guard_locked":
        #         self.client.character = "guard"
        #
        #     elif obj.event == "bear_locked":
        #         self.client.character = "bear"
        #
        #     elif obj.event == "chicken_locked":
        #         self.client.character = "chicken"
        #
        #     elif obj.event == "bear_locked":
        #         self.client.character = "bear"
        #
        #     elif obj.event == "fox_locked":
        #         self.client.character = "fox"
        #
        # for address, client in self.server.clients.items():
        #     try:
        #         if address != self.client_address:
        #             if self.server.state != "game":
        #                 if obj.kind == "event":
        #                     if obj.event == "guard_locked":
        #                         self.client.character = "guard"
        #
        #                     elif obj.event == "bear_locked":
        #                         self.client.character = "bear"
        #
        #                     elif obj.event == "chicken_locked":
        #                         self.client.character = "chicken"
        #
        #                     elif obj.event == "bear_locked":
        #                         self.client.character = "bear"
        #
        #                     elif obj.event == "fox_locked":
        #                         self.client.character = "fox"
        #                 client.request.sendto(self.request[0], address)
        #             elif self.client.character == "guard" and self.server.state == "game":
        #                 self.client.old_character_object = self.client.character_object
        #                 self.client.character_object = pickle.loads(self.request[0])
        #
        #                 if self.client.old_character_object.scene != "scarejump" and self.client.character_object.scene == "scarejump":
        #                     for clt in self.server.clients.values():
        #                         if clt.character in ["rabbit", "chicken", "bear", "fox"]:
        #                             if clt.status == 5 or clt.location == "inside":
        #                                 winner = clt.kind
        #
        #                                 client.request.sendto(netObjects.Event("scarejump", winner))
        #
        #             elif self.client.character == "chicken" and self.server.state == "game":
        #                 self.client.old_character_object = self.client.character_object
        #                 self.client.character_object = pickle.loads(self.request[0])
        #
        #             elif self.client.character == "rabbit" and self.server.state == "game":
        #                 self.client.old_character_object = self.client.character_object
        #                 self.client.character_object = pickle.loads(self.request[0])
        #
        #             elif self.client.character == "bear" and self.server.state == "game":
        #                 self.client.old_character_object = self.client.character_object
        #                 self.client.character_object = pickle.loads(self.request[0])
        #
        #             elif self.client.character == "fox" and self.server.state == "game":
        #                 self.client.old_character_object = self.client.character_object
        #                 self.client.character_object = pickle.loads(self.request[0])
        #
        #         else:
        #             pass
        #
        #     except AttributeError as e:
        #         print("Warning:", e)

class Server(socketserver.UDPServer):
    def __init__(self, host=(), handler=pyDLASYIAS_UDPHandler):
        self.clients = {("0.0.0.0", 1987) : Dummy(server=self, character="bear"),
                        ("0.0.0.0", 1988) : Dummy(server=self, character="rabbit"),
                        ("0.0.0.0", 1989) : Dummy(server=self, character="fox")}
        self.isFull = False

        self.hour = -1
        self.power = 100

        self.state = "character_select"

        self.update_thread = threading.Thread(target=self.update)
        self.time_thread = threading.Thread(target=self.next_hour)
        self.power_thread = threading.Thread(target=self.power_calculations)
        self.command_thread = threading.Thread(target=self.commands)
        self.world_thread = threading.Thread(target=self.send_world)

        self.update_thread.start()
        self.command_thread.start()

        super().__init__(host, handler)

    def on_game_start(self):
        for client in self.clients.values():
            if client.character == "guard":
                self.guard = client
            elif client.character == "chicken":
                self.chicken = client
            elif client.character == "rabbit":
                self.rabbit = client
            elif client.character == "bear":
                self.bear = client
            elif client.character == "fox":
                self.fox = client
            client.request.sendto(pyDLASYIAS.networking.netObjects.Event("game_start").get_pickled(), client.client_address)

        self.state = "game"
        self.power_thread.start()
        self.time_thread.start()
        self.world_thread.start()

    def send_world(self):
        while True:
            world = netObjects.World(self.power, self.hour, self.guard.character_object, self.chicken.character_object, netObjects.Rabbit(), netObjects.Bear(), netObjects.Fox())
            for client in self.clients.values():
                client.request.sendto(world.get_pickled(), client.client_address)
            time.sleep(1/30)

    def power_calculations(self, dt=0, old_usage=1):
        if dt == 0:
            if self.power >= 0:
                try:
                    if self.guard.character_object.usage == 1:
                        if old_usage == 1:
                            self.power -= 1

                        if old_usage >= 2:
                            self.power -= 2

                        self.power_calculations(9.6, 1)

                    if self.guard.character_object.usage == 2:
                        if old_usage == 1:
                            self.power -= 1

                        if old_usage == 2:
                            self.power -= 1

                        if old_usage >= 3:
                            self.power -= 2

                        self.power_calculations(4.8, 2)

                    if self.guard.character_object.usage == 3:
                        if old_usage == 1:
                            self.power -= 1

                        if old_usage == 2:
                            self.power -= 1

                        if old_usage == 3:
                            self.power -= 1

                        if old_usage == 4:
                            self.power -= 2

                        self.power_calculations(random.choice([2.8, 2.9, 3.9]), 3)

                    if self.guard.character_object.usage == 4:
                        self.power -= 1

                        self.power_calculations(random.choice([1.9, 2.9]), 4)

                    if self.guard.character_object.usage == 5:
                        self.guard.character_object.usage = 4
                        self.power -= 1

                        self.power_calculations(random.choice([1.9, 2.9]), 4)
                except AttributeError:
                    pass
            else:
                time.sleep(dt)
                self.power_calculations(0, old_usage)

    def next_hour(self):
        if self.hour != 6:
            self.hour += 1
            time.sleep(86)
            self.next_hour()

    def update(self):
        if self.state == "character_select":
            if len(self.clients) == 5:
                self.isFull = True
                values = list(self.clients.values())
                if values[0].character and values[1].character \
                and values[2].character and values[3].character \
                and values[4].character and self.state != "game":
                    self.state == "game"
                    try:
                        self.on_game_start()
                    except RuntimeError:
                        pass

        elif self.state == "game":
            pass

        time.sleep(0.15)
        self.update()

    def commands(self):
        cmd = input("> ")
        try:
            exec(cmd)
        except Exception as err:
            print(traceback.format_exc())
        self.commands()

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = Server((HOST, PORT), pyDLASYIAS_UDPHandler)
    server.serve_forever()
