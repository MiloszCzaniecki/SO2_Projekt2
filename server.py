import threading
import socket
import argparse
import os
import sys

HOST = '127.0.0.1'
PORT = 9090

class Server(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.nicknames = []
        self.host = host
        self.port = port

    # every connected client receives a message
    def broadcast(self, message, source):
        for client in self.connections:
            if source is None or client.sockname != source:
                client.send(message)

    # creating socket to enable server work
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(1)
        print(f"Serwer pracuje na {sock.getsockname()}")

        while True:
            sc, sockname = sock.accept()
            print(f"Nowe polaczenie od {sc.getpeername()} do {sc.getsockname()}")

            # introducing usernames (required input)
            sc.send("Uzytkownik\n".encode('utf-8'))
            nickname = sc.recv(1024).decode('utf-8').strip()

            # creation of separate THREAD for new client
            server_socket = ServerSocket(sc, sockname, self, nickname)
            server_socket.start()

            # adding info about new client
            self.connections.append(server_socket)
            self.nicknames.append(nickname)

            self.broadcast(f"{nickname} zostal polaczony(a) z serwerem\n".encode('utf-8'), None)

    def remove_connection(self, connection):
        if connection in self.connections:
            index = self.connections.index(connection)
            nickname=self.nicknames[index]

            # removing user data
            self.connections.remove(connection)
            self.nicknames.pop(index)

            self.broadcast(f"{nickname} odlaczyl(a) sie od serwera\n".encode('utf-8'), None)


    def get_nickname(self, sockname):
        for index, connection in enumerate(self.connections):
            if connection.sockname == sockname:
                return self.nicknames[index]
        return "Nie ma takiego uzytkownika"


class ServerSocket(threading.Thread):

    def __init__(self, sc, sockname, server, nickname):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server
        self.nickname = nickname


    def run(self):
        while True:
            try:
                message = self.sc.recv(1024)

                if message:
                    formatted_message = f"{self.nickname}: {message.decode('utf-8')}"
                    print(formatted_message)

                    # one group chat for all users
                    self.server.broadcast(formatted_message.encode('utf-8'), self.sockname)
                else:
                    print(f"Zamknieto polaczenie z {self.nickname}")
                    self.sc.close()
                    self.server.remove_connection(self)
                    return
            except Exception as e:
                print(f"Blad odbioru wiadomosci od {self.nickname}: {e}")
                self.sc.close()
                self.server.remove_connection(self)
                return

    def send(self, message):
        # wyslanie wiadomosci do klienta
        try:
            self.sc.sendall(message)
        except Exception as e:
            print(f"Blad przy wysylaniu wiadomosci do {self.nickname}: {e}")
            self.sc.close()
            self.server.remove_connection(self)


def exit_server(server):
    while True:
        cmd = input("")
        if cmd.lower() == "q":
            print("Zamykanie wszystkich polaczen")
            for client in server.connections:
                client.sc.close()
            print("Wylaczanie serwery")
            sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Serwer czatu")
    parser.add_argument('--host', default='127.0.0.1', help='Localhost - nasluchiwany adres')
    parser.add_argument('-p', '--port', type=int, default=9090, help='Port TCP (domyslnie 9090)')

    args = parser.parse_args()

    # creation of main server thread
    server = Server(args.host, args.port)
    server.start()

    # thread for closing the server
    exit_thread = threading.Thread(target=exit_server, args=(server,))
    exit_thread.start()



