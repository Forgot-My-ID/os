import threading
import time
import tkinter as tk
from tkinter import ttk

# Peterson's Solution variables
flag = [False, False]
turn = 0

# Shared resources
buffer = []
buffer_size = 8
producer_speed = 2
consumer_speed = 3
running = False

# Producer and consumer counters
produce_count = 0
consume_count = 0

def update_visuals():
    global produce_count, consume_count
    for i in range(buffer_size):
        if i < len(buffer):
            buffer_labels[i].config(bg="blue")
        else:
            buffer_labels[i].config(bg="gray")
    producer_circle.config(bg="green" if flag[0] else "lightgray")
    consumer_circle.config(bg="green" if flag[1] else "lightgray")
    produce_label.config(text=f"Total Produced Pitha: {produce_count}")
    consume_label.config(text=f"Total Consumed Pitha: {consume_count}")
    update_calculation()

def update_calculation():
    remaining_units = produce_count - consume_count
    try:
        unit_price = float(unit_price_entry.get())
    except ValueError:
        unit_price = 0
    total_revenue = remaining_units * unit_price
    remaining_units_label.config(text=f"Remaining Units: {remaining_units}")
    total_revenue_label.config(text=f"Total Revenue: {remaining_units} × {unit_price} = {total_revenue} TK")

def peterson_lock(id):
    global turn, flag
    other = 1 - id
    flag[id] = True
    turn = other
    while flag[other] and turn == other:
        time.sleep(0.001)

def peterson_unlock(id):
    global flag
    flag[id] = False

def producer():
    global buffer, produce_count, running
    while running:
        time.sleep(producer_speed)
        peterson_lock(0)
        if len(buffer) < buffer_size:
            flag[0] = True
            buffer.append(1)
            produce_count += 1
            update_visuals()
            flag[0] = False
        peterson_unlock(0)

def consumer():
    global buffer, consume_count, running
    while running:
        time.sleep(consumer_speed)
        peterson_lock(1)
        if len(buffer) > 0:
            flag[1] = True
            buffer.pop(0)
            consume_count += 1
            update_visuals()
            flag[1] = False
        peterson_unlock(1)

def start_simulation():
    global running
    running = True
    threading.Thread(target=producer, daemon=True).start()
    threading.Thread(target=consumer, daemon=True).start()

def stop_simulation():
    global running
    running = False

def reset_simulation():
    global buffer, produce_count, consume_count
    stop_simulation()
    buffer = []
    produce_count = 0
    consume_count = 0
    update_visuals()

def update_values():
    global producer_speed, consumer_speed, buffer_size, buffer_labels
    try:
        new_producer_speed = float(producer_speed_entry.get())
        new_consumer_speed = float(consumer_speed_entry.get())
        new_buffer_size = int(buffer_size_entry.get())
        global producer_speed, consumer_speed
        producer_speed = new_producer_speed
        consumer_speed = new_consumer_speed
        if new_buffer_size != buffer_size:
            buffer_size = new_buffer_size
            reset_buffer_visuals()
        reset_simulation()
    except ValueError:
        print("Invalid input!")

def reset_buffer_visuals():
    global buffer_labels
    for widget in buffer_frame.winfo_children():
        widget.destroy()
    buffer_labels = [tk.Label(buffer_frame, text="", bg="gray", width=5, height=2, relief="ridge") for _ in range(buffer_size)]
    for lbl in buffer_labels:
        lbl.pack(side=tk.LEFT, padx=2, pady=2)

root = tk.Tk()
root.title("Pitha Shop")
root.state('zoomed')  # Maximize the window

title_label = tk.Label(root, text="𓆩⫷  Pitha Shop ⫸𓆪", font=("Helvetica", 30, "bold"), fg="purple")
title_label.pack(pady=20)

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

producer_circle = tk.Label(main_frame, text="Producer", bg="lightgray", width=15, height=8, font=("Arial", 12))
producer_circle.grid(row=0, column=0, padx=20)

consumer_circle = tk.Label(main_frame, text="Consumer", bg="lightgray", width=15, height=8, font=("Arial", 12))
consumer_circle.grid(row=0, column=2, padx=20)

buffer_frame = tk.Frame(main_frame)
buffer_frame.grid(row=0, column=1, padx=10)
buffer_labels = [tk.Label(buffer_frame, text="", bg="gray", width=6, height=2, relief="ridge") for _ in range(buffer_size)]
for lbl in buffer_labels:
    lbl.pack(side=tk.LEFT, padx=5)

control_frame = tk.Frame(root)
control_frame.pack(pady=10)

tk.Label(control_frame, text="Pitha Producer Speed (s):").grid(row=0, column=0, padx=5)
producer_speed_entry = tk.Entry(control_frame, width=10)
producer_speed_entry.insert(0, str(producer_speed))
producer_speed_entry.grid(row=0, column=1, padx=5)

tk.Label(control_frame, text="Pitha Consumer Speed (s):").grid(row=1, column=0, padx=5)
consumer_speed_entry = tk.Entry(control_frame, width=10)
consumer_speed_entry.insert(0, str(consumer_speed))
consumer_speed_entry.grid(row=1, column=1, padx=5)

tk.Label(control_frame, text="Pitha Storage:").grid(row=2, column=0, padx=5)
buffer_size_entry = tk.Entry(control_frame, width=10)
buffer_size_entry.insert(0, str(buffer_size))
buffer_size_entry.grid(row=2, column=1, padx=5)

apply_button = ttk.Button(control_frame, text="Apply", command=update_values)
apply_button.grid(row=3, column=0, columnspan=2, pady=5)

buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=20)

start_button = ttk.Button(buttons_frame, text="Start", command=start_simulation)
start_button.grid(row=0, column=0, padx=10)

stop_button = ttk.Button(buttons_frame, text="Stop", command=stop_simulation)
stop_button.grid(row=0, column=1, padx=10)

reset_button = ttk.Button(buttons_frame, text="Reset", command=reset_simulation)
reset_button.grid(row=0, column=2, padx=10)

calculation_frame = tk.Frame(root)
calculation_frame.pack(pady=20)

tk.Label(calculation_frame, text="Unit Price:").grid(row=0, column=0, padx=5)
unit_price_entry = tk.Entry(calculation_frame, width=10)
unit_price_entry.insert(0, "0")
unit_price_entry.grid(row=0, column=1, padx=5)

remaining_units_label = tk.Label(calculation_frame, text="Remaining Units: 0", font=("Arial", 14))
remaining_units_label.grid(row=1, column=0, columnspan=2, pady=5)

total_revenue_label = tk.Label(calculation_frame, text="Total Revenue: 0 × 0 = 0 TK", font=("Arial", 14))
total_revenue_label.grid(row=2, column=0, columnspan=2, pady=5)

status_frame = tk.Frame(root)
status_frame.pack(pady=10)

produce_label = tk.Label(status_frame, text=f"Total Produced Pitha: {produce_count}", fg="green", font=("Arial", 14))
produce_label.grid(row=0, column=0, padx=20)

consume_label = tk.Label(status_frame, text=f"Total Consumed Pitha: {consume_count}", fg="blue", font=("Arial", 14))
consume_label.grid(row=0, column=1, padx=20)

root.mainloop()
