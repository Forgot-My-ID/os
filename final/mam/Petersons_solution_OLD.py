import tkinter as tk
from tkinter import ttk
import threading
import time

# Shared variables for Peterson's Algorithm
flag = [False, False]
turn = 0

# Initialize the main tkinter window
root = tk.Tk()
root.title("Peterson Algorithm Simulation")
root.geometry("500x400")
root.configure(bg="#f0f0f5")

# Define styles for a premium look
style = ttk.Style()
style.configure("TFrame", background="#f0f0f5")
style.configure("TLabel", background="#f0f0f5", font=("Arial", 12))
style.configure("Status.TLabel", font=("Arial", 10, "italic"))
style.configure("ProcessLabel.TLabel", font=("Arial", 14, "bold"), foreground="black")
style.configure("StartButton.TButton", font=("Arial", 12), foreground="#4b0082", background="#a0a0e0")

# GUI Elements for Process 0
frame_0 = ttk.Frame(root, style="TFrame")
frame_0.pack(padx=20, pady=(20, 10))
process_label_0 = ttk.Label(frame_0, text="Process 0", style="ProcessLabel.TLabel", width=20, anchor="center")
process_label_0.grid(row=0, column=0, pady=5)
status_label_0 = ttk.Label(frame_0, text="Non-Critical Section", style="Status.TLabel", foreground="black")
status_label_0.grid(row=1, column=0, pady=5)

# GUI Elements for Process 1
frame_1 = ttk.Frame(root, style="TFrame")
frame_1.pack(padx=20, pady=10)
process_label_1 = ttk.Label(frame_1, text="Process 1", style="ProcessLabel.TLabel", width=20, anchor="center")
process_label_1.grid(row=0, column=0, pady=5)
status_label_1 = ttk.Label(frame_1, text="Non-Critical Section", style="Status.TLabel", foreground="black")
status_label_1.grid(row=1, column=0, pady=5)

# Function to update UI states for Process 0
def update_process_0(status, color):
    status_label_0.config(text=status, foreground=color)
    process_label_0.config(background=color)

# Function to update UI states for Process 1
def update_process_1(status, color):
    status_label_1.config(text=status, foreground=color)
    process_label_1.config(background=color)

# Function for Process 0 with after() to handle GUI updates
def peterson_algorithm_0():
    global flag, turn

    def enter_critical_section():
        print("Process 0: In Critical Section")
        update_process_0("In Critical Section", "#32CD32")
        root.after(2000, exit_critical_section)  # Stay in critical section for 2 seconds

    def exit_critical_section():
        print("Process 0: Exiting")
        update_process_0("Exiting...", "#BA55D3")
        root.after(1000, reset_to_non_critical_section)  # Exiting section for 1 second

    def reset_to_non_critical_section():
        flag[0] = False
        print("Process 0: Non-Critical Section")
        update_process_0("Non-Critical Section", "black")

    # Start the entering phase
    print("Process 0: Entering")
    update_process_0("Entering...", "#87CEEB")
    flag[0] = True
    turn = 1

    # Check if Process 1 is in critical section
    def wait_loop():
        if flag[1] and turn == 1:
            print("Process 0: Waiting")
            update_process_0("Waiting...", "#FFA07A")
            root.after(500, wait_loop)  # Check every 0.5 seconds
        else:
            enter_critical_section()

    wait_loop()

# Function for Process 1 with after() to handle GUI updates
def peterson_algorithm_1():
    global flag, turn

    def enter_critical_section():
        print("Process 1: In Critical Section")
        update_process_1("In Critical Section", "#32CD32")
        root.after(2000, exit_critical_section)  # Stay in critical section for 2 seconds

    def exit_critical_section():
        print("Process 1: Exiting")
        update_process_1("Exiting...", "#BA55D3")
        root.after(1000, reset_to_non_critical_section)  # Exiting section for 1 second

    def reset_to_non_critical_section():
        flag[1] = False
        print("Process 1: Non-Critical Section")
        update_process_1("Non-Critical Section", "black")

    # Start the entering phase
    print("Process 1: Entering")
    update_process_1("Entering...", "#87CEEB")
    flag[1] = True
    turn = 0

    # Check if Process 0 is in critical section
    def wait_loop():
        if flag[0] and turn == 0:
            print("Process 1: Waiting")
            update_process_1("Waiting...", "#FFA07A")
            root.after(500, wait_loop)  # Check every 0.5 seconds
        else:
            enter_critical_section()

    wait_loop()

# Function to run both processes in parallel threads
def run_simulation():
    # Reset display for each run
    update_process_0("Non-Critical Section", "black")
    update_process_1("Non-Critical Section", "black")

    # Start both processes in parallel threads
    threading.Thread(target=peterson_algorithm_0).start()
    threading.Thread(target=peterson_algorithm_1).start()

# Start button to initiate the simulation
start_button = ttk.Button(root, text="Start Simulation", style="StartButton.TButton", command=run_simulation)
start_button.pack(pady=20)

# Run the GUI main loop
root.mainloop()
