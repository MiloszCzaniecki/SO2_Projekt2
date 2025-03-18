#include <iostream>
#include <random>
#include <thread>
#include <mutex>
using namespace std;

int num_phil = 5;
std::mt19937 rng;
std::mutex mtx;

int left_phil(int id_phil){
    return (id_phil-1+num_phil)%num_phil;
}

int right_phil(int id_phil){
    return (id_phil+1)%num_phil;
}

void thinking(int& thinking_time, int id_phil){ // action_id = 0
    cout << "Philosopher number " << id_phil << " is thinking for " << chrono::milliseconds(thinking_time).count() << endl;
}

void waiting(int& waiting_time, int id_phil){ // action_id = 1
    cout << "Philosopher number " << id_phil << " is waiting for " << chrono::milliseconds(waiting_time).count() << endl;
}

void taking_forks(int& taking_time, int id_phil){ // action_id = 2
    cout << "Philosopher number " << id_phil << " is picking up forks for " << chrono::milliseconds(taking_time).count() << endl;
}

void eating(int& eating_time, int id_phil){ // action_id = 3
    cout << "Philosopher number " << id_phil << " is eating for " << chrono::milliseconds(eating_time).count() << endl;
}

void returning_forks(int& returning_time, int id_phil){ // action_id = 4
    cout << "Philosopher number " << id_phil << " is putting forks away for " << chrono::milliseconds(returning_time).count() << endl;
}

void check_directions(){
    for(int i =0;i<num_phil;i++){
        std::cout << " lewy wobec niego " << left_phil(i) << " Obecny filozof " << i <<  " prawy wobec niego " << right_phil(i) << std::endl;
    }
}

void philosopher(int times_array[], int id_phil, mutex& mut, mutex& tex){
    int thinking_time = times_array[0];
    int waiting_time = times_array[1];
    int taking_time = times_array[2];
    int eating_time = times_array[3];
    int returning_time = times_array[4];

    while(true){
        // noone will forbid philosopher to think freely
        thinking_time = std::uniform_int_distribution<int>(1000, 2000)(rng);
        {
            std::lock_guard<std::mutex> g_thinking(mtx);
            thinking(thinking_time, id_phil);
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(thinking_time));

        // possible to trash
        waiting_time = std::uniform_int_distribution<int>(1000, 2000)(rng);
        std::lock_guard<std::mutex> g_waiting(mtx);
        {
            waiting(waiting_time, id_phil);
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(waiting_time));

        taking_time = std::uniform_int_distribution<int>(1000, 2000)(rng);
        std::lock_guard<std::mutex> g_taking(mtx);
        {
            taking_forks(taking_time, id_phil);
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(taking_time));

        eating_time = std::uniform_int_distribution<int>(1000, 2000)(rng);
        std::lock_guard<std::mutex> g_eating(mtx);
        {
            eating(eating_time, id_phil);
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(eating_time));

        returning_time = std::uniform_int_distribution<int>(1000, 2000)(rng);
        std::lock_guard<std::mutex> g_returning(mtx);
        {
            returning_forks(returning_time, id_phil);
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(returning_time));


    }


}

int main() {
    int table_state[num_phil];

    int thinking_time;  // time_id = 0
    int taking_time;    // time_id = 0
    int returning_time; // time_id = 0
    int eating_time;    // time_id = 0
    int waiting_time;   // time_id = 0

    int times_array[num_phil][5];
    // every philosopher [num_phil] has a list of times it takes to makes an action
    // on this basis (e.g. which philosopher is waiting the longest to eat) priority queue will be created
    //check_directions();
    ;
    mutex mut1, mut2, mut3, mut4, mut5;
    // c++ threads require user to add parameters after passing pointer to desired function
    //    thread t1(philosopher,&times_array[0][5], 0, mut1, mut2);
    //    thread t2(philosopher,&times_array[1][5], 1);
    //    thread t3(philosopher,&times_array[2][5], 2);
    //    thread t4(philosopher,&times_array[3][5], 3);
    //    thread t5(philosopher,&times_array[4][5], 4);

    thread t1([&] {philosopher(&times_array[0][5], 0, mut1, mut2);});
    thread t2([&] {philosopher(&times_array[1][5], 1, mut2, mut3);});
    thread t3([&] {philosopher(&times_array[2][5], 2, mut3, mut4);});
    thread t4([&] {philosopher(&times_array[3][5], 3, mut4, mut5);});
    thread t5([&] {philosopher(&times_array[4][5], 4, mut5, mut1);});

    t1.join();
    t2.join();
    t3.join();
    t4.join();
    t5.join();

    return 0;
}

/* converting number into time
int value = 1000;
auto time = std::chrono::milliseconds(value);
cout << "   " <<time.count();

 * */


