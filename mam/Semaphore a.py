import threading

Semaphore = 5
Limit = 5

def wait():  # Buffer er vitor produce korte thake
    global Semaphore, Limit
    while Semaphore <= 0:
        print("\n Buffer Full \n")
    Semaphore -= 1

def signal():  # Buffer theke consume korte thake
    global Semaphore, Limit
    while Semaphore >= Limit:
        print("\n Buffer Empty \n")
    Semaphore += 1


def producer():
    for i in range(10):
        wait()
        print(f"Produced {i}")


def consumer():
    for i in range(10):
        signal()
        print(f"Consumed {i}")

t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)

t1.start()
t2.start()
