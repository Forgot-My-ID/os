import time
import matplotlib.pyplot as plt
from multiprocessing import Process, current_process

def run_task(process_id, burst_time):
    """
    Simulates a process running with a specific burst time.
    """
    process_pid = current_process().pid  # Get process ID
    print(f"Process {process_id} (Process ID: {process_pid}) started with burst time {burst_time}")
    time.sleep(burst_time)  # Simulate the process by sleeping for burst time
    print(f"Process {process_id} (Process ID: {process_pid}) completed after {burst_time} seconds")

if __name__ == "__main__":
    main_pid = current_process().pid  # Get main process ID
    print(f"Main Process ID: {main_pid}\n")

    # Get the number of processes
    num_process = int(input("Number of processes: "))
    process_data = []

    # Collect process data
    for i in range(num_process):
        print(f"Process {i}:")
        arrival = float(input("Arrival time: "))
        burst = float(input("Burst time: "))
        process_data.append((i, arrival, burst))

    # Sort processes by arrival time for FCFS scheduling
    process_data.sort(key=lambda x: x[1])

    # Scheduling and Execution
    current_time = 0
    system_idle = 0
    entry_times = []
    exit_times = []
    turnaround_times = []
    waiting_times = []

    for process_id, arrival, burst in process_data:
        if current_time < arrival:
            system_idle += arrival - current_time
            current_time = arrival

        # Start the external process for each task
        start_time = current_time
        process = Process(target=run_task, args=(process_id, burst))
        process.start()
        process.join()  # Wait for the process to finish (simulating FCFS)

        end_time = start_time + burst
        entry_times.append(start_time)
        exit_times.append(end_time)
        current_time = end_time

        # Calculate turnaround and waiting times
        turnaround_time = end_time - arrival
        waiting_time = start_time - arrival
        turnaround_times.append(turnaround_time)
        waiting_times.append(waiting_time)

    # Display results
    print("\nProcess Execution Order:", [f"P{process_id}" for process_id, _, _ in process_data])
    print("Total System Idle Time:", system_idle)
    print("System Utilization:", ((current_time - system_idle) / current_time) * 100, "%")

    # Display turnaround and waiting times
    print("\nProcess-wise Times:")
    for i, (process_id, arrival, burst) in enumerate(process_data):
        print(f"P{process_id}: Turnaround Time = {turnaround_times[i]}s, Waiting Time = {waiting_times[i]}s")

    # Calculate and display averages
    avg_turnaround_time = sum(turnaround_times) / num_process
    avg_waiting_time = sum(waiting_times) / num_process
    print("\nAverage Turnaround Time:", avg_turnaround_time)
    print("Average Waiting Time:", avg_waiting_time)

    # Plot Gantt Chart
    plt.barh(
        y=[f"P{process_id}" for process_id, _, _ in process_data],
        width=[burst for _, _, burst in process_data],
        left=entry_times,
        align='center',
        edgecolor='black'
    )
    plt.xlabel("Time")
    plt.ylabel("Process")
    plt.title("FCFS Scheduling Gantt Chart")
    plt.show()
