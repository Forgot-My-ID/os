import random
import time
import threading
import tkinter as tk
from queue import Queue

# Global parameters
PRODUCE_TIME = 2  # Time taken by the producer to produce a product (in seconds)
CONSUME_TIME = 3  # Time taken by the consumer to package a product (in seconds)

# Shared variables
buffer = None  # Buffer will be initialized dynamically
stop_event = threading.Event()


# Producer function
def producer(producer_label, buffer_listbox):
    while not stop_event.is_set():
        if not buffer.full():
            product = f"Product-{random.randint(1, 100)}"
            buffer.put(product)
            producer_label.config(text=f"Produced: {product}")
            update_buffer_display(buffer_listbox)
        else:
            producer_label.config(text="Buffer is full, waiting...")
        time.sleep(PRODUCE_TIME)


# Consumer function
def consumer(consumer_label, buffer_listbox, consumer_listbox):
    while not stop_event.is_set():
        if not buffer.empty():
            product = buffer.get()
            consumer_listbox.insert(tk.END, product)  # Add the consumed product to the consumer listbox
            consumer_label.config(text=f"Consumed: {product}")
            update_buffer_display(buffer_listbox)
        else:
            consumer_label.config(text="Buffer is empty, waiting...")
        time.sleep(CONSUME_TIME)


# Update the buffer display
def update_buffer_display(buffer_listbox):
    buffer_listbox.delete(0, tk.END)  # Clear the buffer listbox
    for item in list(buffer.queue):
        buffer_listbox.insert(tk.END, item)  # Add each product to the buffer listbox


# Start the production line
def start_production(producer_label, consumer_label, buffer_listbox, consumer_listbox, start_button):
    start_button.config(state=tk.DISABLED)  # Disable the start button
    stop_event.clear()

    # Start producer and consumer threads
    producer_thread = threading.Thread(target=producer, args=(producer_label, buffer_listbox))
    consumer_thread = threading.Thread(target=consumer, args=(consumer_label, buffer_listbox, consumer_listbox))

    producer_thread.start()
    consumer_thread.start()


# Stop the production line
def stop_production(start_button):
    stop_event.set()
    start_button.config(state=tk.NORMAL)  # Re-enable the start button


# Initialize the buffer dynamically
def initialize_buffer(root, buffer_size_entry):
    global buffer
    try:
        buffer_size = int(buffer_size_entry.get())
        if buffer_size <= 0:
            raise ValueError("Buffer size must be a positive integer.")
        buffer = Queue(buffer_size)
        buffer_size_entry.config(state=tk.DISABLED)  # Disable entry after initialization
        root.destroy()  # Close the initialization window
        create_gui()  # Start the main GUI
    except ValueError as e:
        buffer_size_entry.delete(0, tk.END)
        buffer_size_entry.insert(0, "Enter a valid positive number")


# GUI setup for buffer initialization
def buffer_size_gui():
    root = tk.Tk()
    root.title("Initialize Buffer Size")

    tk.Label(root, text="Enter Buffer Size:", font=("Arial", 14)).pack(pady=10)
    buffer_size_entry = tk.Entry(root, font=("Arial", 12), width=15)
    buffer_size_entry.pack(pady=10)

    submit_button = tk.Button(root, text="Submit", font=("Arial", 12, "bold"),
                              command=lambda: initialize_buffer(root, buffer_size_entry))
    submit_button.pack(pady=20)

    root.mainloop()


# Main GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Factory Production Line")

    # Producer section
    producer_frame = tk.Frame(root, pady=10, padx=10)
    producer_frame.grid(row=0, column=0, sticky="nsew")
    tk.Label(producer_frame, text="Producer", font=("Arial", 14, "bold")).pack()
    producer_label = tk.Label(producer_frame, text="Produced: None", font=("Arial", 12), bg="lightblue", width=30)
    producer_label.pack()

    # Buffer section
    buffer_frame = tk.Frame(root, pady=10, padx=10)
    buffer_frame.grid(row=0, column=1, sticky="nsew")
    tk.Label(buffer_frame, text="Production Line (Buffer)", font=("Arial", 14, "bold")).pack()
    buffer_listbox = tk.Listbox(buffer_frame, font=("Arial", 12), bg="lightyellow", width=30, height=10)
    buffer_listbox.pack()

    # Consumer section
    consumer_frame = tk.Frame(root, pady=10, padx=10)
    consumer_frame.grid(row=0, column=2, sticky="nsew")
    tk.Label(consumer_frame, text="Consumer", font=("Arial", 14, "bold")).pack()
    consumer_label = tk.Label(consumer_frame, text="Consumed: None", font=("Arial", 12), bg="lightgreen", width=30)
    consumer_label.pack()
    consumer_listbox = tk.Listbox(consumer_frame, font=("Arial", 12), bg="lightgreen", width=30, height=10)
    consumer_listbox.pack()

    # Control buttons
    control_frame = tk.Frame(root, pady=20)
    control_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")
    start_button = tk.Button(control_frame, text="Start", font=("Arial", 12, "bold"),
                              command=lambda: start_production(producer_label, consumer_label, buffer_listbox, consumer_listbox, start_button))
    start_button.pack(side=tk.LEFT, padx=10)
    stop_button = tk.Button(control_frame, text="Stop", font=("Arial", 12, "bold"),
                             command=lambda: stop_production(start_button))
    stop_button.pack(side=tk.RIGHT, padx=10)

    root.mainloop()


if __name__ == "__main__":
    buffer_size_gui()
