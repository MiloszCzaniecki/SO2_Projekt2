import threading
import socket
import argparse
import sys
import tkinter as tk
from tkinter import scrolledtext, simpledialog

# python client.py 127.0.0.1 -p 9090
class Client:

    def __init__(self, host, port):
        self.host = host
        self.port=port
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname=None
        self.gui_done=False
        self.running=True


    def connect(self):
        print(f"Laczenie sie z {self.host}:{self.port}...")
        try:
            self.sock.connect((self.host, self.port))
            print(f"Pomyslnie polaczono z {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Nie udalo sie polaczyc z powodu: {e}")
            return False