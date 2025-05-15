import tkinter as tk
import threading
import time
import random

# Buffer settings
BUFFER_SIZE = 5
buffer = []

# Semaphores for synchronization
empty_slots = threading.Semaphore(BUFFER_SIZE)  # Initially, all slots are empty
full_slots = threading.Semaphore(0)  # Initially, no slots are full
buffer_lock = threading.Lock()

# GUI setup
class ProducerConsumerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Semaphore Producer-Consumer Problem")
        self.master.geometry("500x400")
        self.master.configure(bg="#f0f4f8")

        # Buffer Display
        self.buffer_frame = tk.Frame(master, bg="#f0f4f8")
        self.buffer_frame.pack(pady=20)

        self.buffer_labels = []
        for i in range(BUFFER_SIZE):
            label = tk.Label(self.buffer_frame, text="Empty", width=10, height=2,
                             font=("Helvetica", 12), borderwidth=2, relief="solid",
                             bg="#ddd", fg="#333")
            label.grid(row=0, column=i, padx=5, pady=5)
            self.buffer_labels.append(label)

        # Control Buttons
        self.control_frame = tk.Frame(master, bg="#f0f4f8")
        self.control_frame.pack(pady=10)

        self.start_producer_button = tk.Button(self.control_frame, text="Start Producer", command=self.start_producer,
                                               font=("Helvetica", 10), bg="#4CAF50", fg="white", width=15)
        self.start_producer_button.grid(row=0, column=0, padx=5, pady=5)

        self.start_consumer_button = tk.Button(self.control_frame, text="Start Consumer", command=self.start_consumer,
                                               font=("Helvetica", 10), bg="#2196F3", fg="white", width=15)
        self.start_consumer_button.grid(row=0, column=1, padx=5, pady=5)

        # Status Labels
        self.status_frame = tk.Frame(master, bg="#f0f4f8")
        self.status_frame.pack(pady=10)

        self.producer_status = tk.Label(self.status_frame, text="Producer Status: Waiting",
                                        font=("Helvetica", 12), fg="#4CAF50", bg="#f0f4f8")
        self.producer_status.grid(row=0, column=0, padx=10, pady=5)

        self.consumer_status = tk.Label(self.status_frame, text="Consumer Status: Waiting",
                                        font=("Helvetica", 12), fg="#2196F3", bg="#f0f4f8")
        self.consumer_status.grid(row=1, column=0, padx=10, pady=5)

        # Control Variables
        self.producer_active = False
        self.consumer_active = False

    def start_producer(self):
        if not self.producer_active:
            self.producer_active = True
            threading.Thread(target=self.producer).start()

    def start_consumer(self):
        if not self.consumer_active:
            self.consumer_active = True
            threading.Thread(target=self.consumer).start()

    def producer(self):
        while self.producer_active:
            time.sleep(random.uniform(0.5, 1.5))  # Simulate production time
            item = random.randint(1, 100)  # Produce a random item

            # Wait for an empty slot
            empty_slots.acquire()
            with buffer_lock:
                buffer.append(item)
                self.update_buffer()  # Schedule GUI buffer display update

            full_slots.release()  # Signal that there is a full slot
            self.update_status("producer", f"Produced: {item}")
            time.sleep(1)  # To show production status clearly

    def consumer(self):
        while self.consumer_active:
            time.sleep(random.uniform(0.5, 1.5))  # Simulate consumption time

            # Wait for a full slot
            full_slots.acquire()
            with buffer_lock:
                item = buffer.pop(0)
                self.update_buffer()  # Schedule GUI buffer display update

            empty_slots.release()  # Signal that there is an empty slot
            self.update_status("consumer", f"Consumed: {item}")
            time.sleep(1)  # To show consumption status clearly

    def update_buffer(self):
        # Schedule buffer update on main thread using after()
        self.master.after(0, self._update_buffer_labels)

    def _update_buffer_labels(self):
        for i in range(BUFFER_SIZE):
            if i < len(buffer):
                self.buffer_labels[i].config(text=str(buffer[i]), bg="#b3e5fc", fg="#333")
            else:
                self.buffer_labels[i].config(text="Empty", bg="#ddd", fg="#333")

    def update_status(self, role, message):
        # Schedule status update on main thread using after()
        if role == "producer":
            self.master.after(0, lambda: self.producer_status.config(text=message))
        elif role == "consumer":
            self.master.after(0, lambda: self.consumer_status.config(text=message))


# Create the main window
root = tk.Tk()
app = ProducerConsumerGUI(root)
root.mainloop()
