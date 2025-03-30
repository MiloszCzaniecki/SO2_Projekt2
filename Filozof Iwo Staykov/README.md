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

## Execution

Compile the program with the following command 

```bash
g++ -std=c++11 dining_philosophers.cpp -o dining_philosophers -pthread
```
The program takes the number of philosophers as a command-line argument:

```bash
./dining_philosophers 5
```
Each philosopher will continuously think and eat, with console outputs indicating their state.

## Conclusion

This implementation ensures that all philosophers get a chance to eat while preventing deadlocks. The alternating fork acquisition strategy provides a simple yet effective way to handle concurrent resource allocation.