import threading
import time


# Function to simulate job execution
def execute_job(job_id, burst_time):
    thread_id = threading.get_ident()  # Get the current thread's ID
    print(f"Job {job_id} started with burst time {burst_time} units on Thread {thread_id}.")
    time.sleep(burst_time)  # Simulate job execution by sleeping for burst time
    print(f"Job {job_id} completed on Thread {thread_id}.")


# SJF Scheduling Algorithm with Arrival Time
def sjf_schedule(jobs):
    current_time = 0  # Track the current time to simulate arrival time delays
    jobs.sort(key=lambda x: (x[1], x[2]))  # Sort by arrival time, then burst time

    threads = []

    # Start a thread for each job based on its arrival time
    for job_id, arrival_time, burst_time in jobs:
        # If the job arrives later, wait until its arrival time
        if arrival_time > current_time:
            wait_time = arrival_time - current_time
            print(f"Waiting for {wait_time} seconds until Job {job_id} arrives.")
            time.sleep(wait_time)
            current_time = arrival_time  # Update the current time to the job's arrival time

        # Create and start the thread
        thread = threading.Thread(target=execute_job, args=(job_id, burst_time))
        threads.append(thread)
        thread.start()
        thread.join()
        print(f"Job {job_id} scheduled to start at time {arrival_time} on Thread {thread.ident}")

        current_time += burst_time  # Update the current time after the job's execution


def main():
    num_jobs = int(input("Enter the number of jobs: "))

    jobs = []

    # Get the arrival time and burst time for each job
    for i in range(num_jobs):
        job_id = i + 1
        arrival_time = int(input(f"Enter arrival time for Job {job_id}: "))
        burst_time = int(input(f"Enter burst time for Job {job_id}: "))
        jobs.append((job_id, arrival_time, burst_time))

    # Run the SJF scheduling algorithm
    sjf_schedule(jobs)


if __name__ == "__main__":
    main()
