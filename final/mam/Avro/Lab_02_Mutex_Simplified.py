import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox


class Locks:
    def __init__(self):
        self.lock_1 = threading.RLock()
        self.lock_2 = threading.RLock()
        self.count = 0
        self.thread_1_running = False
        self.thread_2_running = False


class SimpleMutexDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Mutex Lock Demo")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # Initialize locks
        self.locks = Locks()
        
        # Configure overall layout
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Mutex Lock Demonstration", font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Log")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.log_text = tk.Text(log_frame, height=10, width=50)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        # Lock status
        locks_frame = ttk.LabelFrame(status_frame, text="Lock Status")
        locks_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.lock1_label = ttk.Label(locks_frame, text="Lock 1: Free")
        self.lock1_label.pack(pady=2)
        
        self.lock2_label = ttk.Label(locks_frame, text="Lock 2: Free")
        self.lock2_label.pack(pady=2)
        
        # Counter frame
        counter_frame = ttk.LabelFrame(status_frame, text="Counter")
        counter_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.counter_label = ttk.Label(counter_frame, text="0", font=('Arial', 14))
        self.counter_label.pack(padx=5, pady=5)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        self.thread1_button = ttk.Button(control_frame, text="Run Thread 1", 
                                        command=self.start_thread_1)
        self.thread1_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        self.thread2_button = ttk.Button(control_frame, text="Run Thread 2", 
                                        command=self.start_thread_2)
        self.thread2_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        self.both_button = ttk.Button(control_frame, text="Run Both", 
                                     command=self.start_both)
        self.both_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        self.reset_button = ttk.Button(control_frame, text="Reset", 
                                      command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
    
    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)  # Scroll to the bottom
        
    def update_lock_status(self, lock_num, status):
        if lock_num == 1:
            self.lock1_label.config(text=f"Lock 1: {status}")
        else:
            self.lock2_label.config(text=f"Lock 2: {status}")
        
        # Update counter display
        self.counter_label.config(text=str(self.locks.count))
    
    def start_thread_1(self):
        if self.locks.thread_1_running:
            messagebox.showinfo("Info", "Thread 1 is already running!")
            return
            
        self.locks.thread_1_running = True
        thread = threading.Thread(target=self.thread_1_routine)
        thread.daemon = True
        thread.start()
        self.log("Started Thread 1")
    
    def start_thread_2(self):
        if self.locks.thread_2_running:
            messagebox.showinfo("Info", "Thread 2 is already running!")
            return
            
        self.locks.thread_2_running = True
        thread = threading.Thread(target=self.thread_2_routine)
        thread.daemon = True
        thread.start()
        self.log("Started Thread 2")
    
    def start_both(self):
        if self.locks.thread_1_running or self.locks.thread_2_running:
            messagebox.showinfo("Info", "A thread is already running!")
            return
            
        # Start both threads
        self.start_thread_1()
        # Small delay to increase chance of deadlock
        self.root.after(100, self.start_thread_2)
    
    def thread_1_routine(self):
        try:
            self.log("Thread 1: Trying to get Lock 1")
            with self.locks.lock_1:
                self.update_lock_status(1, "Held by Thread 1")
                self.log("Thread 1: Got Lock 1")
                time.sleep(1)
                
                self.log("Thread 1: Trying to get Lock 2")
                with self.locks.lock_2:
                    self.update_lock_status(2, "Held by Thread 1")
                    self.log("Thread 1: Got Lock 2")
                    
                    # Critical section
                    self.locks.count += 1
                    self.log(f"Thread 1: Updated count to {self.locks.count}")
                    time.sleep(0.5)
                
                self.update_lock_status(2, "Free")
                self.log("Thread 1: Released Lock 2")
            
            self.update_lock_status(1, "Free")
            self.log("Thread 1: Released Lock 1")
            self.log("Thread 1: Finished")
        finally:
            self.locks.thread_1_running = False
    
    def thread_2_routine(self):
        try:
            self.log("Thread 2: Trying to get Lock 2")
            with self.locks.lock_2:
                self.update_lock_status(2, "Held by Thread 2")
                self.log("Thread 2: Got Lock 2")
                time.sleep(1)
                
                self.log("Thread 2: Trying to get Lock 1")
                with self.locks.lock_1:
                    self.update_lock_status(1, "Held by Thread 2")
                    self.log("Thread 2: Got Lock 1")
                    
                    # Critical section
                    self.locks.count += 1
                    self.log(f"Thread 2: Updated count to {self.locks.count}")
                    time.sleep(0.5)
                
                self.update_lock_status(1, "Free")
                self.log("Thread 2: Released Lock 1")
            
            self.update_lock_status(2, "Free")
            self.log("Thread 2: Released Lock 2")
            self.log("Thread 2: Finished")
        finally:
            self.locks.thread_2_running = False
    
    def reset(self):
        if self.locks.thread_1_running or self.locks.thread_2_running:
            messagebox.showinfo("Info", "Cannot reset while threads are running")
            return
            
        # Reset locks and counter
        self.locks = Locks()
        
        # Reset UI
        self.log_text.delete(1.0, tk.END)
        self.update_lock_status(1, "Free")
        self.update_lock_status(2, "Free")
        self.log("System reset")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleMutexDemo(root)
    root.mainloop()
