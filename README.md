# Projekt 1 - Problem jedzących filozofów (Iwo Staykov)
Dining Philosophers Problem

Introduction

The Dining Philosophers problem is a classic synchronization problem used to illustrate the challenges of resource sharing and avoiding deadlocks in concurrent programming. The problem involves a set of philosophers sitting around a table, each alternating between thinking and eating. To eat, a philosopher must acquire two forks (one on their left and one on their right). The challenge is to prevent deadlocks while ensuring fairness in resource allocation.

Implementation

This implementation in C++ uses std::thread for concurrency and std::mutex for fork synchronization. The key aspects of the solution are:

Using mutexes for fork control: Each fork is represented by a std::mutex, ensuring exclusive access to resources.

Philosopher behavior:

A philosopher first thinks for a predefined time.

They then attempt to pick up two forks in a specific order (even-indexed philosophers pick the left fork first, while odd-indexed ones pick the right fork first) to avoid deadlock.

Once both forks are acquired, the philosopher eats and then releases the forks.

Avoiding deadlocks: The alternating fork-picking order ensures that at least one philosopher can proceed, preventing circular wait conditions.

Code Example

void eat(int id) {
    int left_fork = id;
    int right_fork = (id + 1) % num_philosophers;
    
    // Lock forks in a specific order to avoid deadlocks
    if (id % 2 == 0) {
        forks[left_fork].lock();
        forks[right_fork].lock();
    } else {
        forks[right_fork].lock();
        forks[left_fork].lock();
    }
    
    cout << "Philosopher " << id << " is eating.\n";
    this_thread::sleep_for(chrono::milliseconds(1000));
    
    // Unlock forks
    forks[left_fork].unlock();
    forks[right_fork].unlock();
}

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
