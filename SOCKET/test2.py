import sys
import os
from client import Client
from threading import Thread

c2 = Client("James")

for _ in range(10):
    b = c2.send_msg(input("> "))
    if not b:
        exit()

print("XXX")
