from database import Database
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.db = Database()
        self.db.create_tasks_table()

    def run(self, user):
        while True:
            print(f"\nTask Management for {user['username']}")
            print("1. Create Task")
            print("2. View Tasks")
            print("3. Update Task")
            print("4. Delete Task")
            print("5. Logout")
            choice = input("Choose an option (1-5): ")

            if choice == '1':
                self.create_task(user['id'])
            elif choice == '2':
                self.view_tasks(user['id'])
            elif choice == '3':
                self.update_task(user['id'])
            elif choice == '4':
                self.delete_task(user['id'])
            elif choice == '5':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 5.")

    def create_task(self, user_id):
        title = input("Enter the task title: ")
        description = input("Enter the task description: ")
        deadline = input("Enter the deadline (YYYY-MM-DD): ")
        category = input("Enter the category: ")
        self.db.add_task(user_id, title, description, deadline, category)
        print("Task created successfully.")

    def view_tasks(self, user_id):
        tasks = self.db.get_tasks(user_id)
        if not tasks:
            print("No tasks found.")
        else:
            for task in tasks:
                print(f"\nID: {task['id']}")
                print(f"Title: {task['title']}")
                print(f"Description: {task['description']}")
                print(f"Deadline: {task['deadline']}")
                print(f"Category: {task['category']}")
                print(f"Completed: {'Yes' if task['completed'] else 'No'}")

    def update_task(self, user_id):
        task_id = input("Enter the task ID to update: ")
        task = self.db.get_task(user_id, task_id)
        if task:
            title = input(f"Enter new title (current: {task['title']}): ") or task['title']
            description = input(f"Enter new description (current: {task['description']}): ") or task['description']
            deadline = input(f"Enter new deadline (current: {task['deadline']}): ") or task['deadline']
            category = input(f"Enter new category (current: {task['category']}): ") or task['category']
            completed = input(f"Is the task completed? (y/n, current: {'y' if task['completed'] else 'n'}): ")
            completed = True if completed.lower() == 'y' else False if completed.lower() == 'n' else task['completed']
            self.db.update_task(task_id, title, description, deadline, category, completed)
            print("Task updated successfully.")
        else:
            print("Task not found.")

    def delete_task(self, user_id):
        task_id = input("Enter the task ID to delete: ")
        if self.db.delete_task(user_id, task_id):
            print("Task deleted successfully.")
        else:
            print("Task not found.")