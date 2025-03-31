#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <vector>
#include <chrono>

using namespace std;

enum class State { THINKING, HUNGRY, EATING };

class DiningPhilosophers {
private:
    int num_philosophers;
    vector<mutex> forks;
    vector<State> states;
    vector<condition_variable> conditions;
    mutex table_mutex;
    mutex output_mutex;

public:
    DiningPhilosophers(int n) : num_philosophers(n), forks(n), states(n, State::THINKING), conditions(n) {}

    void philosopher(int id) {
        while (true) {
            think(id);
            pick_up_forks(id);
            eat(id);
            put_down_forks(id);
        }
    }

    // Simulate thinking process of a philosopher
    // This function is called when a philosopher is thinking
    void think(int id) {
        lock_guard<mutex> lock(output_mutex);
        cout << "Philosopher " << id << " is thinking.\n";
        this_thread::sleep_for(chrono::milliseconds(1000));
    }

    // Pick up forks and notify neighbors
    // This function is called when a philosopher wants to eat
    void pick_up_forks(int id) {
        unique_lock<mutex> lock(table_mutex);
        states[id] = State::HUNGRY;

        // Wait until both forks are available
        conditions[id].wait(lock, [this, id] { return can_eat(id); });

        states[id] = State::EATING;
    }

    // Eat the food
    // This function simulates the eating process of a philosopher
    void eat(int id) {
        lock_guard<mutex> lock(output_mutex);
        cout << "Philosopher " << id << " is eating.\n";
        this_thread::sleep_for(chrono::milliseconds(1000));
    }

    // Put down forks and notify neighbors
    // This function is called when a philosopher finishes eating
    void put_down_forks(int id) {
        unique_lock<mutex> lock(table_mutex);
        states[id] = State::THINKING;

        // Notify neighbors that forks are available
        conditions[left(id)].notify_one();
        conditions[right(id)].notify_one();
    }

    // Check if the philosopher can eat
    // A philosopher can eat if they are hungry and their left and right neighbors are not eating
    bool can_eat(int id) {
        return states[id] == State::HUNGRY &&
               states[left(id)] != State::EATING &&
               states[right(id)] != State::EATING;
    }

    // Helper functions to get the left and right philosopher indices
    int left(int id) { return (id + num_philosophers - 1) % num_philosophers; }
    int right(int id) { return (id + 1) % num_philosophers; }
};

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cerr << "Provide a number of philosophers.\n";
        return 1;
    }

    int num_philosophers = stoi(argv[1]);
    DiningPhilosophers dp(num_philosophers);
    vector<thread> philosophers;

    // Create threads for each philosopher
    // Each philosopher will run the philosopher function in a separate thread
    for (int i = 0; i < num_philosophers; i++)
        philosophers.emplace_back(&DiningPhilosophers::philosopher, &dp, i);

    // Wait for all philosophers to finish
    // This will not happen in this simulation as philosophers run indefinitely
    for (auto& t : philosophers)
        t.join();

    return 0;
}
