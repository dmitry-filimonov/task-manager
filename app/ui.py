from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QDateTimeEdit, QMenuBar, QAction, QStatusBar
from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QIcon
from app.database import add_task, get_all_tasks, delete_task
from datetime import datetime
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Task Manager с таймером до дедлайна')
        self.setGeometry(100, 100, 800, 600)  # Размер и положение окна
        self.initUI()
        self.load_tasks()

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        # Меню
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        
        fileMenu = self.menuBar.addMenu('Файл')
        helpMenu = self.menuBar.addMenu('Справка')

        exitAction = QAction(QIcon('icons/delete.png'), 'Выход', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        aboutAction = QAction('О программе', self)
        helpMenu.addAction(aboutAction)
        aboutAction.triggered.connect(self.showAboutDialog)

        # Статусная строка
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        # Ввод для новой задачи
        self.title_input = QLineEdit(self)
        self.description_input = QLineEdit(self)
        self.deadline_input = QDateTimeEdit(self)
        self.deadline_input.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.deadline_input.setDateTime(QDateTime.currentDateTime())

        self.add_task_button = QPushButton(QIcon('icons/add.png'), 'Добавить задачу', self)
        self.add_task_button.clicked.connect(self.add_task)

        self.layout.addWidget(QLabel('Название:'))
        self.layout.addWidget(self.title_input)
        self.layout.addWidget(QLabel('Описание:'))
        self.layout.addWidget(self.description_input)
        self.layout.addWidget(QLabel('Дедлайн:'))
        self.layout.addWidget(self.deadline_input)
        self.layout.addWidget(self.add_task_button)

        # Таблица для отображения задач
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)  # ID, Название, Описание, Дедлайн, Оставшееся время
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Описание', 'Дедлайн', 'Оставшееся время'])
        self.table.setColumnWidth(0, 50)   # ID
        self.table.setColumnWidth(1, 200)  # Название
        self.table.setColumnWidth(2, 300)  # Описание
        self.table.setColumnWidth(3, 200)  # Дедлайн
        self.table.setColumnWidth(4, 150)  # Оставшееся время
        self.layout.addWidget(self.table)

        # Кнопка для удаления задачи
        self.delete_task_button = QPushButton(QIcon('icons/delete.png'), 'Удалить задачу', self)
        self.delete_task_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_task_button)

        # Таймер для обновления дедлайнов
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_deadlines)
        self.timer.start(60000)  # Обновлять каждую минуту

        # Стилизация
        self.setStyleSheet("""
            QMainWindow {
                background-image: url('icons/background.jpeg');
            }
            QLineEdit {
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                font-size: 14px;
                padding: 5px;
            }
            QTableWidget {
                background-color: #ffffff;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
            }
        """)

    def load_tasks(self):
        tasks = get_all_tasks()
        self.table.setRowCount(len(tasks))
        for index, (task_id, title, description, deadline) in enumerate(tasks):
            self.table.setItem(index, 0, QTableWidgetItem(str(task_id)))
            self.table.setItem(index, 1, QTableWidgetItem(title))
            self.table.setItem(index, 2, QTableWidgetItem(description))
            self.table.setItem(index, 3, QTableWidgetItem(deadline))
            self.update_time_left(index, deadline)

    def add_task(self):
        title = self.title_input.text()
        description = self.description_input.text()
        deadline = self.deadline_input.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        try:
            deadline_datetime = datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')
            add_task(title, description, deadline)
            self.load_tasks()  # Обновить список задач после добавления новой
            self.title_input.clear()
            self.description_input.clear()
            self.deadline_input.setDateTime(QDateTime.currentDateTime())
            self.statusBar.showMessage('Задача добавлена', 2000)
        except ValueError:
            QMessageBox.warning(self, "Неверный формат", "Введите дедлайн в формате YYYY-MM-DD HH:MM:SS")

    def delete_task(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            task_id = int(self.table.item(selected_row, 0).text())
            delete_task(task_id)
            self.table.removeRow(selected_row)  # Удалить строку из таблицы
            self.statusBar.showMessage('Задача удалена', 2000)

    def update_deadlines(self):
        current_time = QDateTime.currentDateTime()
        for row in range(self.table.rowCount()):
            deadline = self.table.item(row, 3).text()
            self.update_time_left(row, deadline)

    def update_time_left(self, row, deadline):
        current_time = QDateTime.currentDateTime()
        deadline_datetime = QDateTime.fromString(deadline, 'yyyy-MM-dd HH:mm:ss')
        time_left = current_time.secsTo(deadline_datetime)
        if time_left < 0:
            self.table.setItem(row, 4, QTableWidgetItem("Срок истёк"))
        else:
            hours, remainder = divmod(time_left, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.table.setItem(row, 4, QTableWidgetItem(f"{hours} ч. {minutes} мин."))

    def showAboutDialog(self):
        QMessageBox.about(self, "О программе", "Task Manager с таймером до дедлайна\nРазработано с использованием PyQt5.")

