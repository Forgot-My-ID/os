import random
import time
import threading
import logging
import queue
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

# Peterson's Solution variables
flag = [False, False]  # flag[0] for producer, flag[1] for consumer
turn = 0  # Shared turn variable

BSIZE = 8  # Buffer size
PWT = 4  # Producer wait time limit
CWT = 10  # Consumer wait time limit
RT = 15  # Program run-time in seconds

# Initialize producer and consumer counters
produce_count = 0
consume_count = 0

def myrand(n):
    return random.randint(3, n)

def peterson_lock(id):
    global turn, flag
    other = 1 - id
    flag[id] = True
    turn = other
    while flag[other] and turn == other:
        time.sleep(0.001)  # Busy wait

def peterson_unlock(id):
    global flag
    flag[id] = False

def producer(shared_queue, stop_event, data):
    global produce_count
    while not stop_event.is_set():
        peterson_lock(0)  # Locking for producer (id = 0)
        if not shared_queue.full():  # Only produce if the queue is not full
            tempo = myrand(BSIZE * 3)
            shared_queue.put(tempo)
            produce_count += 1  # Increment the producer count
            data.append(("Producer", list(shared_queue.queue)))  # Update data for plotting
        peterson_unlock(0)  # Unlocking for producer
        time.sleep(myrand(PWT))

def consumer(shared_queue, stop_event, data):
    global consume_count
    while not stop_event.is_set():
        peterson_lock(1)  # Locking for consumer (id = 1)
        if not shared_queue.empty():  # Only consume if the queue is not empty
            shared_queue.get()
            consume_count += 1  # Increment the consumer count only if something is consumed
            data.append(("Consumer", list(shared_queue.queue)))  # Update data for plotting
        peterson_unlock(1)  # Unlocking for consumer
        time.sleep(myrand(CWT))

def update_plot(i, data, producer_circle, consumer_circle, buffer_rectangles, produce_text, consume_text):
    global produce_count, consume_count
    if data:
        action, buffer = data[-1]  # Get the latest action and buffer state

        # Reset producer and consumer indicators
        producer_circle.set_facecolor("lightgray")
        consumer_circle.set_facecolor("lightgray")

        # Fill the buffer from the bottom up
        for rect in buffer_rectangles:
            rect.set_facecolor("lightgray")  # Reset all buffer slots

        # Color the buffer based on the current state
        for i in range(len(buffer)):
            buffer_rectangles[i].set_facecolor("blue")

        # Indicate when producer produces or consumer consumes
        if action == "Producer":
            producer_circle.set_facecolor("green")
        elif action == "Consumer":
            consumer_circle.set_facecolor("green")

        # Update the text with the current produce/consume counts
        produce_text.set_text(f"Produced: {produce_count}")
        consume_text.set_text(f"Consumed: {consume_count}")

def setup_plot():
    fig, ax = plt.subplots()
    ax.set_xlim(-2, 2)  # Wider x limits to fit producer and consumer
    ax.set_ylim(0, BSIZE)
    ax.set_aspect('auto')
    ax.axis('off')

    # Create buffer as a vertical stack of rectangles
    buffer_rectangles = []
    for i in range(BSIZE):
        rect = patches.Rectangle((-0.5, i), 1, 1, edgecolor="black", facecolor="lightgray")
        ax.add_patch(rect)
        buffer_rectangles.append(rect)

    # Producer circle on the left
    producer_circle = patches.Circle((-1.5, BSIZE/2), 0.5, edgecolor="black", facecolor="lightgray")
    ax.add_patch(producer_circle)
    ax.text(-1.5, BSIZE/2, "Producer", ha="center", va="center", fontsize=12, fontweight="bold", color="black")

    # Consumer circle on the right
    consumer_circle = patches.Circle((1.5, BSIZE/2), 0.5, edgecolor="black", facecolor="lightgray")
    ax.add_patch(consumer_circle)
    ax.text(1.5, BSIZE/2, "Consumer", ha="center", va="center", fontsize=12, fontweight="bold", color="black")

    # Text to display the produce and consume counts
    produce_text = ax.text(-1.5, -1, f"Produced: {produce_count}", ha="center", fontsize=12, fontweight="bold", color="green")
    consume_text = ax.text(1.5, -1, f"Consumed: {consume_count}", ha="center", fontsize=12, fontweight="bold", color="blue")

    return fig, ax, producer_circle, consumer_circle, buffer_rectangles, produce_text, consume_text

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s', force=True)  # Immediate logging output

    shared_queue = queue.Queue(BSIZE)
    buffer_data = []  # For tracking buffer state
    stop_event = threading.Event()

    # Producer (id = 0) and Consumer (id = 1)
    producer_thread = threading.Thread(target=producer, args=(shared_queue, stop_event, buffer_data))
    consumer_thread = threading.Thread(target=consumer, args=(shared_queue, stop_event, buffer_data))

    # Start the producer and consumer threads
    producer_thread.start()
    consumer_thread.start()

    # Set up the plot
    fig, ax, producer_circle, consumer_circle, buffer_rectangles, produce_text, consume_text = setup_plot()

    # Animation function with explicit frame count
    ani = animation.FuncAnimation(fig, update_plot, frames=100, fargs=(buffer_data, producer_circle, consumer_circle, buffer_rectangles, produce_text, consume_text), interval=500)

    # Display the plot
    plt.show()

    # Let the program run for RT seconds
    time.sleep(RT)

    # Signal the threads to stop
    stop_event.set()

    # Wait for threads to finish
    producer_thread.join()
    consumer_thread.join()

    logging.info("\nThe clock ran out.")
