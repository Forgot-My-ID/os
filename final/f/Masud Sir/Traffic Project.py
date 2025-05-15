import threading
import time
import tkinter as tk
from tkinter import ttk
from threading import Semaphore
import random

# Semaphore and shared resources
signal_semaphore = Semaphore(1)  # Only one car can pass at a time
buffer_size = 5  # Max cars that can wait at the signal
incoming_cars = 0  # Total incoming cars
outgoing_cars = 0  # Total outgoing cars
waiting_cars = 0  # Cars waiting at the signal
car_queue = []  # Queue representing waiting cars
running = False

# UI components for animation
road_canvas = None

def update_labels():
    """Update the labels for incoming, outgoing, and waiting cars."""
    incoming_label.config(text=f"{incoming_cars}")
    outgoing_label.config(text=f"{outgoing_cars}")
    waiting_label.config(text=f"{len(car_queue)}")

def add_car_to_signal():
    """Add a car to the waiting queue."""
    global incoming_cars, waiting_cars, car_queue
    while running:
        random_delay = random.uniform(2, 3)  # Random delay between 3 and 6 seconds
        time.sleep(random_delay)
        if len(car_queue) < buffer_size:
            signal_semaphore.acquire()  # Wait for signal access
            incoming_cars += 1
            waiting_cars += 1
            # Add car to the canvas with proper spacing
            x_position = 100 + len(car_queue) * 100  # Adjust spacing for better visibility

            # Car body
            car_body = road_canvas.create_rectangle(
                x_position, adjusted_height // 2 - 30,
                x_position + 70, adjusted_height // 2 + 10,
                fill="Red", outline=""
            )
            # Wheels
            front_wheel = road_canvas.create_oval(
                x_position + 10, adjusted_height // 2 + 10,
                x_position + 30, adjusted_height // 2 + 30,
                fill="gray", outline=""
            )
            rear_wheel = road_canvas.create_oval(
                x_position + 40, adjusted_height // 2 + 10,
                x_position + 60, adjusted_height // 2 + 30,
                fill="gray", outline=""
            )

            # Grouping car parts together
            car = [car_body, front_wheel, rear_wheel]
            car_queue.append(car)
            update_labels()
            signal_semaphore.release()  # Release signal access


def remove_car_from_signal():
    """Remove a car from the waiting queue."""
    global outgoing_cars, waiting_cars, car_queue
    while running:
        time.sleep(5)  # Car exits every 5 seconds when the signal is green
        if len(car_queue) > 0:
            signal_semaphore.acquire()  # Wait for signal access
            outgoing_cars += 1
            waiting_cars -= 1
            # Animate car exiting
            car_parts = car_queue.pop(0)
            for _ in range(50):
                for part in car_parts:
                    road_canvas.move(part, 30, 0)
                time.sleep(0.1)
            for part in car_parts:
                road_canvas.delete(part)  # Remove car from canvas
            # Shift remaining cars visually
            for i, car_parts in enumerate(car_queue):
                x_position = 100 + i * 100
                road_canvas.coords(
                    car_parts[0],  # Body
                    x_position, adjusted_height // 2 - 30,
                    x_position + 70, adjusted_height // 2 + 10
                )
                road_canvas.coords(
                    car_parts[1],  # Front wheel
                    x_position + 10, adjusted_height // 2 + 10,
                    x_position + 30, adjusted_height // 2 + 30
                )
                road_canvas.coords(
                    car_parts[2],  # Rear wheel
                    x_position + 40, adjusted_height // 2 + 10,
                    x_position + 60, adjusted_height // 2 + 30
                )
            update_labels()
            signal_semaphore.release()  # Release signal access

def start_simulation():
    """Start the simulation."""
    global running
    running = True
    threading.Thread(target=add_car_to_signal, daemon=True).start()
    threading.Thread(target=remove_car_from_signal, daemon=True).start()

def stop_simulation():
    """Stop the simulation."""
    global running
    running = False

def reset_simulation():
    """Reset the simulation."""
    global incoming_cars, outgoing_cars, waiting_cars, car_queue
    stop_simulation()
    time.sleep(1)  # Allow threads to stop gracefully
    incoming_cars = 0
    outgoing_cars = 0
    waiting_cars = 0
    car_queue = []
    road_canvas.delete("all")  # Clear the canvas
    draw_road()
    update_labels()

def draw_road():
    """Draw a road with a checking station on the canvas."""
    # Add green grass
    road_canvas.create_rectangle(0, 0, adjusted_width, adjusted_height // 2 - 50, fill="#228B22", outline="")  # Light green grass
    road_canvas.create_rectangle(0, adjusted_height // 2 + 50, adjusted_width, adjusted_height, fill="#228B22", outline="")  # Light green grass

    # Add road
    road_canvas.create_rectangle(0, adjusted_height // 2 - 50, adjusted_width, adjusted_height // 2 + 50, fill="black", outline="")

    # Add yellow divider lines
    for i in range(0, adjusted_width, 80):
        road_canvas.create_rectangle(i, adjusted_height // 2 - 5, i + 40, adjusted_height // 2 + 5, fill="white", outline="")

    # Add a checking station
    road_canvas.create_rectangle(adjusted_width - 250, adjusted_height // 2 - 50, adjusted_width - 150, adjusted_height // 2 + 50, fill="lightgray", outline="black")
    road_canvas.create_text(adjusted_width - 200, adjusted_height // 2, text="Check Point", font=("Consolas", 13, "bold"), fill="black")

# Create the main Tkinter window
root = tk.Tk()
root.title("Traffic Simulation")
root.state('zoomed')  # Set the window to fullscreen

# Adjust dimensions for screen scaling
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
adjusted_width = int(screen_width * 1)  # Adjust to fit most of the screen
adjusted_height = int(screen_height * .65)

# Add a stylish title
import tkinter as tk
from tkinter import font

# Load custom font
custom_font = font.Font(family="Broadway", size=40, weight="bold")  # Replace with the installed font

# Apply custom font to title
title_label = tk.Label(
    root,
    text="Traffic Police Checking Point",
    font=custom_font,
    fg="white",
    bg="black"  # Background matching retro style
)
title_label.pack(pady=10)


# Create road canvas
road_canvas = tk.Canvas(root, width=adjusted_width, height=adjusted_height - 150, bg="white")
road_canvas.pack(fill=tk.BOTH, expand=True, pady=20)

# Draw initial road
draw_road()

# Control buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Create a custom style for the buttons
style = ttk.Style()
style.configure("Large.TButton", font=("Consolas", 16), padding=(10, 5))  # Font size and padding

# Start Button
start_button = ttk.Button(button_frame, text="Start", command=start_simulation, style="Large.TButton")
start_button.grid(row=0, column=0, padx=20, pady=10)

# Stop Button
stop_button = ttk.Button(button_frame, text="Stop", command=stop_simulation, style="Large.TButton")
stop_button.grid(row=0, column=1, padx=20, pady=10)

# Reset Button
reset_button = ttk.Button(button_frame, text="Reset", command=reset_simulation, style="Large.TButton")
reset_button.grid(row=0, column=2, padx=20, pady=10)


# Labels for car counts
status_frame = tk.Frame(root)
status_frame.pack(pady=20)

tk.Label(status_frame, text="Incoming Cars:", font=("Consolas", 18, "bold")).grid(row=0, column=0, padx=20)
incoming_label = tk.Label(status_frame, text=f"{incoming_cars}", font=("Consolas", 24, "bold"), fg="blue")
incoming_label.grid(row=1, column=0, padx=20)

tk.Label(status_frame, text="Outgoing Cars:", font=("Consolas", 18, "bold")).grid(row=0, column=1, padx=20)
outgoing_label = tk.Label(status_frame, text=f"{outgoing_cars}", font=("Consolas", 24, "bold"), fg="green")
outgoing_label.grid(row=1, column=1, padx=20)

tk.Label(status_frame, text="Waiting Cars:", font=("Consolas", 18, "bold")).grid(row=0, column=2, padx=20)
waiting_label = tk.Label(status_frame, text=f"{waiting_cars}", font=("Consolas", 24, "bold"), fg="red")
waiting_label.grid(row=1, column=2, padx=20)

# Footer Section
footer = tk.Label(root, text="Developed by: Md Mohidul Alam | © 2024", font=("Consolas", 12), fg="black")
footer.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
