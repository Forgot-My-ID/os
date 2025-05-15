import threading
import time
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random


class Locks:
    def __init__(self, gui):
        self.lock_1 = threading.RLock()
        self.lock_2 = threading.RLock()
        self.count = 0
        self.gui = gui  # Pass in the GUI object to update interface
        self.thread_1_running = False
        self.thread_2_running = False

    def log(self, message):
        print(message)  # Print to terminal
        self.gui.update_log(message)  # Print to GUI


def thread_1_routine(locks):
    locks.thread_1_running = True
    tid = threading.current_thread().name
    locks.log(f"{tid}: Attempting to acquire lock_1")
    time.sleep(1)  # 1-second delay

    with locks.lock_1:
        locks.log(f"{tid}: Acquired lock_1")
        locks.gui.update_lock_status("lock_1", tid)
        locks.gui.update_thread_status("thread_1", "Working with lock_1")
        time.sleep(1)  # 1-second delay

        locks.log(f"{tid}: Attempting to acquire lock_2")
        locks.gui.update_thread_status("thread_1", "Waiting for lock_2")
        time.sleep(1)  # 1-second delay
        with locks.lock_2:
            locks.log(f"{tid}: Acquired lock_2")
            locks.gui.update_lock_status("lock_2", tid)
            locks.gui.update_thread_status("thread_1", "Working with both locks")
            locks.count += 1
            locks.log(f"{tid}: Updated count to {locks.count}")
            time.sleep(1)  # 1-second delay

        locks.gui.update_lock_status("lock_2", "Released")
        locks.gui.update_thread_status("thread_1", "Released lock_2")

    locks.gui.update_lock_status("lock_1", "Released")
    locks.gui.update_thread_status("thread_1", "Finished")
    locks.log(f"{tid}: Released lock_1 and finished")
    locks.thread_1_running = False


def thread_2_routine(locks):
    locks.thread_2_running = True
    tid = threading.current_thread().name
    locks.log(f"{tid}: Attempting to acquire lock_2")
    time.sleep(1)  # 1-second delay

    with locks.lock_2:
        locks.log(f"{tid}: Acquired lock_2")
        locks.gui.update_lock_status("lock_2", tid)
        locks.gui.update_thread_status("thread_2", "Working with lock_2")
        time.sleep(1)  # 1-second delay

        locks.log(f"{tid}: Attempting to acquire lock_1")
        locks.gui.update_thread_status("thread_2", "Waiting for lock_1")
        time.sleep(1)  # 1-second delay
        with locks.lock_1:
            locks.log(f"{tid}: Acquired lock_1")
            locks.gui.update_lock_status("lock_1", tid)
            locks.gui.update_thread_status("thread_2", "Working with both locks")
            locks.count += 1
            locks.log(f"{tid}: Updated count to {locks.count}")
            time.sleep(1)  # 1-second delay

        locks.gui.update_lock_status("lock_1", "Released")
        locks.gui.update_thread_status("thread_2", "Released lock_1")

    locks.gui.update_lock_status("lock_2", "Released")
    locks.gui.update_thread_status("thread_2", "Finished")
    locks.log(f"{tid}: Released lock_2 and finished")
    locks.thread_2_running = False


class ThreadGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mutex Lock Demonstration")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Set styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", padding=6, relief="flat", background="#4CAF50")
        self.style.configure("Running.TLabel", foreground="blue", background="#f0f0f0", font=('Arial', 10, 'bold'))
        self.style.configure("Locked.TLabel", foreground="red", background="#f0f0f0", font=('Arial', 10, 'bold'))
        self.style.configure("Free.TLabel", foreground="green", background="#f0f0f0", font=('Arial', 10, 'bold'))
        self.style.configure("Title.TLabel", foreground="#333333", background="#f0f0f0", font=('Arial', 14, 'bold'))
        self.style.configure("Header.TLabel", foreground="#555555", background="#f0f0f0", font=('Arial', 12, 'bold'))
        
        # Main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title and description
        title_label = ttk.Label(main_frame, text="Mutex Lock Demonstration", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")
        
        desc_label = ttk.Label(main_frame, text="This simulation demonstrates how threads interact with mutex locks and potential deadlock situations.", 
                         wraplength=760)
        desc_label.grid(row=1, column=0, columnspan=3, pady=(0, 15), sticky="w")
        
        # Left panel - Controls and status
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=2, column=0, padx=(0, 10), sticky="nsew")
        
        # Thread controls section
        controls_frame = ttk.LabelFrame(left_frame, text="Thread Controls")
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(controls_frame, text="Start individual threads:").grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        self.thread_1_button = ttk.Button(controls_frame, text="Start Thread 1", command=self.start_thread_1)
        self.thread_1_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        self.thread_2_button = ttk.Button(controls_frame, text="Start Thread 2", command=self.start_thread_2)
        self.thread_2_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.start_both_button = ttk.Button(controls_frame, text="Start Both Threads", command=self.start_both_threads)
        self.start_both_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        self.reset_button = ttk.Button(controls_frame, text="Reset", command=self.reset_simulation)
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Status section
        status_frame = ttk.LabelFrame(left_frame, text="Current Status")
        status_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        # Lock status
        ttk.Label(status_frame, text="Lock Status:", style="Header.TLabel").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.lock_1_status_frame = ttk.Frame(status_frame)
        self.lock_1_status_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=2)
        ttk.Label(self.lock_1_status_frame, text="Lock 1:").pack(side=tk.LEFT)
        self.lock_1_label = ttk.Label(self.lock_1_status_frame, text="Released", style="Free.TLabel")
        self.lock_1_label.pack(side=tk.LEFT, padx=5)
        
        self.lock_2_status_frame = ttk.Frame(status_frame)
        self.lock_2_status_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=2)
        ttk.Label(self.lock_2_status_frame, text="Lock 2:").pack(side=tk.LEFT)
        self.lock_2_label = ttk.Label(self.lock_2_status_frame, text="Released", style="Free.TLabel")
        self.lock_2_label.pack(side=tk.LEFT, padx=5)
        
        # Thread status
        ttk.Label(status_frame, text="Thread Status:", style="Header.TLabel").grid(row=3, column=0, sticky="w", padx=5, pady=(10, 5))
        
        self.thread_1_status_frame = ttk.Frame(status_frame)
        self.thread_1_status_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=2)
        ttk.Label(self.thread_1_status_frame, text="Thread 1:").pack(side=tk.LEFT)
        self.thread_1_status = ttk.Label(self.thread_1_status_frame, text="Not started", style="Free.TLabel")
        self.thread_1_status.pack(side=tk.LEFT, padx=5)
        
        self.thread_2_status_frame = ttk.Frame(status_frame)
        self.thread_2_status_frame.grid(row=5, column=0, sticky="ew", padx=5, pady=2)
        ttk.Label(self.thread_2_status_frame, text="Thread 2:").pack(side=tk.LEFT)
        self.thread_2_status = ttk.Label(self.thread_2_status_frame, text="Not started", style="Free.TLabel")
        self.thread_2_status.pack(side=tk.LEFT, padx=5)
        
        # Count display
        ttk.Label(status_frame, text="Shared Counter:", style="Header.TLabel").grid(row=6, column=0, sticky="w", padx=5, pady=(10, 5))
        self.count_display = ttk.Label(status_frame, text="0", font=('Arial', 16, 'bold'))
        self.count_display.grid(row=7, column=0, padx=5, pady=5)
        
        self.evaluate_button = ttk.Button(status_frame, text="Evaluate Count", command=self.evaluate_count)
        self.evaluate_button.grid(row=8, column=0, padx=5, pady=5, sticky="ew")
        
        # Right panel - Log display
        log_frame = ttk.LabelFrame(main_frame, text="Execution Log")
        log_frame.grid(row=2, column=1, padx=(10, 0), sticky="nsew")
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=50)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED)  # Make it read-only
        
        # Set column and row weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(2, weight=1)
        
        # Initialize Locks object with GUI reference
        self.locks = Locks(self)
        
        # Add explanation text
        explanation_frame = ttk.Frame(main_frame)
        explanation_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        explanation_text = """
This demonstration shows potential deadlock situations with mutex locks:
• Thread 1 acquires Lock 1 first, then tries to acquire Lock 2
• Thread 2 acquires Lock 2 first, then tries to acquire Lock 1
• If both threads run simultaneously, they may deadlock (each waiting for the other's lock)
        """
        explanation_label = ttk.Label(explanation_frame, text=explanation_text, wraplength=760, justify=tk.LEFT)
        explanation_label.pack(fill=tk.X, pady=5)
        
        # Initial update for count display
        self.update_count_display()

    def update_log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)  # Scroll to the bottom
        self.log_text.config(state=tk.DISABLED)  # Make it read-only again

    def update_lock_status(self, lock_name, status):
        if lock_name == "lock_1":
            if status == "Released":
                self.lock_1_label.config(text="Released", style="Free.TLabel")
            else:
                self.lock_1_label.config(text=f"Held by {status}", style="Locked.TLabel")
        elif lock_name == "lock_2":
            if status == "Released":
                self.lock_2_label.config(text="Released", style="Free.TLabel")
            else:
                self.lock_2_label.config(text=f"Held by {status}", style="Locked.TLabel")
        
        # Update the count display whenever lock status changes
        self.update_count_display()

    def update_thread_status(self, thread_name, status):
        if thread_name == "thread_1":
            self.thread_1_status.config(text=status, 
                                       style="Running.TLabel" if status != "Finished" and status != "Not started" else "Free.TLabel")
        elif thread_name == "thread_2":
            self.thread_2_status.config(text=status,
                                       style="Running.TLabel" if status != "Finished" and status != "Not started" else "Free.TLabel")

    def update_count_display(self):
        self.count_display.config(text=str(self.locks.count))

    def start_thread_1(self):
        if not self.locks.thread_1_running:
            thread_1 = threading.Thread(target=thread_1_routine, args=(self.locks,), name="Thread-1")
            thread_1.daemon = True  # Make thread daemon so it exits when main thread exits
            thread_1.start()
            self.update_log("Main: Started Thread 1")
            self.update_thread_status("thread_1", "Starting...")
        else:
            messagebox.showinfo("Already Running", "Thread 1 is already running!")

    def start_thread_2(self):
        if not self.locks.thread_2_running:
            thread_2 = threading.Thread(target=thread_2_routine, args=(self.locks,), name="Thread-2")
            thread_2.daemon = True  # Make thread daemon so it exits when main thread exits
            thread_2.start()
            self.update_log("Main: Started Thread 2")
            self.update_thread_status("thread_2", "Starting...")
        else:
            messagebox.showinfo("Already Running", "Thread 2 is already running!")

    def start_both_threads(self):
        # Start both threads with a small random delay between them
        if not self.locks.thread_1_running and not self.locks.thread_2_running:
            self.start_thread_1()
            
            # Add a small random delay to increase the chance of demonstrating deadlock
            delay = random.uniform(0.1, 0.3)
            self.root.after(int(delay * 1000), self.start_thread_2)
            
            self.update_log(f"Main: Started both threads with {delay:.2f}s delay")
        else:
            messagebox.showinfo("Already Running", "One or both threads are already running!")

    def reset_simulation(self):
        # Check if threads are still running
        if self.locks.thread_1_running or self.locks.thread_2_running:
            messagebox.showwarning("Threads Running", 
                                  "Cannot reset while threads are running. Wait for them to finish.")
            return
            
        # Reset locks and count
        self.locks = Locks(self)
        
        # Reset UI elements
        self.update_lock_status("lock_1", "Released")
        self.update_lock_status("lock_2", "Released")
        self.update_thread_status("thread_1", "Not started")
        self.update_thread_status("thread_2", "Not started")
        self.update_count_display()
        
        # Clear log
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.update_log("Main: Simulation reset")

    def evaluate_count(self):
        # Final count evaluation for correctness
        total_threads_run = 0
        if self.thread_1_status.cget("text") == "Finished":
            total_threads_run += 1
        if self.thread_2_status.cget("text") == "Finished":
            total_threads_run += 1
            
        if total_threads_run == 0:
            self.update_log("Main: No threads have completed yet")
        elif self.locks.count == total_threads_run:
            self.update_log(f"Main: OK. Total count is {self.locks.count} as expected for {total_threads_run} completed threads")
        else:
            self.update_log(f"Main: ERROR! Total count is {self.locks.count} but {total_threads_run} threads completed")


# Run the Tkinter GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = ThreadGUI(root)
    root.mainloop()
