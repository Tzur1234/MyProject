from client import Client
import time
from threading import Thread

c1 = Client("ME")
c2 = Client("name")


def update_messages():
    """
    updates the *local* list of messages (c1)
    :return: None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1)  # update every 1/10 of a second
        new_messages = c1.get_messages()  # get any new messages from client
        msgs.extend(new_messages)  # add to the local list of messages

        for msg in new_messages:  # display new messages
            print(msg)

            if msg == "{quit}":
                run = False
                break


Thread(target=update_messages).start()

a = input("> ")
c1.send_message(a)

time.sleep(4)
c2.send_message("hello")

a = input("> ")
c1.send_message(a)

time.sleep(4)
c2.send_message("Nothing much")


time.sleep(2)
c1.disconnect()
time.sleep(2)
c2.disconnect()