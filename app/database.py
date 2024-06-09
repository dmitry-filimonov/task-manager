import sqlite3
from datetime import datetime

def connect():
    """Создает соединение с базой данных SQLite."""
    conn = sqlite3.connect('tasks.db')
    return conn

def create_table():
    """Создает таблицу задач, если она еще не существует."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            deadline TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_task(title, description, deadline):
    """Добавляет новую задачу в базу данных."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, deadline) VALUES (?, ?, ?)",
                   (title, description, deadline))
    conn.commit()
    conn.close()

def get_all_tasks():
    """Возвращает все задачи из базы данных."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    """Удаляет задачу по ее ID."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Убедимся, что таблица создана при первом использовании модуля
create_table()
