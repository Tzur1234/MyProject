from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, Lock
import datetime
import sys





class Client: 

    

    def __init__(self, name):

        # CLIENT SOCKET SETTING
        self.IP = 'localhost'
        self.PORT = 1234
        self.ADDR = (self.IP, self.PORT)
               
        self.HEADER_LENGTH = 10
        self.lock = Lock()
        self.name = name

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        
        self.send_msg(name)
        Thread(target=self.recv_msg).start()




    def recv_msg(self):
        """
        The function always checking out for new messages 
        if SERVER is close - close the socket
        """
        
        while True:
            try:
                    
                username_header = self.client_socket.recv(self.HEADER_LENGTH)
                if not len(username_header):
                        self.disconnect()
                else:
                    username_header = int(username_header.decode('utf-8'))
                    username = self.client_socket.recv(username_header).decode('utf-8')

                    header_msg = self.client_socket.recv(self.HEADER_LENGTH)
                    header_msg = int(header_msg.decode('utf-8'))
                    msg = self.client_socket.recv(header_msg).decode('utf-8')

                    print(f" -- {username} -- : {msg}")

                    # Safe acess to the memory
                    self.lock.acquire()
                    self.messages.append(msg)
                    self.lock.release()

            except Exception as e:
                print(f"client.py/ recv_msg() ||| {str(e)} ")
        



    def send_msg(self, msg):
        """
        The the function send the message to the server
        INPUT: string mag
        OUTPUT: None
        """
        if msg == "{quit}":
            print(f"Close {self.name} SOCKET")
            self.disconnect()
        else:
            username_header = self.convert(self.name)
            username = self.name.encode('utf-8')

            msg_header = self.convert(msg)
            msg = msg.encode('utf-8')

            try:
                # print(f" Try to send the mesage: {username_header + username + msg_header + msg}")
                self.client_socket.send(username_header + username + msg_header + msg)
            except:
                print("client.py / broadcast() ||| Could not send the message !")


    def get_msg(self):
        """
        return all the last messages send to the client socket
        """
        #safe acess to the memory
        self.lock.acquire()
        copy_messages = self.messages
        self.lock.release()

        self.messages = []

        return copy_messages


    def convert(self, st):
        """
        INPUT: a string
        OPUTPUT: a 10 charecters represent the length of the string in bytes format 
        """
        return f'{len(st):<{self.HEADER_LENGTH}}'.encode('utf-8')



    def disconnect(self):
        """
        deleate the socket of the client
        """
        self.client_socket.close()
        self.messages = []
        

