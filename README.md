# Projekt 2 - Wielowątkowy serwer czatu

## Autorzy

Miłosz Czaniecki 272872
Iwo Staykov 259259

## Opis

Projekt implementuje prosty, wielowątkowy serwer czatu, umożliwiający wielu użytkownikom jednoczesne komunikowanie się. Składa się z dwóch programów:

- `server.py` – obsługuje połączenia klientów i rozsyła wiadomości
- `client.py` – umożliwia użytkownikom dołączanie do czatu i wysyłanie wiadomości

## Wymagania

- Python 3.x
- Biblioteki standardowe: `socket`, `threading`, `argparse`, `sys`, `tkinter`

## Instalacja i uruchomienie

### Serwer

1. Uruchom serwer czatu:
   ```sh
   python server.py --host 127.0.0.1 -p 9090
   ```
   Argumenty:

- --host – adres IP, na którym nasłuchuje serwer (domyślnie 127.0.0.1)

- -p, --port – numer portu (domyślnie 9090)

2. Aby zakończyć działanie serwera, wpisz q w konsoli.

### Klient

1. Uruchom klienta:

```bash
python client.py 127.0.0.1 -p 9090
```

Argumenty:

- host – adres IP serwera (domyślnie 127.0.0.1)

- -p, --port – numer portu (domyślnie 9090)

2. Po uruchomieniu program poprosi o podanie nazwy użytkownika.

## Funkcjonalności programu

### Server.py

- Obsługuje wielu klientów jednocześnie przy użyciu wątków.
- Każdy klient dostaje unikalną nazwę użytkownika.
- Wysyła wiadomości do wszystkich użytkowników w pokoju czatu.
- Informuje, gdy użytkownik dołącza lub opuszcza czat.
- Obsługuje komendę q, aby zamknąć serwer i zakończyć wszystkie połączenia.
- Archiwizuje wysyłane wiadomości, aby nowi użytkownicy mogli je zobaczyć po dołączeniu.
- Zapewnia synchronizację dostępu do wspólnych zasobów serwera.

### Client.py

- Łączy się z serwerem czatu.
- Pozwala użytkownikowi wysyłać i odbierać wiadomości.
- Obsługuje graficzny interfejs użytkownika z wykorzystaniem tkinter.
- Automatycznie przewija okno czatu po otrzymaniu nowych wiadomości.
- Wysyłanie wiadomości odbywa się po kliknięciu przycisku lub naciśnięciu Enter.
- Obsługuje komunikaty systemowe o dołączaniu i opuszczaniu użytkowników.
- Wyświetla wcześniejsze wiadomości czatu po dołączeniu nowego użytkownika.

## Działanie serwera

### Tworzenie serwera

```cpp
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((self.host, self.port))
sock.listen(1)
```

Serwer tworzy gniazdo (socket), przypisuje je do podanego hosta i portu, a następnie oczekuje na połączenia klientów (sock.listen(1)).

### Obsługa nowego klienta

```cpp
sc, sockname = sock.accept()
print(f"Nowe polaczenie od {sc.getpeername()} do {sc.getsockname()}")

sc.send("Uzytkownik\n".encode('utf-8'))
nickname = sc.recv(1024).decode('utf-8').strip()
```

Po zaakceptowaniu nowego połączenia serwer wysyła prośbę o podanie nazwy użytkownika i oczekuje na jej przesłanie przez klienta.

### Tworzenie wątku klienta

```cpp
server_socket = ServerSocket(sc, sockname, self, nickname)
server_socket.start()
```

Dla każdego nowego klienta tworzony jest osobny wątek ServerSocket, który obsługuje jego wiadomości.

### Rozsyłanie wiadomości

```cpp
def broadcast(self, message, source):
    for client in self.connections:
        if source is None or client.sockname != source:
            client.send(message)
```

Serwer wysyła wiadomość do wszystkich klientów poza nadawcą.

## Działanie klienta

### Łączenie z serwerem

```cpp
self.sock.connect((self.host, self.port))
```

Gniazdo klienta łączy się z serwerem przy użyciu podanego adresu i portu.

### Interfejs użytkownika

```cpp
self.win = tk.Tk()
self.text_area = scrolledtext.ScrolledText(frame_messages)
self.input_area = tk.Text(input_frame, height=3)
self.send_button = tk.Button(input_frame, text="Wyslij", command=self.write)
```

Klient posiada interfejs tkinter z polem tekstowym do wyświetlania wiadomości i przyciskiem do wysyłania wiadomości.

### Obsługa odbierania wiadomości

```cpp
def receive(self):
    while self.running:
        message = self.sock.recv(1024).decode('utf-8')
        self.text_area.insert('end', message + "\n")
```

Wątek receive() działa w tle i nasłuchuje na nowe wiadomości, które są wyświetlane w polu tekstowym.

### Usługa wysyłania wiadomości

```cpp
def write(self):
    message = self.input_area.get('1.0', 'end-1c').strip()
    self.sock.send(message.encode('utf-8'))
```

Po naciśnięciu przycisku "Wyślij" wiadomość jest kodowana i przesyłana do serwera.

## Implementacja archiwizacji

Aby nowo dołączający użytkownik mógł zobaczyć historię wcześniejszych wiadomości:

- Na serwerze (server.py) została utworzona lista self.message_history, przechowująca ostatnie wiadomości czatu (z limitem 100 wiadomości).

- Po odebraniu nazwy użytkownika i utworzeniu nowego wątku klienta (ServerSocket), serwer wysyła zgromadzone wiadomości do nowego klienta.

```cpp
with self.server.lock:
    for msg in self.server.message_history:
        self.send(msg)
```

Po odebraniu wiadomości klient buforuje je, jeśli GUI jeszcze nie jest gotowe, a następnie wyświetla w oknie czatu po jego załadowaniu.
Dzięki temu nowy użytkownik natychmiast widzi rozmowy prowadzone przed jego dołączeniem.

## Implementacja synchronizacji

Ze względu na wielowątkowość serwera, konieczne było zastosowanie synchronizacji dostępu do wspólnych zasobów (self.connections, self.nicknames, self.message_history).

W tym celu:

- W serwerze (server.py) utworzono obiekt blokady:

```cpp
self.lock = threading.Lock()
```

- Każde modyfikowanie lub odczytanie wspólnych zasobów odbywa się wewnątrz sekcji krytycznej:

```cpp
with self.lock:
    self.message_history.append(message)
```

lub

```cpp
with self.lock:
    self.connections.append(server_socket)
    self.nicknames.append(nickname)
```

Funkcja broadcast() również korzysta z tej blokady, aby wszystkie operacje wysyłania wiadomości były spójne i nie powodowały kolizji między wątkami.

Dzięki temu serwer zachowuje stabilność i poprawność działania nawet przy wielu jednoczesnych klientach.
