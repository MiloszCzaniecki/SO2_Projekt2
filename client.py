import threading
import socket
import argparse
import sys
import tkinter as tk
from tkinter import scrolledtext, simpledialog

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = None
        self.gui_done = False
        self.running = True
        self.message_buffer = []  # Buffer for archive messages before GUI is ready

    def connect(self):
        print(f"Łączenie z {self.host}:{self.port}...")
        try:
            self.sock.connect((self.host, self.port))
            print(f"Połączono z {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Nie udało się połączyć: {e}")
            return False

    def start(self):
        if not self.connect():
            return

        root = tk.Tk()
        root.withdraw()
        self.nickname = simpledialog.askstring("Nazwa użytkownika", "Podaj nazwę:", parent=root)

        if not self.nickname:
            print("Nie podano imienia – zakończono")
            self.sock.close()
            return

        print(f"Witaj {self.nickname}")

        gui_thread = threading.Thread(target=self.gui_loop)
        gui_thread.daemon = True
        gui_thread.start()

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.daemon = True
        receive_thread.start()

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
        self.msg_label = tk.Label(frame_input, text="Wiadomość:", bg="lightgray", font=("Arial", 12))
        self.msg_label.pack(anchor="w", padx=20, pady=5)

        input_frame = tk.Frame(frame_input)
        self.input_area = tk.Text(input_frame, height=3)
        self.input_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 5), pady=5)
        self.input_area.bind("<Return>", self.handle_return)

        self.send_button = tk.Button(input_frame, text="Wyślij", command=self.write, font=("Arial", 12))
        self.send_button.pack(side=tk.RIGHT, padx=(5, 20), pady=5)

        input_frame.pack(fill=tk.X)
        frame_input.pack(fill=tk.X)

        status_frame = tk.Frame(self.win, bg="lightgray")
        self.status_label = tk.Label(status_frame, text=f"Zalogowany jako: {self.nickname}", bg="lightgray", font=("Arial", 10))
        self.status_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.exit_button = tk.Button(status_frame, text="Wyjdź", command=self.stop, font=("Arial", 10))
        self.exit_button.pack(side=tk.RIGHT, padx=20, pady=10)

        status_frame.pack(fill=tk.X)

        self.win.geometry("600x500")
        self.gui_done = True

        # Display messages from the buffer
        for msg in self.message_buffer:
            self.display_message(msg)
        self.message_buffer.clear()

        self.win.mainloop()

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')

                if message.strip() == "Uzytkownik":
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.display_message(message)
                    else:
                        self.message_buffer.append(message)
            except ConnectionAbortedError:
                break
            except Exception as e:
                print(f"Błąd odbioru: {e}")
                if self.running:
                    self.display_system_message("Utracono połączenie z serwerem")
                    self.stop()
                break

    def handle_return(self, event):
        if not event.state & 0x1:
            self.write()
            return "break"
        return None

    def write(self):
        message = self.input_area.get('1.0', 'end-1c').strip()
        if message:
            if message.upper() == "QUIT":
                self.send_message("opuścił czat", system=True)
                self.stop()
            else:
                self.send_message(message)
        self.input_area.delete('1.0', 'end')
        self.input_area.focus()

    def send_message(self, message, system=False):
        try:
            to_send = f"System: {self.nickname} {message}" if system else message
            self.sock.send(to_send.encode('utf-8'))
        except Exception as e:
            print(f"Błąd wysyłania: {e}")
            self.display_system_message("Nie można wysłać wiadomości")

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert('end', message.strip() + "\n")
        self.text_area.yview('end')
        self.text_area.config(state='disabled')

    def display_system_message(self, message):
        if self.gui_done:
            self.text_area.config(state='normal')
            self.text_area.insert('end', f"*** {message} ***\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')

    def stop(self):
        print("Zamykanie klienta")
        self.running = False
        if hasattr(self, 'win') and self.win:
            self.win.destroy()
        self.sock.close()
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Klient czatu")
    parser.add_argument('host', nargs='?', default='127.0.0.1', help='Adres serwera')
    parser.add_argument('-p', '--port', type=int, default=9090, help='Port TCP (domyślnie 9090)')
    args = parser.parse_args()

    client = Client(args.host, args.port)
    try:
        client.start()
        while client.running:
            pass
    except KeyboardInterrupt:
        print("\nPrzerwano przez użytkownika")
        client.stop()
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")
        client.stop()

if __name__ == '__main__':
    main()
