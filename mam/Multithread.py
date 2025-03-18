import threading
import time

def work(loop_counter, thread_name):
    for i in range(loop_counter):
        print(f"{thread_name} is working... ({i+1}/{loop_counter})")
        time.sleep(0.1)

# creating threads
t1 = threading.Thread(target=work, args=(10, 'Thread-1'))
t2 = threading.Thread(target=work, args=(5, 'Thread-2'))
t3 = threading.Thread(target=work, args=(10, 'Thread-3'))

t1.start()
t2.start()
t3.start()

# Wait for thread 2 to finish before printing the final message
t2.join()

# Print a message after Thread 2 finishes
print("\n[Main] Thread-2 has finished its work. Now continuing with the rest...")

# Joining remaining threads after the main message
t1.join()
t3.join()

print("\n[Main] All threads have completed.")
