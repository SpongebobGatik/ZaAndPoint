import json
from PySide6.QtWidgets import QMessageBox
from sources.python.config import PATHS, TABLES
from sources.python.table_window import TableWindow

class TableApp:

    """Приложение для работы с таблицами."""
    
    def __init__(self, table_type, refresh_button, main_window=None):
        self.json_file = PATHS["info_json"]
        self.background_image = PATHS["background"]
        self.table_type = table_type
        self.data = self.load_data()
        self.refresh_button = refresh_button
        self.main_window = main_window
        self.window = self.create_window()
        self.visible = False

    def load_data(self):

        """Загружает данные из JSON файла."""

        try:
            with open(self.json_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Файл {self.json_file} не найден.")
            return {"data": {}}

    def create_window(self):

        """Создает окно таблицы."""

        table_info = TABLES.get(self.table_type)
        if table_info:
            title = table_info["title"]
            columns = table_info["columns"]
            data_key = table_info.get("data_key", self.table_type)
            data = self.data.get("data", {}).get(data_key, [])
            if self.table_type in ["grades", "students"]:
                if self.table_type == "grades":
                    additional_params = {"semesters": list(set(item["semester"] for item in data))}
                else:  # self.table_type == "students"
                    additional_params = {"directions_groups": self.data.get("data", {}).get("directions_groups", [])}
                window = TableWindow(title, data, columns, self.background_image, self.refresh_button, 
                                    self.table_type, self, main_window=self.main_window, **additional_params)
            else:
                window = TableWindow(title, data, columns, self.background_image, self.refresh_button, 
                                    self.table_type, self, main_window=self.main_window)

            if self.table_type == "teachers":
                data = self.remove_duplicates(data, ["teacher_name", "email", "phone"])
                window.update_table_data(data)  # Обновляем данные в окне
            elif self.table_type == "employees":
                data += self.data.get("data", {}).get("all_secretaries", [])
                window.update_table_data(data)  # Обновляем данные в окне
            return window
        else:
            raise ValueError("Invalid table type")

    def remove_duplicates(self, data, keys):
        seen = set()
        unique_data = []
        for item in data:
            identifier = tuple(item[key] for key in keys)
            if identifier not in seen:
                unique_data.append(item)
                seen.add(identifier)
        return unique_data
    
    def show(self):

        """Показывает окно таблицы."""

        self.window.showMaximized()
        self.visible = True

    def close(self):

        """Закрывает окно таблицы."""

        self.window.close()
        self.visible = False

    def isVisible(self):

        """Возвращает True, если окно таблицы видимо."""

        return self.visible

    def load_semester_grades(self, semester):

        """Загружает оценки для выбранного семестра."""

        grades = self.data.get("data", {}).get("grades", [])
        if semester is None:  # Обработка "Все семестры"
            filtered_grades = grades  # Берем все оценки
        else:
            filtered_grades = [grade for grade in grades if grade["semester"] == semester]
        self.window.update_table_data(filtered_grades)

    def load_group_students(self, direction_name, group_name):

        """Загружает студентов для выбранной группы."""

        group_members = self.data.get("data", {}).get("group_members", [])
        if direction_name == "Все направления" and group_name == "Все группы":
            students = group_members
        elif group_name == "Все группы выбранного направления":
            students = [
                member for member in group_members 
                if member["direction_name"] == direction_name
            ]
        elif isinstance(group_name, list):
            students = [
                member for member in group_members 
                if member["group_name"] in group_name
            ]
        else:
            students = [
                member for member in group_members 
                if member["group_name"] == group_name
            ]  
        # Если список студентов пуст, создаем пустую таблицу
        if not students:
            empty_student = {key: "" for key in self.window.columns}
            students = [empty_student]
        self.window.update_table_data(students)
