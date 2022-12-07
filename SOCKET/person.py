class Person:

    def __init__(self, addr, client_socket):
        self.addr = addr
        self.client_socket = client_socket
        self.name = None

    def set_name(self, name):
        self.name = name
    
    def __repr__(self):
        """
        the function return the Socket adress of "clien_socket" and the name of the person
        """
        return f"Person ({self.addr}, {self.name})"


