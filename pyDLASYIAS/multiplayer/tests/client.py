import socket
import sys
import threading

HOST, PORT = "localhost", int(input())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def client():
    try:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))

        received = str(sock.recv(1024), "utf-8")

    finally:
        while 1:
            receive()
            sock.send(bytes(input("> "), "utf-8"))

def receive():
    global received
    received = str(sock.recv(1024), "utf-8")
    print(received)

threading.Thread(target=receive)
client()
