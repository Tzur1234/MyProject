from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNETIONS = 10
BUFSIZ = 512
HEADER_LENGTH = 10

# GLOBAL VARIABLES
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)  # set up server


def broadcast(msg, name, obj):
    """
    send new messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return:
    """
    username = f'{name:<{HEADER_LENGTH}}'.encode('utf-8')

    for person in persons:
        
        if obj != person:
                        
            client = person.client
            try:
                client.send(username + msg)
            except Exception as e:
                print("[EXCEPTION]", e)


def client_communication(person):
    """
    Thread to handle all messages from client
    :param person: Person
    :return: None
    """
    client = person.client

    # first message received is always the persons name
    header_msg = client.recv(HEADER_LENGTH) #in bytes
    name = convert_to_s(person, header_msg) #in string
    person.set_name(name)

    msg = convert_to_b(f"{name} has joined the chat!") # convert to bytes the message
    broadcast(msg, "", person)  # broadcast welcome message

    while True:  # wait for any messages from person
        header_msg = client.recv(HEADER_LENGTH)
        msg = convert_to_s(person, header_msg)


        if msg == "{quit}":  # if message is qut disconnect client

            client.close()
            persons.remove(person)
            broadcast(convert_to_b(f"{name} has left the chat..."), "", person)
            print(f"[DISCONNECTED] {name} disconnected")
            break

        else:  # otherwise send message to all other clients
            msg = convert_to_b(msg) # convert back to bytes
            broadcast(msg, name +": ", person)
            print(f"{name}: ", msg.decode("utf8"))


def wait_for_connection():
    """
    Wait for connecton from new clients, start new thread once connected
    :return: None
    """

    while True:
        try:
            client, addr = SERVER.accept()  # wait for any new connections
            person = Person(addr, client)  # create new person for connection
            persons.append(person)

            print(f"[CONNECTION] {addr[0]} : {addr[1]} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()

        except Exception as e:
            print("[EXCEPTION]", e)
            break
    
    # this line will run only when exception has happened
    print("SERVER CRASHED")



def convert_to_b(msg):
    """
    convert the recived msg to bytes form: header + msg
    INPUT : msg (str) , name (str)
    RETURN: bytes format of the message + header
    """
    msg_header = f'{len(msg):<{HEADER_LENGTH}}'.encode('utf-8')
    msg = msg.encode('utf-8') 
    return msg_header + msg

def convert_to_s(obj , length):
    """
    INPUT: person object + the length of the message in bytes
    OUTPUT: a string of the message
    The function reade the message accordind to the length
    """
    # take the client socket
    client_socket = obj.client
    # translate the length from bytes -> int
    length = int(length.decode('utf-8'))
    
    # recv the message itself 
    msg = client_socket.recv(length).decode('utf-8') 
    
    # return the msg
    return msg 


if __name__ == "__main__":
    SERVER.listen(MAX_CONNETIONS)  # open server to listen for connections
    print("[STARTED] Waiting for connections...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()