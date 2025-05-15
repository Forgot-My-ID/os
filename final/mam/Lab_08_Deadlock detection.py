import tkinter as tk
import time
import threading


class DeadlockSimulation:
    def __init__(self, master):
        self.master = master
        self.master.title("Deadlock Detection and Recovery Simulation")
        self.master.geometry("600x300")

        # Canvas for visualization
        self.canvas = tk.Canvas(self.master, width=600, height=300, bg="lightgray")
        self.canvas.pack()

        # Draw road (single lane)
        self.canvas.create_rectangle(0, 100, 600, 200, fill="black", outline="")

        # Cars (represented by rectangles)
        self.car1 = self.canvas.create_rectangle(100, 120, 140, 160, fill="blue")  # Car moving right
        self.car2 = self.canvas.create_rectangle(500, 120, 540, 160, fill="red")   # Car moving left

        # Labels
        self.label = tk.Label(self.master, text="Simulation Running...", font=("Arial", 14))
        self.label.pack()

        # Control variables
        self.deadlock_detected = False

        # Start the simulation
        self.run_simulation()

    def move_car(self, car, direction, speed):
        """
        Move a car in a specified direction with a constant speed.
        """
        while not self.deadlock_detected:
            x1, y1, x2, y2 = self.canvas.coords(car)

            # Move car
            self.canvas.move(car, direction * speed, 0)
            time.sleep(0.05)

            # Check for deadlock
            if self.check_deadlock():
                self.detect_deadlock()
                break

    def check_deadlock(self):
        """
        Check if the distance between the two cars is less than or equal to 5 pixels.
        """
        x1, _, x2, _ = self.canvas.coords(self.car1)  # Coordinates of car1
        x3, _, x4, _ = self.canvas.coords(self.car2)  # Coordinates of car2

        # Calculate distance between the nearest edges of the two cars
        distance = min(abs(x2 - x3), abs(x4 - x1))
        return distance <= 5

    def detect_deadlock(self):
        """
        Stop both cars and display a deadlock detected message.
        """
        self.deadlock_detected = True
        self.label.config(text="Deadlock Detected!")  # Update label
        print("Deadlock detected!")  # Log to the console

    def car1_thread(self):
        self.move_car(self.car1, direction=1, speed=2)  # Car 1 moves right

    def car2_thread(self):
        self.move_car(self.car2, direction=-1, speed=4)  # Car 2 moves left

    def run_simulation(self):
        """
        Run the two cars in separate threads.
        """
        threading.Thread(target=self.car1_thread, daemon=True).start()
        threading.Thread(target=self.car2_thread, daemon=True).start()


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = DeadlockSimulation(root)
    root.mainloop()
