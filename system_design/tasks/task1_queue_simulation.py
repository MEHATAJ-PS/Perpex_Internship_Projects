import time
import threading
import random

class TaskQueue:
    def __init__(self):
        self.queue = []  
        self.lock = threading.Lock()  # Prevent race conditions

    def enqueue(self, task):
        """Add a task to the queue (FIFO)"""
        with self.lock:
            self.queue.append(task)
            print(f"Task added: {task}")

    def dequeue(self):
        """Remove and return the first task"""
        with self.lock:
            if not self.queue:
                return None
            return self.queue.pop(0)

    def is_empty(self):
        """Check if queue is empty"""
        with self.lock:
            return len(self.queue) == 0

def worker(worker_id, task_queue):
    """Worker function to process tasks"""
    while True:
        task = task_queue.dequeue()
        if task is None:
            break  # No more tasks
        print(f"[Worker {worker_id}] Processing: {task}")
        time.sleep(random.uniform(0.5, 2.0))  # Simulate processing time
        print(f"[Worker {worker_id}] Completed: {task}")

# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    q = TaskQueue()

    # Add tasks to queue
    for i in range(10):
        q.enqueue(f"Task {i+1}")

    # Create multiple worker threads
    workers = []
    for i in range(3):  # 3 workers
        t = threading.Thread(target=worker, args=(i+1, q))
        workers.append(t)
        t.start()

    # Wait for all workers to finish
    for t in workers:
        t.join()

    print("✅ All tasks processed.")

