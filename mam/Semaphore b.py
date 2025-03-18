import threading
import time

# Initialize Semaphore with buffer capacity
Semaphore = threading.Semaphore(5)
Limit = 5

# Shared buffer to simulate production/consumption
buffer = 0

def wait():
    """Producer waits for an available slot to produce."""
    global buffer
    while buffer >= Limit:
        print("\nBuffer Full, Producer is waiting...")
        time.sleep(0.1)  # Simulate the waiting time

    buffer += 1  # Produce an item

def signal():
    """Consumer consumes an item if available."""
    global buffer
    while buffer <= 0:
        print("\nBuffer Empty, Consumer is waiting...")
        time.sleep(0.1)  # Simulate the waiting time

    buffer -= 1  # Consume an item

def producer():
    """Producer function."""
    for i in range(10):
        wait()  # Wait for available buffer space
        print(f"Produced item {i+1}")

def consumer():
    """Consumer function."""
    for i in range(10):
        signal()  # Wait for an item to consume
        print(f"Consumed item {i+1}")

# Create producer and consumer threads
t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)

# Start the threads
t1.start()
t2.start()

# Wait for threads to complete
t1.join()
t2.join()
