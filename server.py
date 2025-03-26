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
        
    def start(self):
        if not self.connect():
            return

        root = tk.Tk()
        root.withdraw()
        self.nickname = simpledialog.askstring("Nazwa uzytkownika", "Podaj nazwe uzytkownika", parent=root)

        if not self.nickname:
            print("Zamykam bo nie podales swojego imienia")
            self.sock.close()
            return

        print(f"Witaj {self.nickname}")

        # main thread of the app
        gui_thread = threading.Thread(target=self.gui_loop)
        gui_thread.daemon=True
        gui_thread.start()

        # thread for receiving messages
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.daemon = True
        receive_thread.start()

        # we checked whether user could successfully connect
        #self.send_message(f"Dolaczono do czatu", system=True)

        return gui_thread, receive_thread
    
def main():
    # required arguments to run app: (local)host and port
    #HOST = '127.0.0.1'
    #PORT = 9090
    parser = argparse.ArgumentParser(description="Klient czatu")
    parser.add_argument('host', nargs='?', default='127.0.0.1', help='Adres serwera')
    parser.add_argument('-p', '--port', type=int, default=9090, help='Port TCP (domyslnie 9090)')

    args = parser.parse_args()

    client = Client(args.host, args.port)
    try:
        # initializating connection with server
        client.start()
        while client.running:
            pass
        # gui and receiving threads constantly running
    except KeyboardInterrupt:
        print("\nPrzerwano przez uzytkownika")
        client.stop()
    except Exception as e:
        print(f"Nieoczekiwany blad: {e}")
        client.stop()

if __name__ == '__main__':
    main()
