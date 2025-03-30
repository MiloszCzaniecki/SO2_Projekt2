#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <vector>
#include <chrono>

using namespace std;

class DiningPhilosophers {
private:
    int num_philosophers;
    vector<mutex> forks; 
    vector<condition_variable> conditions;
    vector<bool> eating;
    mutex output_mutex;

public:
    DiningPhilosophers(int n) : num_philosophers(n), forks(n), conditions(n), eating(n, false) {}

    void philosopher(int id) {
        while (true) {
            think(id);
            pick_up_forks(id);
            eat(id);
            put_down_forks(id);
        }
    }

    void think(int id) {
        lock_guard<mutex> lock(output_mutex);
        cout << "Philosopher " << id << " is thinking.\n";
        this_thread::sleep_for(chrono::milliseconds(1000));
    }

    void pick_up_forks(int id) {
        unique_lock<mutex> left_lock(forks[id]);
        unique_lock<mutex> right_lock(forks[(id + 1) % num_philosophers]);

        conditions[id].wait(left_lock, [this, id] { return !eating[id]; });
        conditions[(id + 1) % num_philosophers].wait(right_lock, [this, id] { return !eating[(id + 1) % num_philosophers]; });

        eating[id] = true;
    }

    void eat(int id) {
        lock_guard<mutex> lock(output_mutex);
        cout << "Philosopher " << id << " is eating.\n";
        this_thread::sleep_for(chrono::milliseconds(1000));
    }

    void put_down_forks(int id) {
        unique_lock<mutex> left_lock(forks[id]);
        unique_lock<mutex> right_lock(forks[(id + 1) % num_philosophers]);

        eating[id] = false;

        conditions[id].notify_one();
        conditions[(id + 1) % num_philosophers].notify_one();
    }
};

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <number_of_philosophers>\n";
        return 1;
    }

    int num_philosophers = stoi(argv[1]);
    DiningPhilosophers dp(num_philosophers);
    vector<thread> philosophers;

    for (int i = 0; i < num_philosophers; i++)
        philosophers.emplace_back(&DiningPhilosophers::philosopher, &dp, i);

    for (auto& t : philosophers)
        t.join();

    return 0;
}
