import threading
import socket

#local network, to set for online utilize your IP address
BITS = 1024
hostname = socket.gethostname()
opening_msg = 'Welcome'

HOST = '127.0.0.1'
PORT = 55555
#setting up the server, AF_INET for internet and SOCK_STREAM for TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
#list of info to manage
clients = []
nicknames = []


#sends messages to client connections
def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:

        try: #sends messages to the other clients, server just broadcasts the messages
            message = client.recv(BITS)
            print(f"{nicknames[clients.index(client)]} --> {message}")
            broadcast(message)

        except: #Removes and closes clients from the server
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

#Main function that runs everything 
def receive():
    while True:
        #accepts new clients to the server
        client, address = server.accept()

        print("Connected with " + str(address))
        client.send(opening_msg.encode('utf-8'))
# setting the username that the user typed, receiving from client.py
        nickname = client.recv(BITS)
        nicknames.append(nickname)

        clients.append(client)
        print("Username of the client is " + str(nickname))

        broadcast(f"You have Connected with {nickname}\n".encode('utf-8'))
        client.send("Connected to the server\n".encode('utf-8'))

        #Allows multiple threads to occur
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("server is listening....")


receive()