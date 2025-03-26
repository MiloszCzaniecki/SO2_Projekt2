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
    
    def gui_loop(self):
            self.win = tk.Tk()
            self.win.title("Klient czatu")
            self.win.configure(bg="lightgray")
            self.win.protocol("WM_DELETE_WINDOW", self.stop)

            frame_messages = tk.Frame(self.win)
            self.chat_label = tk.Label(frame_messages, text="Czat:", bg="lightgray", font=("Arial", 12))
            self.chat_label.pack(anchor="w", padx=20, pady=5)
            self.text_area = scrolledtext.ScrolledText(frame_messages)
            self.text_area.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
            self.text_area.config(state='disabled')
            frame_messages.pack(fill=tk.BOTH, expand=True)

            frame_input = tk.Frame(self.win, bg="lightgray")
            self.msg_label = tk.Label(frame_input, text="Wiadomosc: ", bg="lightgray", font=("Arial", 12))
            self.msg_label.pack(anchor="w", padx=20, pady=5)

            input_frame = tk.Frame(frame_input)
            self.input_area = tk.Text(input_frame, height=3)
            self.input_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20,5), pady=5)
            self.input_area.bind("<Return>", self.handle_return)

            self.send_button = tk.Button(input_frame, text="Wyslij", command=self.write, font=("Arial",12))
            self.send_button.pack(side=tk.RIGHT, padx=(5,20), pady=5)

            input_frame.pack(fill=tk.X)
            frame_input.pack(fill=tk.X)

            status_frame = tk.Frame(self.win, bg="lightgray")
            self.status_label = tk.Label(status_frame, text=f"Zalogowany jako: {self.nickname}", bg="lightgray", font=("Arial", 10))
            self.status_label.pack(side=tk.LEFT, padx=20, pady=10)

            self.exit_button=tk.Button(status_frame, text="Wyjdz", command=self.stop, font=("Arial", 10))
            self.exit_button.pack(side=tk.RIGHT, padx=20, pady=10)

            status_frame.pack(fill=tk.X)

            self.win.geometry("600x500")
            self.gui_done=True
            self.win.mainloop()
    
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
