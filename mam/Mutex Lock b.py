import threading
import time

critical_section_available = True

def release():
    global critical_section_available
    critical_section_available = True

def lock_critical():
    global critical_section_available
    while True:
        if critical_section_available:
            print(f"{threading.current_thread().name} is trying to enter...")
            if not critical_section_available:
                print(f"{threading.current_thread().name}: Another thread is using critical section")
                continue
            critical_section_available = False
            break

    for i in range(10):
        print(f"Using {threading.current_thread().name}")
        time.sleep(0.1)

    print(f"{threading.current_thread().name} is releasing...")
    release()

t1 = threading.Thread(target=lock_critical, name="Thread-1")
t2 = threading.Thread(target=lock_critical, name="Thread-2")

t1.start()
t2.start()

