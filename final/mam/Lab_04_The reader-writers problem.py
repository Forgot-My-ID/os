import tkinter as tk
import threading
import time
import random


class ReadersWritersSimulation:
    def __init__(self, master):
        self.master = master
        self.master.title("Readers-Writers Problem Simulation")
        self.master.geometry("800x400")

        # Shared data and lock variables
        self.database = "Shared Data"
        self.reader_count = 0
        self.lock = threading.Lock()  # Protects the reader_count
        self.writer_lock = threading.Lock()  # Ensures only one writer

        # Canvas for visualization
        self.canvas = tk.Canvas(self.master, width=800, height=300, bg="lightgray")
        self.canvas.pack()

        # Labels
        self.label = tk.Label(self.master, text="Simulation Running...", font=("Arial", 14))
        self.label.pack()

        # Readers and writer visualization
        self.reader_rects = []
        self.writer_rect = None
        self.create_visual_elements()

        # Start the simulation
        threading.Thread(target=self.run_simulation, daemon=True).start()

    def create_visual_elements(self):
        """
        Create visual elements for readers and writer.
        """
        # Readers visualization
        for i in range(5):  # Five readers
            rect = self.canvas.create_rectangle(50 + i * 100, 50, 100 + i * 100, 100, fill="green", outline="black")
            self.reader_rects.append(rect)

        # Writer visualization
        self.writer_rect = self.canvas.create_rectangle(350, 150, 450, 200, fill="red", outline="black")

    def simulate_reader(self, reader_id):
        """
        Simulate a reader accessing the shared database.
        """
        while True:
            time.sleep(random.randint(1, 3))  # Random delay before attempting to read
            with self.lock:
                self.reader_count += 1
                if self.reader_count == 1:  # First reader locks the writer
                    self.writer_lock.acquire()
                self.canvas.itemconfig(self.reader_rects[reader_id], fill="yellow")  # Indicate reading
                self.update_label(f"Reader {reader_id + 1} is reading. Total readers: {self.reader_count}")

            time.sleep(2)  # Simulate reading time

            with self.lock:
                self.reader_count -= 1
                if self.reader_count == 0:  # Last reader unlocks the writer
                    self.writer_lock.release()
                self.canvas.itemconfig(self.reader_rects[reader_id], fill="green")  # Done reading
                self.update_label(f"Reader {reader_id + 1} finished reading. Total readers: {self.reader_count}")

    def simulate_writer(self):
        """
        Simulate a writer accessing the shared database.
        """
        while True:
            time.sleep(random.randint(3, 5))  # Random delay before attempting to write
            self.writer_lock.acquire()  # Lock to ensure exclusive access
            self.canvas.itemconfig(self.writer_rect, fill="orange")  # Indicate writing
            self.update_label("Writer is writing to the database.")
            time.sleep(4)  # Simulate writing time
            self.canvas.itemconfig(self.writer_rect, fill="red")  # Done writing
            self.update_label("Writer finished writing.")
            self.writer_lock.release()

    def run_simulation(self):
        """
        Start threads for readers and writer.
        """
        # Start readers
        for i in range(len(self.reader_rects)):
            threading.Thread(target=self.simulate_reader, args=(i,), daemon=True).start()

        # Start writer
        threading.Thread(target=self.simulate_writer, daemon=True).start()

    def update_label(self, message):
        """
        Update the status label on the GUI.
        """
        self.label.config(text=message)


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = ReadersWritersSimulation(root)
    root.mainloop()
