import socket
import random
import pickle
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])

class Bla(object):
    def __init__(self):
        self.var = random.randint(0, 1000000)

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
while 1:
    sock.sendto(pickle.dumps(Bla()), (HOST, PORT))
    received = pickle.loads(sock.recv(1024))

    print("Sent:     {}".format(data))
    print("Received: {}".format(received))
