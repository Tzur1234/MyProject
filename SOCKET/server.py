from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
import datetime
from person import Person
import sys


# server_socket adress
HOST = ''
PORT = 1234
ADDR = (HOST, PORT)

# before each message : 10 charechters represet length
HEADER_LENGTH = 10

# max connections can listen at one time
MAX_CONNECTIONS = 10

# hold all of the client sockets
person = []

# initiate server for the first time __ set adress
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)



def wait_for_connection():
    """
    always look for new connections
    For each new connection (client_socket) initialize new thread 
    Each thread mange communication with each person
    """
    while True:
        try:
            client_socket, addr = SERVER.accept() #won continue till accept new connection event

            #Create a new person object - store the user data
            p = Person(addr, client_socket)
            person.append(p) 

            print(f"New connection from {addr[0]} : {addr[1]} at {datetime.datetime.now()}")

            # New thread for new client
            print("Start new threading to -> client_communicatino()")
            Thread(target=client_communication, args=(p,)).start()

        except Exception as e:
            print(f"Problem with wait_for_connection() \n  || {str(e)}")
            break





def client_communication(p):
    """
    Thread that handle all the messages from the client
    INPUT: receive the p object that has the client's socket
    """
    client_socket = p.client_socket
    addr = p.addr

    # first meesage - must be username
    try:
        username_header_length = int(client_socket.recv(HEADER_LENGTH).decode('utf-8'))
        username = client_socket.recv(username_header_length).decode('utf-8')
        print(f"Received the first mssasge - from {addr[0]} : {addr[1]} || username {username}")

        #set p username
        p.set_name(username)
    except:
        sys.exit("Fail to recv() the username |client_communication ()")

    # always check for new message from the specific person
    while True:
        
        try:
            print("wait for a message ...")
            msg_length = client_socket.recv(HEADER_LENGTH)
            
            
            # if there is no message -the client has closed the connection
            if not len(msg_length):
                print(f"{username} from {addr[0]} : {addr[1]} has closed the connection")

                client_socket.close() #close socket

                person.remove(p) #remove from the list

                break  # stop looking for messages from him
            else:
                msg_length = int(msg_length.decode('utf-8'))
                msg = client_socket.recv(msg_length).decode('utf-8')

                if msg == "{quit}":
                    print(f"{username} from {addr[0]} : {addr[1]} has closed the connection")
                    p.client_socket.close()             
                

                print(f"{username} : {msg}")



                broadcast(msg, username, p)
        except Exception as e:
            print(f"Failed with recv() message | client_communication() |\n {str(e)}")





def broadcast(msg, username, obj):
    """
    Iterate over all of the connected clients
    for each client send the message with header

    INPUT : msg(str) | username(str)
    RTURN: non
    """
    
    for p in person:
        if obj != p:

            client_socket = p.client_socket

            #create header:
            username_header  = f'{len(username):<{HEADER_LENGTH}}'.encode('utf-8') 
            username  = username.encode('utf-8') 

            msg_header = f'{len(msg):<{HEADER_LENGTH}}'.encode('utf-8') 
            msg  = msg.encode('utf-8') 


            try:
                client_socket.send(username_header +  username + msg_header + msg)

            except Exception as e:
                print(f"the user {p.mae} didn't recieve the message | broadcast()" , str(e))


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) # now server listen for connections
    print("SERVER is running ... waiting for new connections")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
































