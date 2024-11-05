import hashlib
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QApplication,
)
from PySide6.QtGui import QIcon, QFont, QScreen
from PySide6.QtCore import Qt
from sources.python.config import (
    ENDPOINTS,
    PATHS,
    WINDOW_STYLES,
    FONTS,
    SIZES,
    TABLES
)
from sources.python.base_window import BaseWindow
from sources.python.register import RegisterWindow

class ClearableLineEdit(QLineEdit):
    def focusInEvent(self, event):
        self.clear()
        super().focusInEvent(event)

class LoginWindow(QWidget, BaseWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setWindowIcon(QIcon(PATHS["icons"]["main"]))
        self.setMinimumSize(SIZES["login_window"]["min_width"],
                            SIZES["login_window"]["min_height"])
        self.setStyleSheet(WINDOW_STYLES["login"])
        self.resize(SIZES["login_window"]["min_width"],
                            SIZES["login_window"]["min_height"])
        layout = QVBoxLayout()
        self.username_input = ClearableLineEdit()
        self.username_input.setFont(QFont(FONTS["default"]["family"], FONTS["default"]["size"]))
        self.username_input.setPlaceholderText("Имя пользователя")
        layout.addWidget(self.username_input)
        self.password_input = ClearableLineEdit()
        self.password_input.setFont(QFont(FONTS["default"]["family"], FONTS["default"]["size"]))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Пароль")
        layout.addWidget(self.password_input)
        self.login_button = QPushButton("Войти")
        self.login_button.setFont(QFont(FONTS["default"]["family"], FONTS["default"]["size"], QFont.Bold))
        self.login_button.setStyleSheet(WINDOW_STYLES["login_button"])
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        layout.addSpacing(5)
        self.rec_window = RegisterWindow()
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.setFont(QFont(FONTS["default"]["family"], FONTS["default"]["size"]))
        self.register_button.setStyleSheet(WINDOW_STYLES["register_button"])
        self.register_button.clicked.connect(self.show_reg_window)
        layout.addWidget(self.register_button, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)
        self.center_window()

    def center_window(self):
        screen_geometry = QScreen.availableGeometry(QApplication.primaryScreen())
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())

    def handle_login(self):
        username = self.username_input.text()
        password = self.hash_data(self.password_input.text())
        data = {
            "username": username,
            "password": password
        }
        self.send_request(data, self.open_main_window)

    def open_main_window(self, username, password):
        from sources.python.main_window import MainWindow
        self.main_window = MainWindow(username, password)
        self.main_window.showMaximized()
        self.close()

    def hash_data(self, data):
        hash_object = hashlib.sha256(data.encode())
        return hash_object.hexdigest()

    def show_reg_window(self):
        if self.rec_window is not None:
            self.rec_window.close()
        self.rec_window = RegisterWindow()
        self.rec_window.show()
