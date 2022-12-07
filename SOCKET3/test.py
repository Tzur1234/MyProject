from threading import Thread
from client import Client
import time 

c1 = Client("Tim")
c2 = Client("Tom")

def update_msg():
    """
    update the msg
    """

    msgs = []
    run = True
    while run:
        time.sleep(0.1)
        new_messages = c1.get_msg()
        msgs.extend(new_messages)

        for msg in new_messages:
            print(f"new message :: {msg}")
            
            if msg == '{quit}':
                run = False
                break
                



Thread(target=update_msg).start()

c1.send_msg("hello")
time.sleep(1)
c2.send_msg("hello")
time.sleep(1)
c1.send_msg("whats up")
time.sleep(1)
c2.send_msg("Nothing much")
time.sleep(1)

c1.disconnect()
time.sleep(2)
c2.disconnect()


 