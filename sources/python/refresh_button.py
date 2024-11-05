from PySide6.QtWidgets import QPushButton, QMessageBox
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt, QSize, QMargins
from sources.python.base_window import BaseWindow
from sources.python.config import PATHS, WINDOW_STYLES

class RefreshButton(QPushButton):
    def __init__(self, username, password, send_request, main_window, parent=None):
        super().__init__(parent)
        self.username = username
        self.password = password
        self.send_request = send_request
        self.main_window = main_window
        self.setFont(QFont("Arial", 14, QFont.Bold))
        self.setStyleSheet(WINDOW_STYLES ["refresh_button"])
        self.setIcon(QIcon(PATHS["icons"]["refresh"]))
        self.setIconSize(QSize(80, 80))
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.clicked.connect(self.refresh_data)

    def refresh_data(self):
        data = {
            "username": self.username,
            "password": self.password
        }
        self.send_request(data, self.show_refresh_success)

    def show_refresh_success(self, *args):
        self.main_window.update_ui()
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Успех")
        msg_box.setWindowIcon(QIcon(PATHS["icons"]["main"]))
        msg_box.setText("База данных была обновлена")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStyleSheet(WINDOW_STYLES ["refresh_success"])
        msg_box.exec()
