from PySide6.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QComboBox,
    QMessageBox,
    QApplication
)
from PySide6.QtGui import (
    QIntValidator,
    QIcon,
    QScreen
)
from PySide6.QtCore import Qt
import hashlib
from sources.python.config import WINDOW_STYLES, TABLES, PATHS

class BaseDialog(QDialog):

    """Базовый класс для диалоговых окон."""
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(PATHS["icons"]["main"]))
        self.setStyleSheet(WINDOW_STYLES["dialog"])
        
    def create_input_field(
        self,
        label_text,
        data_key=None,
        is_readonly=False,
        is_password=False,
        validator=None,
        items=None,
    ):
        
        """Фабричный метод для создания полей ввода."""
        
        layout = QVBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)
        if items is not None:
            input_field = QComboBox()
            if isinstance(items[0], dict):
                for item in items:
                    input_field.addItem(item["name"], item["id"])
            else:
                for item in items:
                    input_field.addItem(str(item), item)  # Добавляем данные для каждого элемента
        else:
            input_field = QLineEdit()
            if is_readonly:
                input_field.setReadOnly(True)
            if is_password:
                input_field.setEchoMode(QLineEdit.Password)
            if validator:
                input_field.setValidator(validator)
        layout.addWidget(input_field)
        self.inputs[data_key or label_text] = input_field
        return layout
    
    def center_window(self):
        screen_geometry = QScreen.availableGeometry(QApplication.primaryScreen())
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.setGeometry(x, y, self.width(), self.height())

class AddDialog(BaseDialog):

    """Диалоговое окно для добавления строки."""

    def __init__(self, columns, table_type, data_source, parent=None, parent_app=None):  # Добавили parent_app
        super().__init__("Добавить строку", parent)
        self.setStyleSheet(WINDOW_STYLES["add"])  # Восстановление стиля
        self.columns = columns
        self.table_type = table_type
        self.data_source = data_source
        self.inputs = {}
        self.parent_app = parent_app    
        layout = QVBoxLayout()
        table_mapping = {
            "attestation": self.create_attestation_fields,
            "direction": self.create_default_fields,
            "dirt": self.create_dirt_fields,
            "discipline": self.create_default_fields,
            "disdir": self.create_disdir_fields,
            "student": self.create_default_fields,
            "studentgroup": self.create_studentgroup_fields,
            "grouplink": self.create_grouplink_fields,
            "tdis": self.create_tdis_fields,
            "user": self.create_user_fields,
        }
        create_fields_func = table_mapping.get(self.table_type, self.create_default_fields)
        layout.addLayout(create_fields_func())
        add_button = QPushButton("Добавить строку")
        add_button.clicked.connect(self.accept)
        layout.addWidget(add_button)
        self.setLayout(layout)

    def create_default_fields(self):

        """Создает поля ввода для таблиц без специфичных полей."""

        layout = QVBoxLayout()
        for col in self.columns:
            if col.endswith("_id"):
                continue
            layout.addLayout(self.create_input_field(col))
        return layout

    def create_attestation_fields(self):

        """Создает поля ввода для таблицы 'attestation'."""
        
        layout = QVBoxLayout()
        exclude_fields = ["grade_id", "student_id", "teacher_id", "grade_5", "grade_date"]
        for col in self.columns:
            if col in exclude_fields:
                 continue
            if col == "semester":
                layout.addLayout(self.create_input_field(col, items=[str(i) for i in range(1, 12)]))
            elif col == "discipline_name":
                layout.addLayout(self.create_input_field(col, items=[item["discipline_name"] for item in self.data_source.get("data", {}).get("disciplines", [])]))
            elif col == "student_name":
                # Используем 'student_id' как ключ, 'student_name' для отображения
                layout.addLayout(self.create_input_field(col, data_key="student_id", items=[{"id": item["student_id"], "name": item["student_name"]} for item in self.data_source.get("data", {}).get("group_members", [])]))
            elif col == "exam_type":
                layout.addLayout(self.create_input_field(col, items=["зачёт", "экзамен"]))
            elif col == "teacher_name":
                layout.addLayout(self.create_input_field(col, is_readonly=True))
                self.inputs[col].setText(self.data_source.get("data", {}).get("teacher_info", [{}])[0].get("full_name", ""))
            elif col == "grade_100":
                input_layout = self.create_input_field(col, validator=QIntValidator(0, 100))
                input_field = input_layout.itemAt(1).widget()
                input_field.textChanged.connect(self.validate_grade_100)
                layout.addLayout(input_layout)
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def create_dirt_fields(self):

        """Создает поля ввода для таблицы 'dirt'."""

        layout = QVBoxLayout()
        for col in self.columns:
            if col == "direction_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["direction_id"], "name": item["direction_name"]} for item in self.data_source.get("data", {}).get("directions", [])]))
            elif col == "teacher_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["teacher_id"], "name": item["full_name"]} for item in self.data_source.get("data", {}).get("all_teachers", [])]))
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def create_disdir_fields(self):

        """Создает поля ввода для таблицы 'disdir'."""

        layout = QVBoxLayout()
        for col in self.columns:
            if col == "discipline_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["discipline_id"], "name": item["discipline_name"]} for item in self.data_source.get("data", {}).get("disciplines", [])]))
            elif col == "direction_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["direction_id"], "name": item["direction_name"]} for item in self.data_source.get("data", {}).get("directions", [])]))
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def create_studentgroup_fields(self):

        """Создает поля ввода для таблицы 'studentgroup'."""

        layout = QVBoxLayout()
        for col in self.columns:
            if col == "direction_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["direction_id"], "name": item["direction_name"]} for item in self.data_source.get("data", {}).get("directions", [])]))
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def create_grouplink_fields(self):

        """Создает поля ввода для таблицы 'grouplink'."""

        layout = QVBoxLayout()
        for col in self.columns:
            if col == "group_id":
               layout.addLayout(self.create_input_field(col, items=[{"id": item["group_id"], "name": item["group_name"]} for item in self.data_source.get("data", {}).get("student_groups", [])]))
            elif col == "student_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["student_id"], "name": item["full_name"]} for item in self.data_source.get("data", {}).get("students", [])]))
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def create_tdis_fields(self):

        """Создает поля ввода для таблицы 'tdis'."""

        layout = QVBoxLayout()
        for col in self.columns:
            if col == "teacher_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["teacher_id"], "name": item["full_name"]} for item in self.data_source.get("data", {}).get("all_teachers", [])]))
            elif col == "discipline_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["discipline_id"], "name": item["discipline_name"]} for item in self.data_source.get("data", {}).get("disciplines", [])]))
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def create_user_fields(self):

        """Создает поля ввода для таблицы 'user'."""

        layout = QVBoxLayout()
        for col in self.columns:
            if col == "permissions":
                layout.addLayout(self.create_input_field(col, items=[str(i) for i in range(0, 3)]))
            elif col == "password":
                layout.addLayout(self.create_input_field(col, is_password=True))
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def get_data(self):

        """Возвращает данные из полей ввода."""

        data = {}
        for key, input_field in self.inputs.items():
            if isinstance(input_field, QComboBox):
                data[key] = input_field.currentData()
            else:
                data[key] = input_field.text()
        # Изменение для корректной отправки данных оценки на сервер
        if self.table_type == "attestation":
            data["grade_id"] = None
            data["grade_100"] = int(data["grade_100"]) if data["grade_100"] else None
            data["student_id"] = data.get("student_id")
            data["grade_5"] = None
            data["grade_date"] = None
            data["teacher_id"] = self.parent_app.data.get("data", {}).get("teacher_info", [{}])[0].get("teacher_id", None)
            for discipline in self.parent_app.data.get("data", {}).get("disciplines", []):
                if discipline["discipline_name"] == data["discipline_name"]:
                    data["discipline_id"] = discipline["discipline_id"]
                    break
        if self.table_type == "studentgroup":
            data["group_id"] = None
        if self.table_type == "user" and "password" in data:
            data["password_hash"] = self.hash_data(data["password"])
            del data["password"]
        return data

    def hash_data(self, data):

        """Хеширует данные с помощью SHA256."""

        hash_object = hashlib.sha256(data.encode())
        return hash_object.hexdigest()

    def validate_grade_100(self):

        """Валидирует значение в поле grade_100."""

        grade = self.inputs["grade_100"].text()
        if grade:
            try:
                grade = int(grade)
                if grade > 100:
                    self.inputs["grade_100"].setText("100")
            except ValueError:
                pass

class AddTempDialog(BaseDialog):

    """Диалоговое окно для добавления временного пользователя."""

    def __init__(self, data, parent=None):
        super().__init__("Добавить пользователя", parent)  # Изменение названия
        self.setStyleSheet(WINDOW_STYLES["add_temp"])  # Восстановление стиля
        self.data = data
        self.row_index = None
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Введите индекс строки для добавления:"))
        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)
        add_button = QPushButton("Добавить пользователя")  # Изменение названия
        add_button.clicked.connect(self.accept)
        layout.addWidget(add_button)
        self.setLayout(layout)

    def get_row_index(self):

        """Возвращает индекс строки для добавления."""

        try:
            self.row_index = int(self.input_field.text()) - 1
            if 0 <= self.row_index < len(self.data):
                return self.row_index
        except ValueError:
            pass
        return None

class DeleteDialog(BaseDialog):

    """Диалоговое окно для удаления строки."""

    def __init__(self, data, parent=None):
        super().__init__("Удалить строку", parent)
        self.setStyleSheet(WINDOW_STYLES["delete"])  # Восстановление стиля
        self.data = data
        self.row_index = None
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Введите индекс строки для удаления:"))
        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)
        delete_button = QPushButton("Удалить строку")
        delete_button.clicked.connect(self.accept)
        layout.addWidget(delete_button)
        self.setLayout(layout)

    def get_row_index(self):

        """Возвращает индекс строки для удаления."""

        try:
            self.row_index = int(self.input_field.text()) - 1
            if 0 <= self.row_index < len(self.data):
                return self.row_index
        except ValueError:
            pass
        return None

class UpdateDialog(BaseDialog):

    """Диалоговое окно для изменения строки."""

    def __init__(self, columns, table_type, data_source, parent=None, parent_app=None): 
        super().__init__("Изменить строку", parent)
        self.setStyleSheet(WINDOW_STYLES["update"])
        self.columns = columns
        self.table_type = table_type
        self.data_source = data_source
        self.row_index = None
        self.inputs = {}
        self.parent_app = parent_app
        self.data = self.data_source.get("data", {}).get(TABLES[table_type].get("data_key", table_type), [])  # Добавили self.data
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Введите индекс строки для изменения:"))
        self.input_field = QLineEdit()
        self.input_field.textChanged.connect(self.fill_inputs)
        layout.addWidget(self.input_field)
        table_mapping = {
            "attestation": self.create_attestation_fields,
            "direction": self.create_default_fields,
            "dirt": self.create_dirt_fields,
            "discipline": self.create_default_fields,
            "disdir": self.create_disdir_fields,
            "student": self.create_default_fields,
            "studentgroup": self.create_studentgroup_fields,
            "grouplink": self.create_grouplink_fields,
            "tdis": self.create_tdis_fields,
            "user": self.create_user_fields,
            "addtemp": self.create_addtemp_fields
        }
        create_fields_func = table_mapping.get(self.table_type, self.create_default_fields)
        layout.addLayout(create_fields_func())
        update_button = QPushButton("Изменить строку")
        update_button.clicked.connect(self.accept)
        layout.addWidget(update_button)
        self.setLayout(layout)

    def create_default_fields(self):

        """Создает поля ввода для таблиц без специфичных полей."""

        layout = QVBoxLayout()
        for col in self.columns:
            if col.endswith("_id"):
                continue
            layout.addLayout(self.create_input_field(col))
        return layout
    
    def create_attestation_fields(self):

        """Создает поля ввода для таблицы 'attestation'."""

        layout = QVBoxLayout()
        exclude_fields = ["grade_id", "student_id", "teacher_id", "grade_5", "grade_date"]
        for col in self.columns:
            if col in exclude_fields:
                 continue
            if col == "semester":
                layout.addLayout(self.create_input_field(col, items=[str(i) for i in range(1, 12)]))
            elif col == "discipline_name":
                layout.addLayout(self.create_input_field(col, items=[item["discipline_name"] for item in self.data_source.get("data", {}).get("disciplines", [])]))
            elif col == "student_name":
                # Используем 'student_id' как ключ, 'student_name' для отображения
                layout.addLayout(self.create_input_field(col, data_key="student_id", items=[{"id": item["student_id"], "name": item["student_name"]} for item in self.data_source.get("data", {}).get("group_members", [])]))
            elif col == "exam_type":
                layout.addLayout(self.create_input_field(col, items=["зачёт", "экзамен"]))
            elif col == "teacher_name":
                layout.addLayout(self.create_input_field(col, is_readonly=True))
                self.inputs[col].setText(self.data_source.get("data", {}).get("teacher_info", [{}])[0].get("full_name", ""))
            elif col == "grade_100":
                input_layout = self.create_input_field(col, validator=QIntValidator(0, 100))
                input_field = input_layout.itemAt(1).widget()
                input_field.textChanged.connect(self.validate_grade_100)
                layout.addLayout(input_layout)
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def create_dirt_fields(self):

        """Создает поля ввода для таблицы 'dirt'."""

        layout = QVBoxLayout()
        for col in self.columns:
            if col == "direction_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["direction_id"], "name": item["direction_name"]} for item in self.data_source.get("data", {}).get("directions", [])]))
            elif col == "teacher_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["teacher_id"], "name": item["full_name"]} for item in self.data_source.get("data", {}).get("all_teachers", [])]))
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def create_disdir_fields(self):

        """Создает поля ввода для таблицы 'disdir'."""

        layout = QVBoxLayout()
        for col in self.columns:
            if col == "discipline_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["discipline_id"], "name": item["discipline_name"]} for item in self.data_source.get("data", {}).get("disciplines", [])]))
            elif col == "direction_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["direction_id"], "name": item["direction_name"]} for item in self.data_source.get("data", {}).get("directions", [])]))
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def create_studentgroup_fields(self):

        """Создает поля ввода для таблицы 'studentgroup'."""

        layout = QVBoxLayout()
        for col in self.columns:
            if col == "direction_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["direction_id"], "name": item["direction_name"]} for item in self.data_source.get("data", {}).get("directions", [])]))
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def create_grouplink_fields(self):

        """Создает поля ввода для таблицы 'grouplink'."""

        layout = QVBoxLayout()
        for col in self.columns:
            if col == "group_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["group_id"], "name": item["group_name"]} for item in self.data_source.get("data", {}).get("student_groups", [])]))
            elif col == "student_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["student_id"], "name": item["full_name"]} for item in self.data_source.get("data", {}).get("students", [])]))
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def create_tdis_fields(self):

        """Создает поля ввода для таблицы 'tdis'."""

        layout = QVBoxLayout()
        for col in self.columns:
            if col == "teacher_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["teacher_id"], "name": item["full_name"]} for item in self.data_source.get("data", {}).get("all_teachers", [])]))
            elif col == "discipline_id":
                layout.addLayout(self.create_input_field(col, items=[{"id": item["discipline_id"], "name": item["discipline_name"]} for item in self.data_source.get("data", {}).get("disciplines", [])]))
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def create_user_fields(self):

        """Создает поля ввода для таблицы 'user'."""

        layout = QVBoxLayout()
        for col in self.columns:
            if col == "permissions":
                layout.addLayout(self.create_input_field(col, items=[str(i) for i in range(0, 3)]))
            elif col == "password":
                layout.addLayout(self.create_input_field(col, is_password=True))
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def create_addtemp_fields(self):

        """Создает поля ввода для таблицы 'addtemp'."""

        layout = QVBoxLayout()
        exclude_fields = ["temp_user_id", "created_at"]
        for col in self.columns:
            if col in exclude_fields:
                 continue
            if col == "permissions":
                layout.addLayout(self.create_input_field(col, items=[str(i) for i in range(0, 3)]))
            else:
                layout.addLayout(self.create_input_field(col))
        return layout

    def fill_inputs(self):

        """Заполняет поля формы данными из выбранной строки."""

        try:
            self.row_index = int(self.input_field.text()) - 1
            if 0 <= self.row_index < len(self.data):
                for col in self.columns:
                    if col in self.inputs:
                        if isinstance(self.inputs[col], QComboBox):
                            index = self.inputs[col].findText(
                                str(self.data[self.row_index].get(col))
                            )
                            if index != -1:
                                self.inputs[col].setCurrentIndex(index)
                        else:
                            self.inputs[col].setText(
                                str(self.data[self.row_index].get(col, ""))
                            )
        except ValueError:
            pass

    def get_data(self):

        """Возвращает индекс строки и измененные данные."""

        try:
            self.row_index = int(self.input_field.text()) - 1
            if 0 <= self.row_index < len(self.data):
                updated_row = {}
                for key, input_field in self.inputs.items():
                    if isinstance(input_field, QComboBox):
                        updated_row[key] = input_field.currentData()
                    else:
                        updated_row[key] = input_field.text()       
                #  Изменение для корректной отправки данных оценки на сервер
                if self.table_type == "attestation":
                    updated_row["grade_100"] = int(updated_row["grade_100"]) if updated_row["grade_100"] else None
                    updated_row["student_id"] = updated_row.get("student_id")
                    updated_row["teacher_id"] = self.data[self.row_index].get("teacher_id", None)
                    updated_row["grade_id"] = self.data[self.row_index].get("grade_id", None)
                    for discipline in self.parent_app.data.get("data", {}).get("disciplines", []):
                        if discipline["discipline_name"] == updated_row["discipline_name"]:
                            updated_row["discipline_id"] = discipline["discipline_id"]
                            break
                elif self.parent_app.table_type == "addtemp":
                    updated_row["temp_user_id"] = self.data[self.row_index].get("temp_user_id", None)
                elif self.parent_app.table_type == "direction":
                    updated_row["direction_id"] = self.data[self.row_index].get("direction_id", None)
                elif self.parent_app.table_type == "dirt":
                    updated_row["teacher_id_new"] = updated_row["teacher_id"]
                    updated_row["teacher_id"] = self.data[self.row_index].get("teacher_id", None)
                    updated_row["direction_id_new"] = updated_row["direction_id"]
                    updated_row["direction_id"] = self.data[self.row_index].get("direction_id", None)
                elif self.parent_app.table_type == "discipline":
                    updated_row["discipline_id"] = self.data[self.row_index].get("discipline_id", None)
                elif self.parent_app.table_type == "disdir":
                    updated_row["discipline_id_new"] = updated_row["discipline_id"]
                    updated_row["discipline_id"] = self.data[self.row_index].get("discipline_id", None)
                    updated_row["direction_id_new"] = updated_row["direction_id"]
                    updated_row["direction_id"] = self.data[self.row_index].get("direction_id", None)
                elif self.parent_app.table_type == "student":
                    updated_row["student_id"] = self.data[self.row_index].get("student_id", None)
                elif self.parent_app.table_type == "studentgroup":
                    updated_row["group_id"] = self.data[self.row_index].get("group_id", None)
                elif self.parent_app.table_type == "grouplink":
                    updated_row["group_id_new"] = updated_row["group_id"]
                    updated_row["group_id"] = self.data[self.row_index].get("group_id", None)
                    updated_row["student_id_new"] = updated_row["student_id"]
                    updated_row["student_id"] = self.data[self.row_index].get("student_id", None)
                elif self.parent_app.table_type == "tdis":
                    updated_row["teacher_id_new"] = updated_row["teacher_id"]
                    updated_row["teacher_id"] = self.data[self.row_index].get("teacher_id", None)
                    updated_row["discipline_id_new"] = updated_row["discipline_id"]
                    updated_row["discipline_id"] = self.data[self.row_index].get("discipline_id", None)
                elif self.table_type == "user" and "password" in updated_row:
                    updated_row["password_hash"] = self.hash_data(updated_row["password"])
                    del updated_row["password"]
                return self.row_index, updated_row
        except ValueError:
            pass
        return None, None

    def hash_data(self, data):

        """Хеширует данные с помощью SHA256."""

        hash_object = hashlib.sha256(data.encode())
        return hash_object.hexdigest()                

    def validate_grade_100(self):

        """Валидирует значение в поле grade_100."""

        grade = self.inputs["grade_100"].text()
        if grade:
            try:
                grade = int(grade)
                if grade > 100:
                    self.inputs["grade_100"].setText("100")
            except ValueError:
                pass

class SelectSemesterDialog(BaseDialog):

    """Диалоговое окно выбора семестра."""

    def __init__(self, semesters, parent=None):
        super().__init__("Выбор семестра", parent)
        self.setStyleSheet(WINDOW_STYLES["select_semester"])  
        self.resize(400, 100)
        self.semesters = semesters
        self.selected_semester = None
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Выберите семестр:"))
        self.semester_combo = QComboBox()
        self.semester_combo.addItem("Все семестры")  # Добавляем "Все семестры"
        self.semester_combo.addItems([str(sem) for sem in semesters])
        layout.addWidget(self.semester_combo)
        select_button = QPushButton("Выбрать")
        select_button.clicked.connect(self.select_semester)
        layout.addWidget(select_button)
        self.setLayout(layout)
        self.center_window()
        
    def select_semester(self):

        """Обработчик выбора семестра."""

        selected_text = self.semester_combo.currentText()
        if selected_text == "Все семестры":
            self.selected_semester = None  # Устанавливаем None для "Все семестры"
        else:
            self.selected_semester = int(selected_text)
        self.accept()

class SelectGroupDialog(BaseDialog):

    """Диалоговое окно выбора группы."""

    def __init__(self, directions_groups, parent=None):
        super().__init__("Выбор направления и группы", parent)
        self.setStyleSheet(WINDOW_STYLES["select_group"])
        self.resize(400, 200)
        self.directions_groups = directions_groups
        self.selected_direction = None
        self.selected_group = None
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Выберите направление:"))
        self.direction_combo = QComboBox()
        self.direction_combo.addItem("Все направления")
        unique_directions = list(set(dg["direction_name"] for dg in directions_groups))
        self.direction_combo.addItems(unique_directions)
        self.direction_combo.currentIndexChanged.connect(self.update_groups)
        layout.addWidget(self.direction_combo)
        layout.addWidget(QLabel("Выберите группу:"))
        self.group_combo = QComboBox()
        layout.addWidget(self.group_combo)
        select_button = QPushButton("Выбрать")
        select_button.clicked.connect(self.select_group)
        layout.addWidget(select_button)
        self.setLayout(layout)
        self.update_groups()
        self.center_window()
        
    def update_groups(self):

        """Обновляет список групп в comboBox."""

        direction_name = self.direction_combo.currentText()
        self.group_combo.clear()
        if direction_name == "Все направления":
            groups = list(set(dg["group_name"] for dg in self.directions_groups))
            self.group_combo.addItem("Все группы")
        else:
            groups = [
                dg["group_name"]
                for dg in self.directions_groups
                if dg["direction_name"] == direction_name
            ]
            self.group_combo.addItem("Все группы выбранного направления")
        self.group_combo.addItems(groups)

    def select_group(self):

        """Обработчик выбора группы."""

        self.selected_direction = self.direction_combo.currentText()
        self.selected_group = self.group_combo.currentText()
        if self.selected_group == "Все группы выбранного направления":
            self.selected_group = [
                dg["group_name"]
                for dg in self.directions_groups
                if dg["direction_name"] == self.selected_direction
            ]
        self.accept()
