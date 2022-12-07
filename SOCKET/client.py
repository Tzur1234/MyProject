from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Lock
import time
import sys



#Number of bytes of header
HEADER_LENGTH = 10

#Number of connection
MAX_CONNECTIONS = 5

class Client:
    """
    basic client for each new user wants to conect to the chat server
    """  
    #Server Socket Adress
    IP = 'localhost'
    PORT = 1234
    ADDR = (IP, PORT)
  
    # store incoming messages
    msg = []

    def __init__(self, name):

        lock = Lock()
        self.name = name

        #creat the client socket + connect to the server
        try:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)   
        except Exception as e:
            sys.exit(f'[client.py | __init__ | failed to connect the server |{str(e)}')
        
        #send the first message to the server = username
        try:
            name_header = self.convert(self.name)
            self.client_socket.send(name_header + self.name.encode('utf-8'))
        except Exception as e:
            sys.exit(f'[client.py | __init__ | failed to send first message - username |{str(e)}')

        # new thread tracking incoming messages
        t1 = Thread(target=self.receive_messages)
        t1.start()



    def receive_messages(self):
        """
        consistently read incoming messages form the server + store them in msg[] list
        message come from "broadcast" function in the server
        """
        try:
            while True:
                sender_header = self.client_socket.recv(HEADER_LENGTH)
                if not len(sender_header):
                    print("server closed connection ... close my socket know")
                    self.client_socket.close()
                    sys.exit()
                else:
                    sender_header_length = int(sender_header.decode('utf-8'))
                    username = self.client_socket.recv(sender_header_length).decode('utf-8')              

                
                message_header = self.client_socket.recv(HEADER_LENGTH)
                msg_header_length = int(message_header.decode('utf-8'))
                msg = self.client_socket.recv(msg_header_length).decode('utf-8') ## 

                print(f"{username} : {msg}")
                self.msg.append(msg) 



        except Exception as e:
            sys.exit(f"[client.py | receive_messages() | {str(e)}")


    

    def send_msg(self, msg):
        if msg == "{quit}":
            self.client_socket.send("".encode('utf-8'))
            print("close client socket |  client.py")
            self.client_socket.close()
            return False
        else:
            # the lenght of the message in ??******** format in bytes format
            msg_header = self.convert(msg)


            try:
                print(f"try to send the message: {msg}")                                        
                print(f"in bytes: {msg_header + bytes(msg, 'utf-8')}")                                        
                self.client_socket.send(msg_header + bytes(msg, 'utf-8'))
            except:
                print(f"send the message : {msg} \n Failed !")
            
        return True



    

    def get_messages(self):
        """
        empty the message list 
        return a copy of the last messages
        """
        # grab all the messages
        msg_copy = self.msg
        
        #empty the list
        self.msg = []

        return msg_copy


    # convert string msg to header_length in bytes format
    def convert(self, msg):
        return f'{len(msg):<{HEADER_LENGTH}}'.encode('utf-8')



##### to think again how can I make disconnectino
    def disconnect(self):
        self.client_socket.close()
        self.send_msg(f"{quit}")













