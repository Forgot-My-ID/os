import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def update_input_fields():
    """Dynamically create input fields based on the number of groups."""
    try:
        n_students = int(entry_students.get())
        for widget in frame_details.winfo_children():
            widget.destroy()  # Clear existing input fields

        # Labels for Max Need and Allocation
        tk.Label(frame_details, text="Maximum Need for Each Group:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(frame_details, text="Currently Allocated Resources:").grid(row=0, column=1, padx=10, pady=5)

        global max_need_entries, allocation_entries
        max_need_entries = []
        allocation_entries = []

        for i in range(n_students):
            entry_max = tk.Entry(frame_details)
            entry_alloc = tk.Entry(frame_details)
            max_need_entries.append(entry_max)
            allocation_entries.append(entry_alloc)
            entry_max.grid(row=i + 1, column=0, padx=10, pady=5)
            entry_alloc.grid(row=i + 1, column=1, padx=10, pady=5)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of groups!")


def simulate_queue_and_graph(safe_sequence):
    """Simulate the queue and dynamically update the graph."""
    canvas.delete("all")  # Clear the canvas
    queue_items = []
    x, y = 10, 10
    n_groups = len(safe_sequence)

    # Create visualization of the queue
    for i in safe_sequence:
        rect = canvas.create_rectangle(x, y, x + 100, y + 50, fill="lightblue")
        text = canvas.create_text(x + 50, y + 25, text=f"Group {i + 1}", font=("Arial", 12))
        queue_items.append((rect, text))
        x += 120

    # Prepare the graph
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.set_title("Group Processing Sequence")
    ax.set_xlabel("Groups")
    ax.set_ylabel("Processing Step")
    bar_colors = ["blue"] * n_groups

    for step, group in enumerate(safe_sequence):
        # Highlight the current group in the queue
        canvas.itemconfig(queue_items[step][0], fill="green")
        canvas.update()
        canvas.after(1000)

        # Update the graph
        bar_colors[step] = "green"
        ax.bar([f"Group {i + 1}" for i in safe_sequence], list(range(1, n_groups + 1)), color=bar_colors)
        graph_canvas = FigureCanvasTkAgg(fig, master=frame_graph)
        graph_canvas.get_tk_widget().grid(row=0, column=0)
        graph_canvas.draw()

        # Mark processed group in light gray
        canvas.itemconfig(queue_items[step][0], fill="lightgray")


def is_safe_state_simulation(available, max_need, allocation, need, n_students):
    """Simulate the Banker's Algorithm one group at a time."""
    work = available[:]
    finish = [False] * n_students
    safe_sequence = []
    simulation_steps = []

    while True:
        allocated = False
        for i in range(n_students):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(len(work))):
                simulation_steps.append(
                    f"Group {i + 1} can be satisfied. Resources allocated: {allocation[i]}."
                    f" Available before allocation: {work}. Available after: {[work[j] + allocation[i][j] for j in range(len(work))]}"
                )
                for j in range(len(work)):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                allocated = True
        if not allocated:
            break

    if all(finish):
        return True, safe_sequence, simulation_steps
    return False, None, simulation_steps


def run_bankers_algorithm():
    """Run the Banker's Algorithm."""
    try:
        n_students = int(entry_students.get())
        available = list(map(int, entry_available.get().split()))
        max_need = [list(map(int, max_need_entries[i].get().split())) for i in range(n_students)]
        allocation = [list(map(int, allocation_entries[i].get().split())) for i in range(n_students)]

        need = [[max_need[i][j] - allocation[i][j] for j in range(len(available))] for i in range(n_students)]

        is_safe, safe_sequence, steps = is_safe_state_simulation(available, max_need, allocation, need, n_students)

        result_text = f"Available Resources: {available}\n"
        result_text += f"Maximum Need: {max_need}\n"
        result_text += f"Allocation: {allocation}\n"
        result_text += f"Need: {need}\n\n"

        result_text += "\nSimulation Steps:\n"
        result_text += "\n".join(steps) + "\n\n"

        if is_safe:
            result_text += "The system is in a SAFE state.\n"
            result_text += f"Safe sequence: {' -> '.join(['Group ' + str(i + 1) for i in safe_sequence])}\n\n"
            result_label.config(text=result_text)
            simulate_queue_and_graph(safe_sequence)
        else:
            result_text += "The system is NOT in a safe state. Deadlock may occur!"
            result_label.config(text=result_text)
            canvas.delete("all")  # Clear the canvas if unsafe state

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")


# GUI Setup
root = tk.Tk()
root.title("Banker's Algorithm GUI")
root.geometry("1000x800")

# Frame for inputs
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

# Number of Groups
tk.Label(frame_inputs, text="Number of Groups:").grid(row=0, column=0, padx=5, pady=5)
entry_students = tk.Entry(frame_inputs)
entry_students.grid(row=0, column=1, padx=5, pady=5)

# Update Button for Dynamic Input Fields
tk.Button(frame_inputs, text="Set Number of Groups", command=update_input_fields).grid(row=0, column=2, padx=10, pady=5)

# Available Resources
tk.Label(frame_inputs, text="Available Resources (Tables, Chairs):").grid(row=1, column=0, padx=5, pady=5)
entry_available = tk.Entry(frame_inputs)
entry_available.grid(row=1, column=1, padx=5, pady=5)

# Frame for Max Need and Allocation
frame_details = tk.Frame(root)
frame_details.pack(pady=10)

# Run Button
tk.Button(root, text="Run Banker's Algorithm", command=run_bankers_algorithm).pack(pady=10)

# Result Label
result_label = tk.Label(root, text="", justify="left", wraplength=750, anchor="w")
result_label.pack(pady=10)

# Canvas for Queue Visualization
canvas = tk.Canvas(root, width=750, height=100, bg="white")
canvas.pack(pady=20)

# Frame for Graph
frame_graph = tk.Frame(root)
frame_graph.pack(pady=10)

# Run the GUI event loop
root.mainloop()
