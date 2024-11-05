import sys
import json
import requests
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QCheckBox, QLabel, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
import hashlib
from sources.python.config import (
    PATHS,
    WINDOW_STYLES,
    FONTS,
    ENDPOINTS,
    SIZES
)

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setWindowIcon(QIcon(PATHS["icons"]["main"]))
        self.setMinimumSize(SIZES["register_window"]["min_width"],
                            SIZES["register_window"]["min_height"])
        self.setStyleSheet(WINDOW_STYLES["register"])
        self.resize(400, 300)
        layout = QVBoxLayout()
        self.login_input = QLineEdit()
        self.login_input.setFont(QFont(FONTS["default"]["family"], FONTS["default"]["size"]))
        self.login_input.setPlaceholderText("Логин")
        layout.addWidget(self.login_input)
        self.password_input = QLineEdit()
        self.password_input.setFont(QFont(FONTS["default"]["family"], FONTS["default"]["size"]))
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Пароль")
        layout.addWidget(self.password_input)
        self.last_name_input = QLineEdit()
        self.password_input.setFont(QFont(FONTS["default"]["family"], FONTS["default"]["size"]))
        self.last_name_input.setPlaceholderText("Фамилия")
        layout.addWidget(self.last_name_input)
        self.first_name_input = QLineEdit()
        self.password_input.setFont(QFont(FONTS["default"]["family"], FONTS["default"]["size"]))
        self.first_name_input.setPlaceholderText("Имя")
        layout.addWidget(self.first_name_input)
        self.middle_name_input = QLineEdit()
        self.password_input.setFont(QFont(FONTS["default"]["family"], FONTS["default"]["size"]))
        self.middle_name_input.setPlaceholderText("Отчество")
        layout.addWidget(self.middle_name_input)
        self.email_input = QLineEdit()
        self.password_input.setFont(QFont(FONTS["default"]["family"], FONTS["default"]["size"]))
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)
        self.phone_input = QLineEdit()
        self.password_input.setFont(QFont(FONTS["default"]["family"], FONTS["default"]["size"]))
        self.phone_input.setPlaceholderText("Телефон")
        layout.addWidget(self.phone_input)
        self.teacher_checkbox = QCheckBox("Учитель")
        self.password_input.setFont(QFont(FONTS["default"]["family"], FONTS["default"]["size"]))
        self.teacher_checkbox.stateChanged.connect(self.toggle_teacher_field)
        layout.addWidget(self.teacher_checkbox)
        self.subject_input = QLineEdit()
        self.password_input.setFont(QFont(FONTS["default"]["family"], FONTS["default"]["size"]))
        self.subject_input.setPlaceholderText("Дисциплины")
        self.subject_input.setVisible(False)
        layout.addWidget(self.subject_input)
        self.submit_button = QPushButton("Отправить")
        self.submit_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.submit_button.setStyleSheet(WINDOW_STYLES["login_button"])
        self.submit_button.clicked.connect(self.show_confirmation)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def toggle_teacher_field(self, state):
        self.subject_input.setVisible(state == 2)

    def show_confirmation(self):
        confirmation_dialog = QMessageBox()
        confirmation_dialog.setWindowTitle("Подтверждение")
        confirmation_dialog.setWindowIcon(QIcon(PATHS["icons"]["main"]))
        confirmation_dialog.setText("Вы уверены, что хотите отправить данные?")
        confirmation_dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirmation_dialog.setDefaultButton(QMessageBox.StandardButton.No)
        confirmation_dialog.buttonClicked.connect(self.confirmation_response)
        confirmation_dialog.exec()

    def confirmation_response(self, button):
        if button.text() == "&Yes":
            self.handle_submit()

    def handle_submit(self):
        full_name = f"{self.first_name_input.text()} {self.last_name_input.text()} {self.middle_name_input.text()}"
        teacher = 1 if self.teacher_checkbox.isChecked() else 0
        # Проверка на пустые значения
        if not self.login_input.text() or not self.password_input.text() or not self.last_name_input.text() or not self.first_name_input.text() or not self.middle_name_input.text():
            self.show_error_message("Логин, пароль, фамилия, имя и отчество не могут быть пустыми")
            return
        data = {
            "command": "register",
            "login": self.login_input.text(),
            "password": self.hash_data(self.password_input.text()),
            "full_name": full_name,
            "email": self.email_input.text(),
            "phone": self.phone_input.text(),
            "disciplines": self.subject_input.text() if self.teacher_checkbox.isChecked() else "",
            "permissions": teacher
        }
        print("Отправляемые данные:", data)  # Отладочное сообщение
        try:
            response = requests.post(ENDPOINTS["register"], json=data)
            print("Статус ответа:", response.status_code)  # Отладочное сообщение
            print("Ответ:", response.text)  # Отладочное сообщение
            response_data = response.json()
            if response_data.get("status") == "success":
                self.show_success_message()
            elif response_data.get("status") == "error code 401":
                self.show_error_message("Вы отправили слишком много запросов. Подождите некоторое время")
            elif response_data.get("status") == "error code 402":
                self.show_error_message("Логин должен быть написан на латинице")
            elif response_data.get("status") == "error code 403":
                self.show_error_message("ФИО должны быть написаны на кириллице")
            else:
                self.show_error_message("Непредвиденная ошибка (возможно такой логин уже существует)")
        except requests.exceptions.RequestException as e:
            print("Ошибка запроса:", e)  # Отладочное сообщение
            self.show_error_message("Непредвиденная ошибка (возможно такой логин уже существует)")

    def hash_data(self, data):
        hash_object = hashlib.sha256(data.encode())
        return hash_object.hexdigest()
    
    def show_success_message(self):
        success_dialog = QMessageBox()
        success_dialog.setWindowTitle("Успех")
        success_dialog.setWindowIcon(QIcon(PATHS["icons"]["main"]))
        success_dialog.setText("Регистрация успешна! Ожидайте пока её проверят сотрудники ВУЗА")
        success_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        success_dialog.buttonClicked.connect(self.close)
        success_dialog.exec()

    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setWindowTitle("Ошибка")
        error_dialog.setWindowIcon(QIcon(PATHS["icons"]["main"]))
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_dialog.exec()
