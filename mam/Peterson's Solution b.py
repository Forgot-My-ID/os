import threading
import time

Critical_item = 0  # Shared critical data
Producer_wish = False
Consumer_wish = False
turn = -1  # -1 means no turn, 0 means Producer's turn, 1 means Consumer's turn

def producer_want_to_produce():
    global Critical_item, Producer_wish, Consumer_wish, turn, produced_count
    Producer_wish = True
    turn = 1  # Producer gives preference to the consumer

    # Busy-waiting loop, ensuring mutual exclusion
    while Consumer_wish and turn == 1:
        print('Producer is waiting, Consumer is in Critical section')
        time.sleep(0.1)  # Simulating a small delay to prevent tight busy-waiting

    # Critical section for Producer
    Critical_item += 1

    for _ in range(100):
        print("Producer in critical section.")
    
    Producer_wish = False
    print('Producer has finished using the critical section')

def consumer_want_to_consume():
    global Critical_item, Producer_wish, Consumer_wish, turn, consumed_count
    Consumer_wish = True
    turn = 0  # Consumer gives preference to the producer

    # Busy-waiting loop, ensuring mutual exclusion
    while Producer_wish and turn == 0:
        print('Consumer is waiting, Producer is in Critical section')
        time.sleep(0.1)  # Simulating a small delay to prevent tight busy-waiting

    # Critical section for Consumer
    Critical_item -= 1
    
    for _ in range(100):
        print("Consumer in critical section.")
    
    Consumer_wish = False
    print('Consumer has finished using the critical section')

# Create threads for producer and consumer
producer = threading.Thread(target=producer_want_to_produce)
consumer = threading.Thread(target=consumer_want_to_consume)

# Start the threads
producer.start()
consumer.start()

# Wait for threads to finish
producer.join()
consumer.join()