## What's Happening in These Examples:

1. **In the fork example**: The parent process creates a child copy. Both processes continue running the same code but take different paths at the if statement. You'll see two separate PIDs printed.
2. **In the exec example**: The program forks a child process, then the child replaces itself with the `ps` command, showing a list of running processes (including itself before the replacement).

## Example 1: Using fork()

This program demonstrates how fork() creates a child process that's a copy of the parent:

```python
import os
import time

def main():
    print(f"Parent process started with PID: {os.getpid()}")
    
    # Fork creates a child process
    child_pid = os.fork()
    
    if child_pid == 0:
        # This code runs in the child process
        print(f"Child process with PID: {os.getpid()}")
        print(f"Child's parent PID: {os.getppid()}")
        time.sleep(5)  # Keep child running for a while
        print("Child process ending")
    else:
        # This code runs in the parent process
        print(f"Parent process. Created child with PID: {child_pid}")
        time.sleep(10)  # Keep parent running longer than child
        print("Parent process ending")

if __name__ == "__main__":
    main()
```

## Example 2: Using exec()

This program shows how exec() replaces the current process with a new program:

```python
import os
import sys

def main():
    print(f"Original process with PID: {os.getpid()}")
    
    # Fork a child process
    child_pid = os.fork()
    
    if child_pid == 0:
        # This is the child process
        print(f"Child process with PID: {os.getpid()} before exec")
        print("Child will now execute 'ps aux' command...")
        
        # Replace the current process with the 'ps' command
        os.execvp("ps", ["ps", "aux"])
        
        # This code will never be executed because exec replaces the process
        print("This will never be printed")
    else:
        # This is the parent process
        print(f"Parent process. Child has PID: {child_pid}")
        # Wait for child to complete
        os.waitpid(child_pid, 0)
        print("Parent process: child has finished")

if __name__ == "__main__":
    main()
```

## How to Run and Monitor These Programs

1. Save the first example as `fork_example.py` and the second as `exec_example.py`

2. Make them executable:

   ```bash
   chmod +x fork_example.py
   chmod +x exec_example.py
   ```

3. Run the programs:

   ```bash
   python3 fork_example.py
   ```

   ```bash
   python3 exec_example.py
   ```

4. While the programs are running, you can monitor the processes in Linux using various commands:

   - Using `ps` to see processes:

     ```bash
     ps aux | grep python
     ```

   - Using `pstree` to see process hierarchy:

     ```bash
     pstree -p | grep python
     ```

   - Using `top` to see processes in real-time:

     ```bash
     top
     ```

   - For a graphical view (if available):

     ```bash
     gnome-system-monitor
     ```