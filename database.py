import sqlite3
from hashlib import sha256

class Database:
    def __init__(self, db_name="task_manager.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_users_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        self.conn.commit()

    def create_tasks_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                description TEXT,
                deadline TEXT,
                category TEXT,
                completed INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()

    def add_user(self, username, password):
        try:
            hashed_password = sha256(password.encode()).hexdigest()
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        hashed_password = sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = self.cursor.fetchone()
        if user:
            return {"id": user[0], "username": user[1]}
        return None

    def add_task(self, user_id, title, description, deadline, category):
        self.cursor.execute("""
            INSERT INTO tasks (user_id, title, description, deadline, category) 
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, title, description, deadline, category))
        self.conn.commit()

    def get_tasks(self, user_id):
        self.cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
        tasks = self.cursor.fetchall()
        return [{"id": task[0], "title": task[2], "description": task[3], "deadline": task[4], "category": task[5], "completed": bool(task[6])} for task in tasks]

    def get_task(self, user_id, task_id):
        self.cursor.execute("SELECT * FROM tasks WHERE user_id = ? AND id = ?", (user_id, task_id))
        task = self.cursor.fetchone()
        if task:
            return {"id": task[0], "title": task[2], "description": task[3], "deadline": task[4], "category": task[5], "completed": bool(task[6])}
        return None

    def update_task(self, task_id, title, description, deadline, category, completed):
        self.cursor.execute("""
            UPDATE tasks 
            SET title = ?, description = ?, deadline = ?, category = ?, completed = ?
            WHERE id = ?
        """, (title, description, deadline, category, int(completed), task_id))
        self.conn.commit()

    def delete_task(self, user_id, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE user_id = ? AND id = ?", (user_id, task_id))
        self.conn.commit()
        return self.cursor.rowcount > 0
