import socket
import select
import errno
import sys

HEADER_LENGTH = 10
IP = 'localhost'
PORT = 1234

#initialize socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# let the server socket to reconect to the same port every time
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

server_socket.bind((IP, PORT))

server_socket.listen()

#Creat list of client_sockets
# any time new client connnect to our server_socket, add their copy socket to the list
sockets_list = [server_socket]

#set a clinet's name dictionaries
# KEY - client_socket
#VALUE - user name (user data)
clients = {}

def receive_message(client_socket):
    """
    the function return the last received message
    input: client_socket
    output: a dictionary presentig the message
    if no message or Error araised - return false
    """
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        #if we didn't recicve any data ==> the client has closed his socket \ disconnected
        if not len(message_header):
            return False
        else:
            message_length = int(message_header.decode('utf-8'))
            return {"header": message_length, "data": client_socket.recv(message_length)}


    except Exception as e:
        print(str(e))
        return False


# The server can raize two types of message (events)
# 1. message for new connection 
# 2. messsage from exsiting client_socket


# always waitting for new event
while True:
    """
    always runing lookig for new message / connection
    """

    print("looking for new event")
    read_sockets, _, exception = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        
        # if the derver is ready for 
        # new connection
        if notified_socket == server_socket:
            client_socket, client_adress = server_socket.accept()

            # the first message from the user is always his name
            user = receive_message(client_socket)

            # the clinet has closed the message or error
            if user is False:
                continue 
            else:
                # add the user data to the clients dictionary (his name)
                # add the client_socket to the list
                clients[client_socket] = user
                sockets_list.append(client_socket)

                print(f"Accepted new connection from {client_adress[0]} : {client_adress[1]} username: {user['data'].decode('utf-8')}")

        else:

            # there is a message from a conected client

            message = receive_message(notified_socket)

            # no information = the client has disconnected
            if message is False:
                print(f"{clients[notified_socket]['data'].decode('utf-8')} has disconected")

                #delete from clients dict
                del clients[notified_socket]
                # remove from sockets_list the specific socket
                sockets_list.remove(notified_socket)

                continue
            else:
                user = clients[notified_socket]
                print(f"Recived messge from : {user['data'].decode('utf-8')} \n Message : {message['data'].decode('utf-8')}")

                # Share the message with every body , except the notified_socket

                for client_socket in clients:

                    # except the notified socket 
                    if client_socket != notified_socket:
                        try: 
                            # send the information of the user who send + the message 
                            # user['header'] + user['data'] == > the user name
                            # message['header'] + message['data'] ==> the message itself  
                                            
                            user_header = f"{user['data']:<{HEADER_LENGTH}}".encode('utf-8')
                            message_header = f"{message['data']:<{HEADER_LENGTH}}".encode('utf-8')
                            
                            # user_header = f"{user['data']:<{HEADER_LENGTH}}".encode('utf-8')
                            # message_header = f"{message['data']:<{HEADER_LENGTH}}".encode('utf-8')

                            client_socket.send(user_header + user['data'] + message_header + message['data'])
                        except Exception as e:
                            print(str(e))
                            sys.exit("Failed with sending all the messages")
        
    # take care for the exception sockets - delte them !
        for notified_socket in exception:
            #remove from all sockets_list & clients
            sockets_list.remove(notified_socket)
            del clients[notified_socket]


























                            







































