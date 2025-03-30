# Dining Philosophers Problem

## Introduction  
The Dining Philosophers problem is a classic synchronization problem in computer science, formulated by Edsger Dijkstra in 1965. It illustrates the challenges of resource allocation and avoiding deadlocks in concurrent programming.  

## Implementation  
This solution implements the Dining Philosophers problem using C++ and `std::thread` for multithreading. The program ensures that philosophers alternate between thinking and eating while avoiding deadlocks.  

### Key Features  
- Uses `std::thread` for concurrency  
- Implements manual synchronization using mutexes  
- Prevents deadlock through a structured locking mechanism  
- Logs each philosopher's state in the console  

### Code Snippet  
```cpp
void philosopher(int id) {
    while (true) {
        think(id);
        pick_up_forks(id);
        eat(id);
        put_down_forks(id);
    }
}
```

Execution

The program takes the number of philosophers as a command-line argument:

./dining_philosophers 5

Each philosopher will continuously think and eat, with console outputs indicating their state.

Conclusion

This implementation ensures that all philosophers get a chance to eat while preventing deadlocks. The alternating fork acquisition strategy provides a simple yet effective way to handle concurrent resource allocation.

# Projekt 2 - Wielowątkowy serwer czatu

🇵🇱
Projekt został napisany przy użyciu bibliotek customtkinter oraz threading w Pythonie.
Wymagania projektu:
- Osobny watek dla kazdego polaczenia od klienta
- Serwer dba o synchrinizacje wiadomosci od klientow
- Klient widzi wiadomosci w czacie
- Klient ma mozliwosc wysylania wiadomosci 

Opcjonalne funkcjonalności:
- Kod spełnia wymagania lintera
- Jest interfejs graficzna
- Automatyzacja budowy projektu

🇺🇸
Project was written in Python using customtkinter and threading libraries.
Project requirements:
- Every thread has separate connections from clients
- Server synchronizes messages from clients
- Client can see messages inside chat
- Client can send messages

Optional functionalities:
- Code suffies linter's requirements
- App has a GUI
- Automated build of project

🇷🇸
Пројект је был написаны в Питону и користаје библиотеки customtkinter и threading.
Вымагања пројекта:
- Особна нитка дља каждого свеза од клиента
- Сервер зајмаје се синхронизацију послањ од клиентов
- Клиент гледаје послања в чату
- Клиент има можност посылања вєдомости

Опционалне функције:
- Код изполњаје измагања линтера
- Има графичны интерфејс
- Автоматична будова пројекта
