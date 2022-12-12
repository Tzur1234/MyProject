from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time


class Client:
    """
    for communication with server
    """
    HOST = "localhost"
    PORT = 5501
    ADDR = (HOST, PORT)
    # BUFSIZ = 512
    HEADER_LENGTH = 10
    messages = []

    def __init__(self, name):
        """
        Init object and send name to server
        :param name: str
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)

        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()

        self.send_message(name)
        self.lock = Lock()

    def receive_messages(self):
        """
        receive messages from server
        :return: None
        """
        while True:
            try:
                username = self.client_socket.recv(self.HEADER_LENGTH) # the name of the sender
                msg_lenght = self.client_socket.recv(self.HEADER_LENGTH) # the length of the message
                msg = self.convert_to_msg(username, msg_lenght) # check for new message

                # make sure memory is safe to access
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
                
            except Exception as e:
                print("[EXCPETION]", e)
                break

    def send_message(self, msg):
        """
        send messages to server
        :param msg: str
        :return: None
        """
        try:
            msg_convert = self.convert_to_b(msg)
            self.client_socket.send(msg_convert) 
            if msg == "{quit}":
                self.client_socket.close()
        except Exception as e:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)






    def convert_to_b(self, msg):
        """
        convert the msg to bytes form: header + msg
        INPUT : msg (str) , name (str)
        RETURN: bytes format of the message + header
        """
        msg_header = f'{len(msg):<{self.HEADER_LENGTH}}'.encode('utf-8')
        msg = msg.encode('utf-8') 
        return msg_header + msg

    def convert_to_msg(self, username, msg_lenght):
        """
        INPUT : username (bytes) and msg_length(bytes)
        convert the message from bytes format to string
        _ _ _ _ _ _ _ _ _ _ + _ _ _ _ _ _ _ _ _ _ + ____________________________
        return one string
        """
        username = username.decode('utf-8')
        msg_lenght = int(msg_lenght.decode('utf-8'))
        msg = self.client_socket.recv(msg_lenght).decode('utf-8')

        return username + msg  # return "tzur       : hello"




    def get_messages(self):
        """
        :returns a list of str messages
        :return: list[str]
        """
        messages_copy = self.messages[:]

        # make sure memory is safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()

        return messages_copy
    
    def disconnect(self):
        self.send_message("{quit}")