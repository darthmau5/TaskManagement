from auth import Auth
from tasks import TaskManager

def main():
    auth = Auth()
    task_manager = TaskManager()

    while True:
        print("\nWelcome to the Task Management System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")

        if choice == '1':
            auth.register()
        elif choice == '2':
            user = auth.login()
            if user:
                task_manager.run(user)
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 3.")

if __name__ == "__main__":
    main()