# import
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, Lock
from person import Person
import sys
import datetime


# server_socket adress
IP = 'localhost'
PORT = 1235
ADDR = (IP, PORT)


MAX_CONNECTIONS = 5

HEADER_LENGTH = 10

# server setting
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


person = []


#####################################################################################################

def wait_for_connection():
    """
    the function create a new Thread for each new SOCKET_CLIENT connection
    INPUT : None
    OUTPUT : None
    """
    while True:
        try:
            client_socket, addr = SERVER.accept()
            p = Person(client_socket, addr)
            person.append(p)

            print(f"Receive new connection from {addr[0]} : {addr[1]}")

            Thread(target=recieve_messages, args=(p,)).start()
        except Exception as _Err:
            print(f"server.py / wait_for_connection ||| Failed set new connection ! {str(_Err)}" )
            break


def recieve_messages(p):
    #recieve first message ( user name)

    client_socket = p.client_socket
    addr = p.addr

    try:
        header_msg = client_socket.recv(HEADER_LENGTH)
        if not len(header_msg):
            print(f"Client {addr[0]} : {addr[1]} Closed Connection")
            client_socket.close()
            person.remove(p)
        else:
            header_msg = int(header_msg.decode('utf-8'))
            username = client_socket.recv(header_msg).decode('utf-8')

            print(f" The received username : {username}")
            print("set username ...")
            p.set_name(username)


    except Exception as e:
        print(f"|Recived the username Failed ! {str(e)}")
        client_socket.close()
        person.remove(p)
        return None

    #Infinte loop
    while True:

        try:
            print("wait for new msg ...")

            username_header = client_socket.recv(HEADER_LENGTH)
            
            
            if not len(username_header):
                print(f"Client {addr[0]} : {addr[1]} Closed Connection")
                client_socket.close()
                person.remove(p)
                break


            else:
                username_header = int(username_header.decode('utf-8'))
                username = client_socket.recv(username_header).decode('utf-8')

                header_msg = client_socket.recv(HEADER_LENGTH)
                header_msg = int(header_msg.decode('utf-8'))
                msg = client_socket.recv(header_msg).decode('utf-8')

                print(f"{username} : {msg}")

                # send the message to all client_sockets
                broadcast(msg, p)

        except Exception as e: 
                print(f"server.py / recieve_messages() | Coudln't recv() the message from {p.name} | {str(e)}")

                

def broadcast(msg, obj):
    """
    The function send the message to all of the users except the user who send the message
    """
    # translate the message + the username to bytes format
    username_header = convert(obj.name)
    username = obj.name.encode('utf-8')

    msg_header = convert(msg)
    msg = msg.encode('utf-8')

    for p in person:
        if p != obj:
            try:

                obj.client_socket.send(username_header + username + msg_header + msg)
            except Exception as e: 
                print(f"server.py / broadcast() | Coudln't send the message from {obj.name} to {p.name} ||| {str(e)}")





def convert(st):
    """
    INPUT: a string
    OPUTPUT: a 10 charecters represent the length of the string in bytes format 
    """
    return f'{len(st):<{HEADER_LENGTH}}'.encode('utf-8')



if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)
    print("Server initiated ! Wait for new connections !")
    THREAD = Thread(target=wait_for_connection)
    THREAD.start()
    THREAD.join()
    SERVER.close()


    