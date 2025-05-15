import threading
import time
import matplotlib.pyplot as plt


# Function to simulate process execution
def execute_process(process_data, timeline, lock):
    process_id, arrival, burst, priority = process_data[0:4]
    entry_time, exit_time, work_done = -1, -1, 0

    # Wait until the process's arrival time
    time.sleep(arrival)

    thread_id = threading.get_ident()  # Get the thread's unique ID
    print(f"Process {process_id} started on Thread {thread_id} with priority {priority}.")

    with lock:
        # Find the start time slot in the timeline for the process
        start = arrival
        while work_done < burst:
            while timeline[start] != -1:  # Look for a free slot
                start += 1
            if timeline[start] == -1:  # Occupy the slot
                timeline[start] = process_id
                work_done += 1
            start += 1

        # Update process entry and exit times
        entry_time = arrival
        exit_time = start
        process_data[4] = entry_time  # entry_time
        process_data[5] = exit_time  # exit_time
        process_data[6] = work_done  # work_done
    time.sleep(burst)
    print(f"Process {process_id} completed on Thread {thread_id}.")


#START
print("Higher numerical value means higher priority")
# Get the number of processes
num_process = int(input("Enter the number of processes: "))
process = []

# Gather input for each process in a single line
for i in range(num_process):
    arrival, burst, priority = map(int, input(
        f"Enter arrival, burst, and priority for Process {i} (e.g., '0 4 4'): ").split())
    process_id = i
    entry_time = -1
    exit_time = -1
    work_done = 0
    data = [process_id, arrival, burst, priority, entry_time, exit_time, work_done]
    process.append(data)

# Sort processes by priority (higher priority first)
process.sort(key=lambda x: x[3], reverse=True)

# Initialize the timeline and a lock for thread synchronization
timeline = [-1 for _ in range(500)]
lock = threading.Lock()
threads = []

# Create and start a thread for each process
for i in range(num_process):
    thread = threading.Thread(target=execute_process, args=(process[i], timeline, lock))
    threads.append(thread)
    thread.start()
    thread.join()


# Calculate Turnaround and Waiting Time
turnaround_time = []
waiting_time = []

process.sort(key=lambda x: x[0])  # Sort by process ID for reporting
for i in range(num_process):
    turnaround_time.append(process[i][5] - process[i][1])
    waiting_time.append(turnaround_time[i] - process[i][2])

# Print results
print("Process          = ", timeline)
print("Timeline         = ", [i + 1 for i in range(len(timeline))])
print("Turnaround Time  = ", turnaround_time)
print("Waiting Time     = ", waiting_time)
