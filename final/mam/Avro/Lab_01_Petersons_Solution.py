import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time

class PetersonAlgorithmSimulator:
    def __init__(self, root):
        # Shared variables for Peterson's Algorithm
        self.flag = [False, False]
        self.turn = 0
        self.simulation_active = False
        self.simulation_speed = 1.0  # Default speed multiplier
        
        # Setup root window
        self.root = root
        self.root.title("Peterson's Algorithm Visualization")
        self.root.geometry("800x650")
        self.root.configure(bg="#f0f0f5")
        
        # Define styles for a premium look
        self.setup_styles()
        
        # Create main frames
        self.create_explanation_frame()
        self.create_process_frames()
        self.create_control_panel()
        self.create_log_area()
        
        # Initialize components
        self.reset_simulation()
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f5")
        self.style.configure("TLabel", background="#f0f0f5", font=("Arial", 12))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"), background="#f0f0f5")
        self.style.configure("Status.TLabel", font=("Arial", 11, "italic"))
        self.style.configure("ProcessLabel.TLabel", font=("Arial", 14, "bold"), foreground="black")
        self.style.configure("Info.TLabel", font=("Arial", 10), background="#f0f0f5")
        self.style.configure("Variable.TLabel", font=("Consolas", 12), background="#e8e8e8")
        self.style.configure("TButton", font=("Arial", 11))
        self.style.configure("Start.TButton", foreground="green")
        self.style.configure("Reset.TButton", foreground="red")
        
    def create_explanation_frame(self):
        # Frame for explanation
        explanation_frame = ttk.Frame(self.root)
        explanation_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title_label = ttk.Label(explanation_frame, text="Peterson's Algorithm Demonstration", 
                              style="Header.TLabel", font=("Arial", 16, "bold"))
        title_label.pack(anchor="w", pady=(0, 5))
        
        explanation_text = """
Peterson's algorithm is a concurrent programming algorithm for mutual exclusion that allows two 
processes to share a single-use resource without conflict, using only shared memory for communication.

Key concepts:
• Two processes (0 and 1) want to enter their critical sections
• flag[i] indicates if process i wants to enter its critical section
• turn indicates which process has priority when both want to enter
• Mutual exclusion is guaranteed - only one process can be in critical section at a time
        """
        explanation_label = ttk.Label(explanation_frame, text=explanation_text, 
                                    wraplength=760, justify="left")
        explanation_label.pack(anchor="w", pady=5)
    
    def create_process_frames(self):
        # Container for both processes
        processes_container = ttk.Frame(self.root)
        processes_container.pack(fill=tk.X, padx=20, pady=5)
        
        # Left frame - Process 0
        self.frame_0 = ttk.Frame(processes_container, style="TFrame", borderwidth=2, relief="ridge")
        self.frame_0.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="nsew")
        
        process_header_0 = ttk.Label(self.frame_0, text="Process 0", style="ProcessLabel.TLabel")
        process_header_0.pack(pady=(10, 5))
        
        self.status_label_0 = ttk.Label(self.frame_0, text="Non-Critical Section", 
                                       style="Status.TLabel", foreground="black")
        self.status_label_0.pack(pady=5)
        
        # State variables for Process 0
        state_frame_0 = ttk.Frame(self.frame_0)
        state_frame_0.pack(pady=10, fill=tk.X)
        
        ttk.Label(state_frame_0, text="flag[0] = ", style="Info.TLabel").grid(row=0, column=0, sticky="e")
        self.flag_0_label = ttk.Label(state_frame_0, text="False", style="Variable.TLabel", width=6)
        self.flag_0_label.grid(row=0, column=1, sticky="w")
        
        # Visual indicator for Process 0 - will be colored based on state
        self.indicator_0 = tk.Canvas(self.frame_0, width=100, height=100, bg="#f0f0f5", highlightthickness=0)
        self.indicator_0.pack(pady=10)
        self.circle_0 = self.indicator_0.create_oval(10, 10, 90, 90, fill="#d1d1d1", outline="black", width=2)
        
        # Right frame - Process 1
        self.frame_1 = ttk.Frame(processes_container, style="TFrame", borderwidth=2, relief="ridge")
        self.frame_1.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="nsew")
        
        process_header_1 = ttk.Label(self.frame_1, text="Process 1", style="ProcessLabel.TLabel")
        process_header_1.pack(pady=(10, 5))
        
        self.status_label_1 = ttk.Label(self.frame_1, text="Non-Critical Section", 
                                       style="Status.TLabel", foreground="black")
        self.status_label_1.pack(pady=5)
        
        # State variables for Process 1
        state_frame_1 = ttk.Frame(self.frame_1)
        state_frame_1.pack(pady=10, fill=tk.X)
        
        ttk.Label(state_frame_1, text="flag[1] = ", style="Info.TLabel").grid(row=0, column=0, sticky="e")
        self.flag_1_label = ttk.Label(state_frame_1, text="False", style="Variable.TLabel", width=6)
        self.flag_1_label.grid(row=0, column=1, sticky="w")
        
        # Visual indicator for Process 1 - will be colored based on state
        self.indicator_1 = tk.Canvas(self.frame_1, width=100, height=100, bg="#f0f0f5", highlightthickness=0)
        self.indicator_1.pack(pady=10)
        self.circle_1 = self.indicator_1.create_oval(10, 10, 90, 90, fill="#d1d1d1", outline="black", width=2)
        
        # Middle frame for shared variables
        shared_frame = ttk.Frame(processes_container, style="TFrame", borderwidth=2, relief="ridge")
        shared_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        
        shared_label = ttk.Label(shared_frame, text="Shared Variables", style="Header.TLabel")
        shared_label.pack(pady=(10, 5))
        
        turn_frame = ttk.Frame(shared_frame)
        turn_frame.pack(pady=10)
        
        ttk.Label(turn_frame, text="turn = ", style="Info.TLabel").grid(row=0, column=0)
        self.turn_label = ttk.Label(turn_frame, text="0", style="Variable.TLabel", width=2)
        self.turn_label.grid(row=0, column=1)
        
        # Configure grid for equal sizing
        processes_container.columnconfigure(0, weight=1)
        processes_container.columnconfigure(1, weight=1)
        
    def create_control_panel(self):
        # Control panel
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Speed control
        speed_frame = ttk.Frame(control_frame)
        speed_frame.pack(side=tk.TOP, pady=5, fill=tk.X)
        
        ttk.Label(speed_frame, text="Simulation Speed:", style="TLabel").pack(side=tk.LEFT, padx=(0, 10))
        
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(speed_frame, from_=0.1, to=2.0, variable=self.speed_var, 
                             orient=tk.HORIZONTAL, length=200)
        speed_scale.pack(side=tk.LEFT)
        
        speed_label = ttk.Label(speed_frame, textvariable=tk.StringVar(value="1.0x"))
        speed_label.pack(side=tk.LEFT, padx=10)
        
        def update_speed_label(event):
            speed_value = round(self.speed_var.get(), 1)
            self.simulation_speed = speed_value
            speed_label.config(text=f"{speed_value}x")
            
        speed_scale.bind("<Motion>", update_speed_label)
        
        # Button frame
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(pady=10, fill=tk.X)
        
        # Start button
        self.start_button = ttk.Button(button_frame, text="Start Simulation", 
                                     style="Start.TButton", command=self.start_simulation)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Reset button
        self.reset_button = ttk.Button(button_frame, text="Reset", 
                                      style="Reset.TButton", command=self.reset_simulation)
        self.reset_button.pack(side=tk.LEFT)
        
        # Individual process buttons
        self.start_p0_button = ttk.Button(button_frame, text="Start Process 0", 
                                         command=lambda: self.start_single_process(0))
        self.start_p0_button.pack(side=tk.LEFT, padx=10)
        
        self.start_p1_button = ttk.Button(button_frame, text="Start Process 1", 
                                         command=lambda: self.start_single_process(1))
        self.start_p1_button.pack(side=tk.LEFT)
    
    def create_log_area(self):
        # Log area
        log_frame = ttk.LabelFrame(self.root, text="Execution Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)  # Auto-scroll to the bottom
    
    def update_process_0(self, status, color):
        self.status_label_0.config(text=status, foreground=color)
        self.indicator_0.itemconfig(self.circle_0, fill=color)
    
    def update_process_1(self, status, color):
        self.status_label_1.config(text=status, foreground=color)
        self.indicator_1.itemconfig(self.circle_1, fill=color)
    
    def update_flags_and_turn(self):
        # Update flag displays
        self.flag_0_label.config(text=str(self.flag[0]))
        self.flag_1_label.config(text=str(self.flag[1]))
        self.turn_label.config(text=str(self.turn))
    
    def get_delay(self, base_delay):
        """Calculate delay time based on speed setting"""
        return int(base_delay / self.simulation_speed)
    
    def reset_simulation(self):
        # Reset variables
        self.flag = [False, False]
        self.turn = 0
        self.simulation_active = False
        
        # Reset UI
        self.update_process_0("Non-Critical Section", "#d1d1d1")
        self.update_process_1("Non-Critical Section", "#d1d1d1")
        self.update_flags_and_turn()
        self.log("Simulation reset")
        
        # Reset buttons
        self.start_button.config(state="normal")
        self.start_p0_button.config(state="normal")
        self.start_p1_button.config(state="normal")
    
    def start_simulation(self):
        if self.simulation_active:
            messagebox.showinfo("Simulation Active", "Simulation is already running!")
            return
            
        self.simulation_active = True
        self.log("Starting full simulation (both processes)")
        
        # Disable start buttons during simulation
        self.start_button.config(state="disabled")
        self.start_p0_button.config(state="disabled")
        self.start_p1_button.config(state="disabled")
        
        # Clear log for new simulation
        self.log_text.delete(1.0, tk.END)
        
        # Start both processes
        threading.Thread(target=self.peterson_algorithm_0, daemon=True).start()
        
        # Add a slight delay to show the interaction more clearly
        self.root.after(500, lambda: threading.Thread(target=self.peterson_algorithm_1, daemon=True).start())
    
    def start_single_process(self, process_id):
        if self.simulation_active:
            messagebox.showinfo("Simulation Active", "Simulation is already running!")
            return
            
        self.simulation_active = True
        
        # Disable start buttons during simulation
        self.start_button.config(state="disabled")
        self.start_p0_button.config(state="disabled")
        self.start_p1_button.config(state="disabled")
        
        if process_id == 0:
            self.log("Starting Process 0 only")
            threading.Thread(target=self.peterson_algorithm_0, daemon=True).start()
        else:
            self.log("Starting Process 1 only")
            threading.Thread(target=self.peterson_algorithm_1, daemon=True).start()
    
    def peterson_algorithm_0(self):
        # Set flag to indicate interest in entering critical section
        self.log("Process 0: Setting flag[0] = True")
        self.flag[0] = True
        self.update_flags_and_turn()
        self.update_process_0("Entering...", "#87CEEB")  # Light blue
        
        # Set turn to the other process
        self.root.after(self.get_delay(500), lambda: self.set_turn_0())
    
    def set_turn_0(self):
        self.log("Process 0: Setting turn = 1")
        self.turn = 1
        self.update_flags_and_turn()
        
        # Check if we need to wait
        self.root.after(self.get_delay(500), self.check_wait_0)
    
    def check_wait_0(self):
        if self.flag[1] and self.turn == 1:
            self.log("Process 0: Waiting (flag[1] is True and turn = 1)")
            self.update_process_0("Waiting...", "#FFA07A")  # Light salmon
            self.root.after(self.get_delay(1000), self.check_wait_0)
        else:
            self.root.after(self.get_delay(500), self.enter_critical_section_0)
    
    def enter_critical_section_0(self):
        self.log("Process 0: Entering critical section")
        self.update_process_0("In Critical Section", "#32CD32")  # Lime green
        
        # Spend some time in critical section
        self.root.after(self.get_delay(2000), self.exit_critical_section_0)
    
    def exit_critical_section_0(self):
        self.log("Process 0: Exiting critical section")
        self.update_process_0("Exiting...", "#BA55D3")  # Medium orchid
        
        # Reset flag
        self.root.after(self.get_delay(1000), lambda: self.reset_flag_0())
    
    def reset_flag_0(self):
        self.log("Process 0: Setting flag[0] = False")
        self.flag[0] = False
        self.update_flags_and_turn()
        self.update_process_0("Non-Critical Section", "#d1d1d1")  # Light gray
        
        # If this was the only process running or both are done, reset simulation state
        if not self.flag[1]:
            self.simulation_active = False
            self.start_button.config(state="normal")
            self.start_p0_button.config(state="normal")
            self.start_p1_button.config(state="normal")
            self.log("Simulation complete")
    
    def peterson_algorithm_1(self):
        # Set flag to indicate interest in entering critical section
        self.log("Process 1: Setting flag[1] = True")
        self.flag[1] = True
        self.update_flags_and_turn()
        self.update_process_1("Entering...", "#87CEEB")  # Light blue
        
        # Set turn to the other process
        self.root.after(self.get_delay(500), lambda: self.set_turn_1())
    
    def set_turn_1(self):
        self.log("Process 1: Setting turn = 0")
        self.turn = 0
        self.update_flags_and_turn()
        
        # Check if we need to wait
        self.root.after(self.get_delay(500), self.check_wait_1)
    
    def check_wait_1(self):
        if self.flag[0] and self.turn == 0:
            self.log("Process 1: Waiting (flag[0] is True and turn = 0)")
            self.update_process_1("Waiting...", "#FFA07A")  # Light salmon
            self.root.after(self.get_delay(1000), self.check_wait_1)
        else:
            self.root.after(self.get_delay(500), self.enter_critical_section_1)
    
    def enter_critical_section_1(self):
        self.log("Process 1: Entering critical section")
        self.update_process_1("In Critical Section", "#32CD32")  # Lime green
        
        # Spend some time in critical section
        self.root.after(self.get_delay(2000), self.exit_critical_section_1)
    
    def exit_critical_section_1(self):
        self.log("Process 1: Exiting critical section")
        self.update_process_1("Exiting...", "#BA55D3")  # Medium orchid
        
        # Reset flag
        self.root.after(self.get_delay(1000), lambda: self.reset_flag_1())
    
    def reset_flag_1(self):
        self.log("Process 1: Setting flag[1] = False")
        self.flag[1] = False
        self.update_flags_and_turn()
        self.update_process_1("Non-Critical Section", "#d1d1d1")  # Light gray
        
        # If this was the only process running or both are done, reset simulation state
        if not self.flag[0]:
            self.simulation_active = False
            self.start_button.config(state="normal")
            self.start_p0_button.config(state="normal")
            self.start_p1_button.config(state="normal")
            self.log("Simulation complete")


# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PetersonAlgorithmSimulator(root)
    root.mainloop()
