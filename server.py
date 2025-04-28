import threading
import socket
import argparse
import sys

class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.nicknames = []
        self.host = host
        self.port = port
        self.message_history = []
        self.history_limit = 100
        self.lock = threading.Lock()

    def broadcast(self, message, source):
        with self.lock:
            self.message_history.append(message)
            if len(self.message_history) > self.history_limit:
                self.message_history.pop(0)
            for client in self.connections:
                client.send(message)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(1)
        print(f"Serwer pracuje na {sock.getsockname()}")

        while True:
            sc, sockname = sock.accept()
            print(f"Nowe połączenie od {sc.getpeername()} do {sc.getsockname()}")

            sc.send("Uzytkownik\n".encode('utf-8'))
            nickname = sc.recv(1024).decode('utf-8').strip()

            server_socket = ServerSocket(sc, sockname, self, nickname)
            server_socket.start()

            with self.lock:
                self.connections.append(server_socket)
                self.nicknames.append(nickname)

            self.broadcast(f"\n{nickname} dołączył(a) do czatu\n".encode('utf-8'), None)

    def remove_connection(self, connection):
        with self.lock:
            if connection in self.connections:
                index = self.connections.index(connection)
                nickname = self.nicknames[index]
                self.connections.remove(connection)
                self.nicknames.pop(index)
                self.broadcast(f"{nickname} opuścił(a) czat\n".encode('utf-8'), None)

    def get_nickname(self, sockname):
        for index, connection in enumerate(self.connections):
            if connection.sockname == sockname:
                return self.nicknames[index]
        return "Nie ma takiego użytkownika"


class ServerSocket(threading.Thread):
    def __init__(self, sc, sockname, server, nickname):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server
        self.nickname = nickname

    def run(self):
        # Send message history
        with self.server.lock:
            for msg in self.server.message_history:
                self.send(msg)

        while True:
            try:
                message = self.sc.recv(1024)
                if message:
                    formatted_message = f"{self.nickname}: {message.decode('utf-8')}"
                    print(formatted_message)
                    self.server.broadcast(formatted_message.encode('utf-8'), self.sockname)
                else:
                    print(f"Zamknięto połączenie z {self.nickname}")
                    self.sc.close()
                    self.server.remove_connection(self)
                    return
            except Exception as e:
                print(f"Błąd odbioru wiadomości od {self.nickname}: {e}")
                self.sc.close()
                self.server.remove_connection(self)
                return

    def send(self, message):
        try:
            with threading.Lock():  # Local lock, could also be a class-wide lock
                self.sc.sendall(message)
        except Exception as e:
            print(f"Błąd przy wysyłaniu do {self.nickname}: {e}")
            self.sc.close()
            self.server.remove_connection(self)



def exit_server(server):
    while True:
        cmd = input("")
        if cmd.lower() == "q":
            print("Zamykanie wszystkich połączeń")
            for client in server.connections:
                client.sc.close()
            print("Wyłączanie serwera")
            sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Serwer czatu")
    parser.add_argument('--host', default='127.0.0.1', help='Adres nasłuchiwania')
    parser.add_argument('-p', '--port', type=int, default=9090, help='Port TCP')

    args = parser.parse_args()

    server = Server(args.host, args.port)
    server.start()

    exit_thread = threading.Thread(target=exit_server, args=(server,))
    exit_thread.start()
