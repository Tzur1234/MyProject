class Person():

    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def set_name(self, name):
        self.name = name
         

    def __reper__(self):
        return f"Person({self.addr},{self.name})"