import sys
import json
import os
import requests
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDialog
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from sources.python.config import (
    ENDPOINTS,
    PATHS,
    WINDOW_STYLES,
    FONTS,
    SIZES,
    TABLES
)

class UpdateDialog(QDialog):
    def __init__(self, refresh_button_instance, name, phone, email, username, password, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Изменение личных данных")
        self.setWindowIcon(QIcon(PATHS["icons"]["main"]))
        self.setMinimumSize(300, 200)
        self.refresh_button_instance = refresh_button_instance
        self.name = name
        self.phone = phone
        self.email = email
        self.username = username
        self.password = password
        layout = QVBoxLayout()
        self.phone_input = QLineEdit(self.phone)
        self.phone_input.setPlaceholderText("Телефон")
        self.phone_input.setFont(QFont("Arial", 14))
        layout.addWidget(self.phone_input)
        self.email_input = QLineEdit(self.email)
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFont(QFont("Arial", 14))
        layout.addWidget(self.email_input)
        self.update_button = QPushButton("Обновить данные")
        self.update_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.update_button.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 5px;")
        self.update_button.clicked.connect(self.confirm_update)
        layout.addWidget(self.update_button)
        self.setLayout(layout)

    def confirm_update(self):
        confirm_msg = QMessageBox.question(self, "Подтверждение", "Вы уверены?",
                                           QMessageBox.Yes | QMessageBox.No)
        if confirm_msg == QMessageBox.Yes:
            self.update_info(self.phone_input.text(), self.email_input.text())

    def update_info(self, phone, email):
        data = {
            "name": self.name,
            "phone": phone,
            "email": email,
            "username": self.username,
            "password": self.password
        }
        print(data)
        try:
            response = requests.post("http://localhost/assessment/update_con.php", json=data)
            print(response.content)
            if response.status_code == 200:
                if response.content:
                    response_data = response.json()
                    if response_data['status'] == 'success':
                        QMessageBox.information(self, "Успех", response_data['message'])
                        self.refresh_button_instance.restart_no_press(1)
                        self.accept()
                    else:
                        QMessageBox.warning(self, "Ошибка", response_data['message'])
                else:
                    QMessageBox.warning(self, "Ошибка", "Empty response from server")
            else:
                QMessageBox.warning(self, "Ошибка", "Failed to update information")
        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Ошибка", f"An error occurred: {e}")

class ConnWindow(QMainWindow):
    def __init__(self, refresh_button_instance, name, phone, email, username, password):
        super().__init__()
        self.setWindowTitle("Личные данные")
        self.setWindowIcon(QIcon("sources/img/icon.png"))
        self.setMinimumSize(600, 300)
        self.resize(600, 300)
        self.refresh_button_instance = refresh_button_instance
        self.name = name
        self.phone = phone
        self.email = email
        self.username = username
        self.password = password
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        self.name_label = QLabel(f"ФИО: {self.name}")
        self.name_label.setFont(QFont("Comic Sans MS", 18, QFont.Bold))
        layout.addWidget(self.name_label)
        self.phone_label = QLabel(f"Телефон: {self.phone}")
        self.phone_label.setFont(QFont("Comic Sans MS", 18, QFont.Bold))
        layout.addWidget(self.phone_label)
        self.email_label = QLabel(f"Email: {self.email}")
        self.email_label.setFont(QFont("Comic Sans MS", 18, QFont.Bold))
        layout.addWidget(self.email_label)
        self.update_button = QPushButton("Изменить данные")
        self.update_button.setFont(QFont("Comic Sans MS", 16, QFont.Bold))
        self.update_button.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 5px;")
        self.update_button.clicked.connect(lambda: self.open_update_dialog(self.refresh_button_instance, self.name, self.phone, self.email, self.username, self.password))
        layout.addWidget(self.update_button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setStyleSheet("background-color: #FFFACD;")

    def open_update_dialog(self, refresh_button_instance, name, phone, email, username, password):
        dialog = UpdateDialog(refresh_button_instance, name, phone, email, username, password, self)
        dialog.exec()
