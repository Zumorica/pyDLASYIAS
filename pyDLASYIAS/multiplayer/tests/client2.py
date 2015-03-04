import socket
import sys
import threading

HOST, PORT = "localhost", 1987

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))

    received = str(sock.recv(1024), "utf-8")

finally:
    while 1:
        print("WOO")
        received = str(sock.recv(1024), "utf-8")
        print("Received: {}".format(received))
