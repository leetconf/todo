import os
import json
import sys
import logging

from dataclasses import asdict
from .models import Task

class Database:
    def __init__(self, tasks_file: str) -> None:
        self.tasks_file = tasks_file
    
    def load_tasks(self) -> list[Task | None]:
        if not os.path.exists(self.tasks_file):
            return []
        try:
            with open(self.tasks_file, "r", encoding="utf-8") as file:
                tasks_data = json.load(file)
        except json.decoder.JSONDecodeError:
            logging.error("Database file is corrupted")
            sys.exit(1)

        return [Task(**task) for task in tasks_data]
    
    def find_task(self, id: int) -> Task | None:
        tasks = self.load_tasks()
        task = next((task for task in tasks if task.id == id), None)
        if not task:
            logging.warning(f"There was no task with ID {id}")
        return task
    
    def update_task(self, updated_version: Task) -> None:
        tasks = self.load_tasks()
        for number, task in enumerate(tasks):
            if task.id == updated_version.id:
                tasks[number] = updated_version
                break
        self.save_tasks(tasks)
    
    def save_tasks(self, tasks: list[Task]) -> None:
        with open(self.tasks_file, "w", encoding="utf-8") as file:
            tasks_dict = [asdict(task) for task in tasks]
            json.dump(tasks_dict, file, indent=4)

    def add_task(self, description: str) -> None:
        tasks = self.load_tasks()
        if tasks:
            new_task_id = max(task.id for task in tasks) + 1
        else:
            new_task_id = 1
            
        new_task = Task(id=new_task_id, description=description, completed=False)
        tasks.append(new_task)
        self.save_tasks(tasks)

    def remove_task(self, id: int) -> bool:
        tasks = self.load_tasks()
        task = self.find_task(id)
        if task:
            tasks.remove(task)
            self.save_tasks(tasks)