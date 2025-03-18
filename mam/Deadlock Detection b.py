import numpy as np

def bankers_algorithm(Allocation, Max, Available):
    Work = Available
    n = len(Allocation)
    Finish = [False for i in range(n)]  # Initially, all processes are unfinished
    Need = np.subtract(Max, Allocation)  # Resources needed by each process

    process_done = []
    process_incomplete = n

    print("\nBanker's Algorithm Execution:")
    print(f"Available Resources: {Available}")
    print("Allocation Matrix:")
    print(Allocation)
    print("Maximum Matrix:")
    print(Max)
    print("Need Matrix:")
    print(Need)
    
    while True:
        if process_incomplete <= 0:  # All processes have been completed
            print("\nSafe State Detected: All processes can complete without causing a deadlock.")
            print("Safe Sequence of Processes:")
            for i in process_done:
                print(f"  Process {i + 1}")  # Display process number starting from 1
            break

        flag = True

        for i in range(n):
            if Finish[i] == False and all(np.less_equal(Need[i], Work)):  # Process can finish
                Finish[i] = True  # Mark process as finished
                Work = np.add(Work, Allocation[i])  # Release resources back to 'Work'
                process_done.append(i)  # Add to safe sequence
                process_incomplete -= 1
                flag = False
                print(f"\nProcess {i + 1} is completing.")
                print(f"  Resources allocated: {Allocation[i]}")
                print(f"  Resources needed: {Need[i]}")
                print(f"  Updated Work (available resources): {Work}")

        if flag:  # If no process could complete, it indicates a deadlock
            print("\nDeadlock Detected: No process could complete with the current available resources.")
            break

# Example matrices
Available = np.array([3, 3, 2])
Allocation = np.array([
    [0, 1, 0],
    [2, 0, 0],
    [3, 0, 2],
    [2, 1, 1],
    [0, 0, 2]
])
Max = np.array([
    [7, 5, 3],
    [3, 2, 2],
    [9, 9, 9],
    [9, 9, 9],
    [9, 9, 9]
])

bankers_algorithm(Allocation, Max, Available)
