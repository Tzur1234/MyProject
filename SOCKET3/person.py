
class Person:

    def __init__(self , client_socket, addr):
        self.client_socket = client_socket
        self.addr = addr
        self.name = None

    def set_name(self, name):
        self.name = name
    
    def __repo__(self):
        return f"username: {self.name} | addr {self.addr[0]} : {self.addr[1]}"