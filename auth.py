import getpass
from database import Database

class Auth:
    def __init__(self):
        self.db = Database()
        self.db.create_users_table()

    def register(self):
        username = input("Enter a username: ")
        password = getpass.getpass("Enter a password: ")
        if self.db.add_user(username, password):
            print("Registration successful.")
        else:
            print("Username already exists.")

    def login(self):
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")
        user = self.db.authenticate_user(username, password)
        if user:
            print("Login successful.")
            return user
        else:
            print("Invalid username or password.")
            return None