import threading

critical_section_available = True 

def release():
    global critical_section_available
    critical_section_available = True

def lock_critical():
    global critical_section_available
    while critical_section_available == False:
        print(f'{threading.current_thread().name} is trying to enter...')

    critical_section_available = False

    for i in range(10):
        print(f"{threading.current_thread().name} is in critical section\n")
    
    print(f"{threading.current_thread().name} is releasing...")
    release()


t1 = threading.Thread(target=lock_critical, name="Thread-1")
t2 = threading.Thread(target=lock_critical, name="Thread-2")

t1.start()
t2.start()
