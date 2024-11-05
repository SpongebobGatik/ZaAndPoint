from PySide6.QtWidgets import (
    QMainWindow, 
    QTableWidget, 
    QTableWidgetItem, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
    QFrame, 
    QHeaderView, 
    QFileDialog,
    QSpacerItem,
    QSizePolicy,
    QWidget,
    QLabel
)
from PySide6.QtGui import QIcon, QPixmap, QPalette, QBrush
from PySide6.QtCore import Qt, QSize
import pandas as pd
import requests
from sources.python.config import PATHS, WINDOW_STYLES, ENDPOINTS, TABLES
from sources.python.dialogs import AddDialog, AddTempDialog, DeleteDialog, UpdateDialog, SelectSemesterDialog, SelectGroupDialog

class TableWindow(QMainWindow):

    """Окно таблицы."""

    def __init__(
        self,
        title,
        data,
        columns,
        background_image,
        refresh_button,
        table_type,
        parent_app,
        semesters=None,
        directions_groups=None,
        main_window=None,
    ):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(PATHS["icons"]["main"]))
        self.setGeometry(100, 100, 800, 600)
        self.parent_app = parent_app
        self.columns = columns
        self.data = data
        self.table_type = table_type
        self.semesters = semesters
        self.directions_groups = directions_groups
        self.main_window = main_window
        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap(background_image)
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)
        self.table = QTableWidget()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        for row, item in enumerate(data):
            for col, key in enumerate(columns):
                cell = QTableWidgetItem(str(item.get(key, "")))
                cell.setFlags(cell.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, cell)
        self.table.setStyleSheet(WINDOW_STYLES["table"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        side_panel = self.create_side_panel(refresh_button)
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.table)
        main_layout.addLayout(side_panel)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_side_panel(self, refresh_button):

        """Создает боковую панель с кнопками."""

        side_panel = QVBoxLayout()
        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setStyleSheet(WINDOW_STYLES["side_panel"])
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(refresh_button)
        if self.table_type == "grades":
            select_button = QPushButton()
            select_button.setIcon(QIcon(PATHS["icons"]["select_semester"]))
            select_button.setIconSize(QSize(80, 80))
            select_button.clicked.connect(self.open_select_semester_dialog)
            layout.addWidget(select_button)
        elif self.table_type == "students":
            select_button = QPushButton()
            select_button.setIcon(QIcon(PATHS["icons"]["select_group"]))
            select_button.setIconSize(QSize(80, 80))
            select_button.clicked.connect(self.open_select_group_dialog)
            layout.addWidget(select_button)
        if self.table_type in [
            "attestation",
            "tdis",
            "user",
            "direction",
            "dirt",
            "discipline",
            "disdir",
            "student",
            "studentgroup",
            "grouplink",
        ]:
            add_button = QPushButton()
            add_button.setIcon(QIcon(PATHS["icons"]["add"]))
            add_button.setIconSize(QSize(80, 80))
            add_button.clicked.connect(self.open_add_dialog)
            layout.addWidget(add_button)
            delete_button = QPushButton()
            delete_button.setIcon(QIcon(PATHS["icons"]["delete"]))
            delete_button.setIconSize(QSize(80, 80))
            delete_button.clicked.connect(self.open_delete_dialog)
            layout.addWidget(delete_button)
            update_button = QPushButton()
            update_button.setIcon(QIcon(PATHS["icons"]["change"]))
            update_button.setIconSize(QSize(80, 80))
            update_button.clicked.connect(self.open_update_dialog)
            layout.addWidget(update_button)
        elif self.table_type == "addtemp":  # Кнопка для addtemp
            addtemp_button = QPushButton()
            addtemp_button.setIcon(QIcon(PATHS["icons"]["add_temp"]))
            addtemp_button.setIconSize(QSize(80, 80))
            addtemp_button.clicked.connect(self.open_addtemp_dialog)
            layout.addWidget(addtemp_button)
            delete_button = QPushButton()
            delete_button.setIcon(QIcon(PATHS["icons"]["delete"]))
            delete_button.setIconSize(QSize(80, 80))
            delete_button.clicked.connect(self.open_delete_dialog)
            layout.addWidget(delete_button)
            update_button = QPushButton()
            update_button.setIcon(QIcon(PATHS["icons"]["change"]))
            update_button.setIconSize(QSize(80, 80))
            update_button.clicked.connect(self.open_update_dialog)
            layout.addWidget(update_button)
        save_button = QPushButton()
        save_button.setIcon(QIcon(PATHS["icons"]["save"]))
        save_button.setIconSize(QSize(185, 185))
        save_button.clicked.connect(self.save_to_excel)
        layout.addWidget(save_button)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
        frame.setLayout(layout)
        side_panel.addWidget(frame)
        return side_panel

    def save_to_excel(self):

        """Сохраняет данные таблицы в Excel файл."""

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить в Excel",
            "",
            "Excel Files (*.xlsx);;All Files (*)",
            options=options,
        )
        if file_path:
            data = [
                [self.table.item(row, col).text() for col in range(self.table.columnCount())]
                for row in range(self.table.rowCount())
            ]
            df = pd.DataFrame(
                data,
                columns=[
                    self.table.horizontalHeaderItem(i).text()
                    for i in range(self.table.columnCount())
                ],
            )
            df.to_excel(file_path, index=False)

    def update_table(self):

        """Обновляет данные в таблице."""

        self.table.setRowCount(len(self.data))
        for row, item in enumerate(self.data):
            for col, key in enumerate(self.columns):
                if key == "student_name" and self.table_type == "grades":
                    student_name = self.get_student_name_by_id(item.get("student_id"))
                    cell = QTableWidgetItem(student_name)
                else:
                    cell = QTableWidgetItem(str(item.get(key, "")))
                cell.setFlags(cell.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, cell)

    def get_student_name_by_id(self, student_id):

        """Возвращает имя студента по его ID."""

        for member in self.parent_app.data.get("data", {}).get("group_members", []):
            if member.get("student_id") == student_id:
                return member.get("student_name")
        return ""

    def open_select_semester_dialog(self):

        """Открывает диалоговое окно выбора семестра."""

        dialog = SelectSemesterDialog(self.semesters, self)
        if dialog.exec():
            selected_semester = dialog.selected_semester
            self.parent_app.load_semester_grades(selected_semester)

    def open_select_group_dialog(self):

        """Открывает диалоговое окно выбора группы."""

        dialog = SelectGroupDialog(self.directions_groups, self)
        if dialog.exec():
            selected_direction, selected_group = dialog.selected_direction, dialog.selected_group
            self.parent_app.load_group_students(selected_direction, selected_group)

    def closeEvent(self, event):

        """Обработчик события закрытия окна."""

        self.parent_app.close()
        event.accept()

    def open_add_dialog(self):
        dialog = AddDialog(self.columns, self.table_type, self.parent_app.data, self, self.parent_app)
        if dialog.exec():
            new_row = dialog.get_data()
            self.data.append(new_row)
            self.update_table()
            self.send_to_server(new_row, self.get_insert_command())
            self.main_window.restart_no_press()

    def open_addtemp_dialog(self):

        """Открывает диалоговое окно добавления временного пользователя."""

        dialog = AddTempDialog(self.data, self)
        if dialog.exec():
            row_index = dialog.get_row_index()
            if row_index is not None:
                add_row = self.data.pop(row_index)
                self.update_table()
                self.send_to_server(add_row, "insert_temp")
                self.main_window.restart_no_press()

    def open_delete_dialog(self):

        """Открывает диалоговое окно удаления строки."""

        dialog = DeleteDialog(self.data, self)
        if dialog.exec():
            row_index = dialog.get_row_index()
            if row_index is not None:
                deleted_row = self.data.pop(row_index)
                self.update_table()
                self.send_to_server(deleted_row, self.get_delete_command())
                self.main_window.restart_no_press()

    def open_update_dialog(self):

        """Открывает диалоговое окно изменения строки."""

        dialog = UpdateDialog(self.columns, self.table_type, self.parent_app.data, self, self.parent_app)
        if dialog.exec():
            row_index, updated_row = dialog.get_data()
            if row_index is not None:
                self.data[row_index] = updated_row
                self.update_table()
                self.send_to_server(updated_row, self.get_update_command())
                self.main_window.restart_no_press()

    def update_table_data(self, data):

        """Обновляет данные таблицы и обновляет ее отображение."""

        self.data = data
        self.update_table()

    def send_to_server(self, row_data, command):

        """Отправляет данные на сервер."""

        data = {
            "username": self.main_window.username,
            "password": self.main_window.password,
            "command": command,
            "data": row_data,
        }
        response = requests.post(ENDPOINTS["add"], json=data)
        print(response.content)
        print(data)

    def get_insert_command(self):

        """Возвращает команду для вставки строки в зависимости от типа таблицы."""

        command_mapping = {
            "attestation": "insert_at",
            "direction": "insert_dir",
            "dirt": "insert_dirt",
            "discipline": "insert_dis",
            "disdir": "insert_disdir",
            "student": "insert_student",
            "studentgroup": "insert_st",
            "grouplink": "insert_gr",
            "tdis": "insert_tdis",
            "user": "insert_user",
        }
        return command_mapping.get(self.table_type)

    def get_delete_command(self):

        """Возвращает команду для удаления строки в зависимости от типа таблицы."""

        command_mapping = {
            "attestation": "delete_at",
            "addtemp": "delete_temp",
            "direction": "delete_dir",
            "dirt": "delete_dirt",
            "discipline": "delete_dis",
            "disdir": "delete_disdir",
            "student": "delete_student",
            "studentgroup": "delete_st",
            "grouplink": "delete_gr",
            "tdis": "delete_tdis",
            "user": "delete_user",
        }
        return command_mapping.get(self.table_type)

    def get_update_command(self):

        """Возвращает команду для обновления строки в зависимости от типа таблицы."""

        command_mapping = {
            "attestation": "update_at",
            "addtemp": "update_temp",
            "direction": "update_dir",
            "dirt": "update_dirt",
            "discipline": "update_dis",
            "disdir": "update_disdir",
            "student": "update_student",
            "studentgroup": "update_st",
            "grouplink": "update_gr",
            "tdis": "update_tdis",
            "user": "update_user",
        }
        return command_mapping.get(self.table_type)
