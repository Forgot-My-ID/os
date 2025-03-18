import threading
import random
import time

philosopher = 5
Chopstick = [False, False, False, False, False]  # Initially, no chopsticks are taken


def wait(n):  # A philosopher tries to pick up chopstick n
    global Chopstick
    while Chopstick[n] == True:  # If the chopstick is already taken, the philosopher waits
        print(f"Philosopher {n} is waiting for chopstick {n}...")
        # time.sleep(0.1)  # Small delay to prevent busy-waiting
    Chopstick[n] = True  # The philosopher picks up the chopstick
    print(f"Philosopher {n} picked up chopstick {n}.")


def signal(n):  # Philosopher puts down chopstick n
    global Chopstick
    Chopstick[n] = False  # Release the chopstick
    print(f"Philosopher {n} put down chopstick {n}.")


def eating(n):  # Philosopher tries to eat
    print(f"Philosopher {n} is thinking...")

    # Philosopher picks up the left and right chopsticks
    wait(n)  # Wait for the left chopstick
    wait((n + 1) % 5)  # Wait for the right chopstick

    print(f"\nPhilosopher {n} is eating...\n")
    time.sleep(1) 

    # Philosopher is done eating and puts down both chopsticks
    signal(n)
    signal((n + 1) % 5)

    print(f"Philosopher {n} is done eating and thinking again...\n")


# Create and start threads for each philosopher
t1 = threading.Thread(target=eating, args=(0,))
t2 = threading.Thread(target=eating, args=(1,))
t3 = threading.Thread(target=eating, args=(2,))
t4 = threading.Thread(target=eating, args=(3,))
t5 = threading.Thread(target=eating, args=(4,))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

# Join all threads
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()

print("\nAll philosophers have finished their meal and thinking.")
