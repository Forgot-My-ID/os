// Java Program to illustrate difference between 
// start() method thread vs show() method 

// Class 1
// Helper thread Class extending main Thread Class
class MyThread1 extends Thread {

    // Method inside MyThread2
    // run() method which is called as soon as thread is
    // started
    public void run() {

        // Print statement when the thread is called
        System.out.println("Thread 1 is running");
    }
}

// Class 2
// Main thread Class extending main Thread Class
class MyThread2 extends Thread {

    // Method
    public void show() {

        // Print statement when thread is called
        System.out.println("Thread 2");
    }
}

// Class 3
// Main Class
class CaseC {

    // Main method
    public static void main(String[] args) {

        // Creating a thread object of our thread class
        MyThread1 obj1 = new MyThread1();
        MyThread2 obj2 = new MyThread2();

        // Getting the threads to the run state

        // This thread will transcend from runnable to run
        // as start() method will look for run() and execute
        // it
        obj1.start();

        // This thread is simply a function call as
        // no start() method is executed so here only
        // thread is created only followed by call
        obj2.show();
    }
}
