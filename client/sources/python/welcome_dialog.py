from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox, QApplication
from PySide6.QtGui import QIcon, QFont, QScreen
from PySide6.QtCore import Qt
from sources.python.config import PATHS, WINDOW_STYLES

class WelcomeDialog(QDialog):
    def __init__(self, full_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Приветственное окно")
        self.setMinimumSize(500, 100)
        self.setStyleSheet(WINDOW_STYLES["welcome_dialog"])
        layout = QVBoxLayout()
        welcome_label = QLabel(f"Добро пожаловать, {full_name}!", self)
        welcome_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(welcome_label)
        self.ok_button = QPushButton("Ок")
        self.ok_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.ok_button.setStyleSheet(WINDOW_STYLES["ok_button"])
        self.ok_button.clicked.connect(self.close)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)
        self.center_window()

    def center_window(self):
        screen_geometry = QScreen.availableGeometry(QApplication.primaryScreen())
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())
