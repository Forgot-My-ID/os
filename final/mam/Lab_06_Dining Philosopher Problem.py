import threading
import time
import random
import tkinter as tk
import math

class Philosopher(threading.Thread):
    def __init__(self, philosopher_id, left_fork, right_fork, shared_state, global_lock):
        threading.Thread.__init__(self)
        self.philosopher_id = philosopher_id
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.shared_state = shared_state
        self.global_lock = global_lock
        self.state = "Thinking"

    def run(self):
        while True:
            self.state = "Thinking"
            self.shared_state[self.philosopher_id]['state'] = self.state
            time.sleep(random.uniform(2, 4))

            self.state = "Hungry"
            self.shared_state[self.philosopher_id]['state'] = self.state

            with self.global_lock:
                with self.left_fork:
                    self.shared_state[self.philosopher_id]['left_fork'] = True
                    with self.right_fork:
                        self.shared_state[self.philosopher_id]['right_fork'] = True
                        self.state = "Eating"
                        self.shared_state[self.philosopher_id]['state'] = self.state
                        time.sleep(1.5)

                self.shared_state[self.philosopher_id]['left_fork'] = False
                self.shared_state[self.philosopher_id]['right_fork'] = False
                self.state = "Thinking"
                self.shared_state[self.philosopher_id]['state'] = self.state

class PhilosopherUI:
    def __init__(self, root, philosopher_count):
        self.root = root
        self.philosopher_count = philosopher_count
        self.canvas_size = 600
        self.radius = 200
        self.philosopher_labels = []
        self.fork_labels = []
        self.chair_labels = []
        self.philosopher_texts = []
        self.eating_label = None
        self.waiting_label = None
        self.create_widgets()
        self.shared_state = [{'state': 'Thinking', 'left_fork': False, 'right_fork': False} for _ in range(self.philosopher_count)]

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        self.canvas.create_oval(150, 150, 450, 450, fill='sienna', outline='black')

        angle = 360 / self.philosopher_count
        for i in range(self.philosopher_count):
            chair_x = 300 + (self.radius + 60) * math.cos(math.radians(i * angle))
            chair_y = 300 + (self.radius + 60) * math.sin(math.radians(i * angle))
            chair_label = self.canvas.create_rectangle(chair_x-20, chair_y-40, chair_x+20, chair_y+40, fill='brown')
            self.chair_labels.append(chair_label)

            body_x = 300 + self.radius * math.cos(math.radians(i * angle))
            body_y = 300 + self.radius * math.sin(math.radians(i * angle))
            philosopher_body = self.canvas.create_rectangle(body_x-15, body_y-40, body_x+15, body_y+20, fill='blue')
            philosopher_head = self.canvas.create_oval(body_x-15, body_y-60, body_x+15, body_y-40, fill='lightpink')
            self.philosopher_labels.append((philosopher_body, philosopher_head))

            fork_x = 300 + (self.radius - 40) * math.cos(math.radians(i * angle + angle / 2))
            fork_y = 300 + (self.radius - 40) * math.sin(math.radians(i * angle + angle / 2))
            fork_label = self.canvas.create_line(300, 300, fork_x, fork_y, fill='black', width=4)
            self.fork_labels.append(fork_label)

            # Add philosopher label (e.g., P1, P2) near the philosopher's head
            text_x = body_x
            text_y = body_y - 70
            philosopher_text = self.canvas.create_text(text_x, text_y, text=f"P{i+1}", font=("Arial", 14, "bold"), fill="black")
            self.philosopher_texts.append(philosopher_text)

        self.eating_label = tk.Label(self.root, text="", font=('Arial', 16), fg="green")
        self.eating_label.pack(pady=10)

        self.waiting_label = tk.Label(self.root, text="", font=('Arial', 16), fg="red")
        self.waiting_label.pack(pady=10)

    def update_status(self):
        eating_philosophers = []
        waiting_philosophers = []

        for i, state in enumerate(self.shared_state):
            body_color = 'blue'
            if state['state'] == "Hungry":
                body_color = 'red'
                waiting_philosophers.append(f"P{i+1}")
            elif state['state'] == "Eating":
                body_color = 'green'
                eating_philosophers.append(f"P{i+1}")

            philosopher_body, _ = self.philosopher_labels[i]
            self.canvas.itemconfig(philosopher_body, fill=body_color)

            left_fork_color = 'black'
            right_fork_color = 'black'

            if state['left_fork']:
                left_fork_color = 'green'
            if state['right_fork']:
                right_fork_color = 'green'

            self.canvas.itemconfig(self.fork_labels[i], fill=left_fork_color)
            self.canvas.itemconfig(self.fork_labels[(i + 1) % self.philosopher_count], fill=right_fork_color)

        # Update eating label in green
        if eating_philosophers:
            self.eating_label.config(text=f"Philosopher(s) eating: {', '.join(eating_philosophers)}", fg="green")
        else:
            self.eating_label.config(text="No philosopher is eating.", fg="red")

        # Update waiting label in red
        if waiting_philosophers:
            self.waiting_label.config(text=f"Philosopher(s) waiting: {', '.join(waiting_philosophers)}", fg="red")
        else:
            self.waiting_label.config(text="")

        self.root.after(300, self.update_status)

def start_simulation():
    K = 5
    root = tk.Tk()
    root.title("Dining Philosophers Simulation")

    ui = PhilosopherUI(root, K)
    forks = [threading.Lock() for _ in range(K)]
    global_lock = threading.Lock()

    philosophers = [Philosopher(i, forks[i], forks[(i + 1) % K], ui.shared_state, global_lock) for i in range(K)]

    for philosopher in philosophers:
        philosopher.start()

    ui.update_status()
    root.mainloop()

start_simulation()
