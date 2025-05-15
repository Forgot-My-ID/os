import threading
import time
import matplotlib.pyplot as plt

class Process(threading.Thread):
    def __init__(self, process_id, arrival, burst, entry_time=-1, exit_time=-1):
        super().__init__()
        self.process_id = process_id
        self.arrival = arrival
        self.burst = burst
        self.entry_time = entry_time
        self.exit_time = exit_time

    def run(self):
        print(f"Process {self.process_id} started execution at time {self.entry_time}")
        time.sleep(self.burst)  # Simulates process run time
        self.exit_time = self.entry_time + self.burst
        print(f"Process {self.process_id} completed execution at time {self.exit_time}")


# Gather input
num_process = int(input("Enter the number of processes: "))
processes = []

for i in range(num_process):
    arrival, burst = map(float, input(f"Enter arrival and burst time for Process {i} (e.g., '0 3'): ").split())
    processes.append(Process(i, arrival, burst))

# Sort by arrival time for FCFS
processes.sort(key=lambda p: p.arrival)

# Schedule processes
current_time = 0
system_idle = 0
process_schedule = []

# Start each process in order of arrival, simulating FCFS
for process in processes:
    if current_time < process.arrival:
        system_idle += process.arrival - current_time
        current_time = process.arrival

    process.entry_time = current_time
    process.start()  # Start thread (simulating FCFS)
    process.join()  # Ensure process completes before starting the next
    current_time += process.burst
    process_schedule.append(process.process_id)

# Calculate Turnaround and Waiting Time
turnaround_times = []
waiting_times = []

for process in processes:
    turnaround_time = process.exit_time - process.arrival
    waiting_time = turnaround_time - process.burst
    turnaround_times.append(turnaround_time)
    waiting_times.append(waiting_time)
    print(f"Process {process.process_id} Turnaround Time = {turnaround_time}")
    print(f"Process {process.process_id} Waiting Time = {waiting_time}")

# Display results
print("Process Execution Order:", process_schedule)
print("Total System Idle Time:", system_idle)
print("System Utilization:", ((current_time - system_idle) / current_time) * 100, "%")

# Plot Gantt chart
plt.barh(
    y=[f"P{process.process_id}" for process in processes],
    width=[process.burst for process in processes],
    left=[process.entry_time for process in processes]
)
plt.xlabel("Time")
plt.ylabel("Process")
plt.title("FCFS Scheduling Gantt Chart")
plt.show()
