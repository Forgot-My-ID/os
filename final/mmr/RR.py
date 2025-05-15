import time
import threading
import matplotlib.pyplot as plt

def run_task(process_id, exec_time):
    """
    Simulates a process running for a given execution time and prints thread ID.
    """
    thread_id = threading.get_ident()
    print(f"Thread ID {thread_id}: Process {process_id} started for {exec_time} seconds.")
    time.sleep(exec_time)  # Simulate the process
    print(f"Thread ID {thread_id}: Process {process_id} completed execution of {exec_time} seconds.")

def round_robin(process_data, quantum):
    """
    Simulates Round Robin scheduling using multithreading.
    """
    time_elapsed = 0
    process_schedule = []
    queue = []
    waiting_time = [0] * len(process_data)
    turnaround_time = [0] * len(process_data)
    remaining_burst = [burst for _, _, burst in process_data]
    entry_times = []
    exit_times = []

    # Sort processes by arrival time
    process_data.sort(key=lambda x: x[1])

    # Initialize queue with processes as they arrive
    i = 0
    while i < len(process_data) or queue:
        while i < len(process_data) and process_data[i][1] <= time_elapsed:
            queue.append(process_data[i][0])  # Add process ID to the queue
            entry_times.append(time_elapsed)
            i += 1

        if queue:
            process_id = queue.pop(0)
            idx = next(index for index, data in enumerate(process_data) if data[0] == process_id)

            # Process execution for a time quantum or remaining burst time
            exec_time = min(quantum, remaining_burst[idx])
            thread = threading.Thread(target=run_task, args=(process_id, exec_time))
            thread.start()
            thread.join()  # Wait for the thread to finish execution
            remaining_burst[idx] -= exec_time
            time_elapsed += exec_time
            process_schedule.append((process_id, time_elapsed))

            if remaining_burst[idx] > 0:  # If burst time is left, re-enqueue
                queue.append(process_id)
            else:
                turnaround_time[idx] = time_elapsed - process_data[idx][1]
                exit_times.append(time_elapsed)
        else:
            # System is idle
            time_elapsed += 1

    # Calculate waiting time
    for idx, (_, arrival, burst) in enumerate(process_data):
        waiting_time[idx] = turnaround_time[idx] - burst

    return process_schedule, waiting_time, turnaround_time, entry_times, exit_times

def plot_gantt_chart(process_schedule):
    """
    Plots the Gantt chart for the process schedule.
    """
    plt.figure(figsize=(10, 5))
    last_time = 0
    for process_id, end_time in process_schedule:
        plt.barh(f"P{process_id}", end_time - last_time, left=last_time, edgecolor="black")
        last_time = end_time

    plt.xlabel("Time")
    plt.ylabel("Process")
    plt.title("Round Robin Scheduling Gantt Chart")
    plt.show()

if __name__ == "__main__":
    num_process = int(input("Number of processes: "))
    quantum = int(input("Quantum value: "))

    process_data = []
    for i in range(num_process):
        print(f"Process {i}:")
        arrival = float(input("Arrival time: "))
        burst = float(input("Burst time: "))
        process_data.append((i, arrival, burst))

    # Execute Round Robin Scheduling
    process_schedule, waiting_time, turnaround_time, entry_times, exit_times = round_robin(process_data, quantum)

    # Display results
    print("\nProcess Schedule (Process ID = Completion Time):")
    for entry in process_schedule:
        print(f"P{entry[0]} = {entry[1]}")

    print("\nWaiting and Turnaround Times:")
    for idx, (process_id, arrival, burst) in enumerate(process_data):
        print(f"Process {process_id} - Waiting Time: {waiting_time[idx]}, Turnaround Time: {turnaround_time[idx]}")

    # Plot the Gantt Chart
    plot_gantt_chart(process_schedule)
