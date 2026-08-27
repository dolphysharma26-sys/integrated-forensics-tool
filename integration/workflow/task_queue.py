"""
Task Queue Module
Manages operation queue for the forensics tool
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import queue
import threading
from dataclasses import dataclass
from typing import Any, Optional, Callable
from enum import Enum
from core.common.logger import setup_logger

logger = setup_logger(__name__)

class TaskStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

@dataclass
class Task:
    """Represents a task in the queue"""
    task_id: str
    name: str
    function: Callable
    args: tuple = ()
    kwargs: dict = None
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: str = None

class TaskQueue:
    """Manages task execution queue"""
    
    def __init__(self, max_workers: int = 1):
        self.queue = queue.Queue()
        self.max_workers = max_workers
        self.workers = []
        self.tasks = {}
        self.running = False
        self.lock = threading.Lock()
        logger.info(f"Task Queue initialized with {max_workers} workers")
    
    def add_task(self, task: Task) -> str:
        """Add task to queue"""
        with self.lock:
            self.tasks[task.task_id] = task
            self.queue.put(task)
            logger.info(f"Task added: {task.name} (ID: {task.task_id})")
        return task.task_id
    
    def start(self):
        """Start worker threads"""
        if self.running:
            return
        
        self.running = True
        
        for i in range(self.max_workers):
            worker = threading.Thread(
                target=self._worker_loop,
                name=f"Worker-{i+1}",
                daemon=True
            )
            worker.start()
            self.workers.append(worker)
        
        logger.info(f"Started {self.max_workers} workers")
    
    def stop(self):
        """Stop worker threads"""
        self.running = False
        
        # Add sentinel tasks to stop workers
        for _ in self.workers:
            self.queue.put(None)
        
        for worker in self.workers:
            worker.join(timeout=5)
        
        self.workers.clear()
        logger.info("Task Queue stopped")
    
    def _worker_loop(self):
        """Worker thread loop"""
        while self.running:
            try:
                task = self.queue.get(timeout=1)
                
                if task is None:  # Sentinel to stop
                    break
                
                # Execute task
                task.status = TaskStatus.RUNNING
                logger.info(f"Executing: {task.name}")
                
                try:
                    kwargs = task.kwargs or {}
                    task.result = task.function(*task.args, **kwargs)
                    task.status = TaskStatus.COMPLETED
                    logger.info(f"Completed: {task.name}")
                except Exception as e:
                    task.status = TaskStatus.FAILED
                    task.error = str(e)
                    logger.error(f"Failed: {task.name} - {e}")
                
                self.queue.task_done()
                
            except queue.Empty:
                continue
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get task status"""
        task = self.tasks.get(task_id)
        return task.status if task else None
    
    def get_task_result(self, task_id: str) -> Any:
        """Get task result"""
        task = self.tasks.get(task_id)
        return task.result if task else None

if __name__ == "__main__":
    import time
    
    def sample_task(name):
        time.sleep(1)
        return f"Result from {name}"
    
    tq = TaskQueue(max_workers=2)
    tq.start()
    
    task1 = Task("1", "Task 1", sample_task, ("First",))
    task2 = Task("2", "Task 2", sample_task, ("Second",))
    
    tq.add_task(task1)
    tq.add_task(task2)
    
    time.sleep(3)
    tq.stop()
    
    print(f"Task 1: {tq.get_task_result('1')}")
    print(f"Task 2: {tq.get_task_result('2')}")