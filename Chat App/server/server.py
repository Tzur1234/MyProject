# AF_INET : represent the adress ( and the protocol)
# if not defined than this protocol is unssaport

## SOCK_STREAM : represent the sock type 
# The socket type should be SOCK_STREAM (the default) 

# socket is the function we use to create a scoket object

from socket import AF_INET, socket, SOCK_STREAM


# threading - a python module to manage and create threads
# Thread - the function we use to create a thread object
from threading import Thread


# bring Person class from person module
from person import Person


#bring datetime object
from datetime import datetime


# GLOBAL veriables
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT) # final adress of the server's socket
SERVER = socket(AF_INET,SOCK_STREAM) # create the server's socket object
SERVER.bind(ADDR) # set socket's adress ( IP + port)

MAX_CONNECTIONS = 10
BUFSIZ = 512  # the max size of one message


persons = [] #list of all the connected persons



def broadcast(msg, name):
    """
    send messages to all other people in the chat room
    INPUT : btyes object mesage  AND name (str)
    RETURN: None
    """
    
    #loop over all of the client_socket and send them a message
    for person in persons:
        # get the client's particular socket
        client_socket = person.client

        try:
            #send to the particular client the message
            client_socket.  send(bytes(name, 'utf8') + msg)
        except Exception as e:
            print(f"[FAILT TO SEND TO {person.name} CLIENT]" + e)


def client_communication(person):

    """
    Thread to handle all messages from clients 
    input: Person object 
    output: None
    """

    client = person.client
    addr = person.addr
    
    # take the first message from the client (his name)
    # decode the mesage from bytes form to string form 
    name = client.recv(BUFSIZ).decode("utf8")
    
    #update the person's name in the Person class
    person.set_name(name)

    #send the message to all of the connected users
    msg = bytes(f" {name} has joined to the chet !{datetime.now()}", "utf8")
    broadcast(msg, "")

    #wait for message from the person
    while True:
        
        msg = client.recv(BUFSIZ) # checking for a message in the "client" socket
                                  # this line of code will run always till new message will come
                             
        if msg == bytes('{quit}', "utf8"):
            client.close()
            persons.remove(person)
            msg = bytes(f"{name} has discconected the chet {datetime.now()}","utf8")
            broadcast(msg, "")
            print("[DISCONNECTED] {name} has discconected") # for debug
            break # break the loop
        else:
            # send the message to every one
            broadcast(msg, name)
            print(f"{name} send : {msg.decode("utf8")}")
            



#infinte loop waiting for connection from new client
# Start new thread once connected
def wait_for_connection():
    
    
    while True:
        try:
            client, addr = SERVER.accept()  # Accept the connection
                                            # The return value is a pair 
                                            # (client, addr)
                                            # client - the new socket object use for send and reciece data
                                            # addr - the adress of the new socket
                                            # on the other end ot the connection 
                                            # this function will run till recieve a new connection
            
            person = Person(addr,client ) # set new Person Object
            persons.append(person)

            print(f"[CONNECTION] {addr} connected to the server ! {datetime.now()}")

            #One thread take care the client's sending messages
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[FAILURE]", e)
            print("SERVER CRUSHED")            
            break
           
if __name__ == "__main__":
    
    SERVER.listen(MAX_CONNECTIONS) # set the number of connectinos
    print('[STARTED] Wating for connection')

    # set one thread for looking new connection 
    ACCEPT_THREAD =Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()

    #close the "server" socket
    SERVER.close()










