class netObject(object):
    '''Class for objects that travel through sockets.'''
    def __init__(self, type):
        self.type = type

    def get_pickled(self):
        import pickle
        return pickle.dumps(self)

    def send_pickled(self, socket):
        socket.send(self.get_pickled())

class Animatronic(netObject):
    '''Class for player-controlled animatronics.'''
    def __init__(self, name, kind):
        super().__init__("Animatronic")
        self.name = name
        self.kind = kind
        self.status = 0         # Used only by foxkind
        if self.kind == "fox":
            self.location = "cam1c"
        else:
            self.location = "cam1a"

class Guard(netObject):
    '''Class for players that play as the guard.'''
    def __init__(self, name, scene="office", lastcam="cam1a", usage=1,
                 leftdoor=False, leftlight=False, rightdoor=False,
                 rightlight=False):
        super().__init__("Guard")
        self.name = name
        self.scene = scene
        self.lastcam = lastcam
        self.usage = usage

        self.leftdoor = leftdoor
        self.leftlight = leftlight
        self.rightdoor = rightdoor
        self.rightlight = rightlight

class Event(netObject):
    '''Class for events. (E.g.: Power goes down by one, 2AM, 3AM, 5AM... etc)'''
    def __init__(self, power=None, time=None):
        super().__init__("Event")
        self.power = power
        self.time = time

class Characters(netObject):
    '''Class for the multiplayer hall.'''
    def __init__(self, bear=False, rabbit=False, chicken=False, fox=False, guard=False):
        super().__init__("Characters")
        self.bear = bear
        self.rabbit = rabbit
        self.chicken = chicken
        self.fox = fox
        self.guard = guard

class Message(netObject):
    '''Class for chat's messages.'''
    def __init__(self, name, message):
        super().__init__("Message")
        self.name = name
        self.message = message
