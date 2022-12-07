import sys
import os
from client import Client
from threading import Thread

c1 = Client("Tzur")

for _ in range(10):
    b = c1.send_msg(input("> "))
    if not b:
        exit()

print("XXX")
