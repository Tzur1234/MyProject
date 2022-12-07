import socket
import select
import errno # for getting a specific merror message when we are not connected to the server
import sys


HEADER_LENGTH = 10

IP = 'localhost'
PORT = 1234

my_username = input("Username: ")

#initialize client socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP,PORT))


# set the socket block mode to - non-blocking - setblocking(0)
# otherwise, if the program is under blocking mode (setblocking(1)) the program execution will stop till the
#  send() or recv() function will be finished
# when we set socket.setblocking(0) , if it's not ready for the operation, then socket.error is raised. (but we don't care if that happens)

client_socket.setblocking(False)


# First message to the server: username
username = my_username.encode('utf-8')
username_header = f"{len(my_username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)



#receive & send message
while True:
    #send message
    message = input(f"{my_username} > ")

    if message:
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message.encode('utf-8'))
    
    try:    
        #recieve things
        while True:
            user_header = client_socket.recv(HEADER_LENGTH)
            if not len(user_header):
                print("the connection with the server has been closed")
                client_socket.close()
                sys.exit("the connection with the server as been closed")
            
            username_length = int(user_header.decode('utf-8'))
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8'))
            message = client_socket.recv(message_length).decode('utf-8')


            # print the the received message
            print(f"{username} : {message}")


    except IOError  as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print(f"Reading error : {str(e)}")
            client_socket.close()
            sys.exit()
        else:
            continue 
            #if the socket was block - we don't care - just continue (remeber setblocking(False))    


    except Exception as e:
        print(f"General error : {str(e)}")
        client_socket.close()
        sys.exit()

















