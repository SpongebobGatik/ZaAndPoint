import json
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QDialog,
    QGridLayout
)
from PySide6.QtGui import QIcon, QPixmap, QFont, QScreen
from PySide6.QtCore import Qt, QSize

from sources.python.base_window import BaseWindow
from sources.python.refresh_button import RefreshButton
from sources.python.сontact_info import ConnWindow
from sources.python.table_app import TableApp
from sources.python.welcome_dialog import WelcomeDialog
from sources.python.login_window import LoginWindow
from sources.python.config import (
    PATHS,
    SIZES,
    FONTS,
    WINDOW_STYLES
)

class PrototypeButton(QLabel):
    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.setStyleSheet("border: 10px solid black;")
        self.pixmap = QPixmap(icon_path)
        self.setPixmap(self.pixmap)
        self.setScaledContents(True)

class MainWindow(QMainWindow, BaseWindow):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.setWindowTitle("Зачётная Книжка и точка")
        self.setWindowIcon(QIcon(PATHS["icons"]["main"]))
        self.setMinimumSize(SIZES["main_window"]["min_width"],
                            SIZES["main_window"]["min_height"])
        self.resize(SIZES["main_window"]["min_width"],
                    SIZES["main_window"]["min_height"])
        # Устанавливаем изображение на задний фон
        self.setStyleSheet(WINDOW_STYLES["main"])
        central_widget = QWidget()
        layout = QVBoxLayout()
        self.windows = []
        try:
            with open('sources/info.json', 'r', encoding='utf-8') as f:
                user_data = json.load(f)
            if user_data['data']['permissions'] == 0:
                self.setup_student_ui(user_data['data']['group'][0]['student_name'], user_data['data']['group'][0]['group_name'], user_data['data']['group'][0]['faculty_name'])
                self.name = user_data['data']['group'][0]['student_name']
                self.email = user_data['data']['group'][0]['email']
                self.phone = user_data['data']['group'][0]['phone']
            elif user_data['data']['permissions'] == 1:
                self.setup_teacher_ui(user_data['data']['teacher_info'][0]['full_name'])
                self.name = user_data['data']['teacher_info'][0]['full_name']
                self.email = user_data['data']['teacher_info'][0]['email']
                self.phone = user_data['data']['teacher_info'][0]['phone']
            else:
                self.setup_secretary_ui(user_data['data']['secretary_info'][0]['full_name'])
                self.name = user_data['data']['secretary_info'][0]['full_name']
                self.email = user_data['data']['secretary_info'][0]['email']
                self.phone = user_data['data']['secretary_info'][0]['phone']      
            self.refresh_button = RefreshButton(self.username, self.password, self.send_request, self, self)
            self.refresh_button.setGeometry(700, 10, 80, 80)
            self.conn_window = ConnWindow(self, self.name, self.phone, self.email, self.username, self.password)
            self.windows.append(self.conn_window)
            self.con_button = QPushButton(self)
            self.con_button.setIcon(QIcon(PATHS["icons"]["contacts"]))
            self.con_button.setIconSize(QSize(80, 80))
            self.con_button.setStyleSheet("border-radius: 40px;")
            self.con_button.clicked.connect(self.show_conn_window)
            layout.addWidget(self.refresh_button)
            layout.addWidget(self.con_button)
            self.logout_button = QPushButton(self)
            self.logout_button.setIcon(QIcon(PATHS["icons"]["exit"]))
            self.logout_button.setIconSize(QSize(80, 80))
            self.logout_button.setStyleSheet("border-radius: 40px;")
            self.logout_button.clicked.connect(self.logout)
            layout.addWidget(self.logout_button)  
        except KeyError as e:
            QMessageBox.warning(self, "Error", f"Missing key in user data: {e}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred while setting up the main window: {e}")

    def logout(self):
        # Закрываем все окна классов и очищаем экземпляры
        for window in self.windows:
            window.close()
        self.windows.clear()
        # Закрываем главное окно
        self.close()
        # Очищаем файл info.json
        with open(PATHS["info_json"], 'w', encoding='utf-8') as f:
            json.dump({}, f)  
        # Открываем окно входа
        self.login_window = LoginWindow()
        self.login_window.show()

    def show_conn_window(self):
        if self.conn_window is not None:
            self.conn_window.close()
        self.conn_window = ConnWindow(self, self.name, self.phone, self.email, self.username, self.password)
        self.windows.append(self.conn_window)  # Добавляем окно в список
        self.conn_window.show()

    def show_windows(self, window_title, window_class_str, restart_act=None):
        if restart_act is None:
            self.close_all_windows()
            if hasattr(self, window_title) and getattr(self, window_title) is not None:
                getattr(self, window_title).close()  # Закрываем предыдущий экземпляр, если он существует
            setattr(self, window_title, eval(window_class_str))  # Создаем экземпляр класса из строки и присваиваем его атрибуту
            if getattr(self, window_title) not in self.windows:
                self.windows.append(getattr(self, window_title))  # Добавляем окно в список, если его там еще нет
            getattr(self, window_title).show()
        else:
            if hasattr(self, window_title) and getattr(self, window_title) is not None:
                if getattr(self, window_title).isVisible():  # Проверяем, показано ли окно
                    getattr(self, window_title).close()  # Закрываем предыдущий экземпляр, если он существует и показан
                    setattr(self, window_title, eval(window_class_str))  # Создаем экземпляр класса из строки и присваиваем его атрибуту
                    if getattr(self, window_title) not in self.windows:
                        self.windows.append(getattr(self, window_title))  # Добавляем окно в список, если его там еще нет
                    getattr(self, window_title).show()
                else:
                    # Если окна не показаны, ничего не делаем
                    pass

    def restart_no_press(self, restart_conn=None):
        data = {
            "username": self.username,
            "password": self.password
        }    
        self.send_request(data)
        if restart_conn is not None:
            self.update_ui(1)
        else:
            self.update_ui()

    def close_all_windows(self):
        for window in self.windows:
            window.close()
        self.windows.clear()
        
    def closeEvent(self, event):    
        # Закрываем все окна классов и очищаем экземпляры
        self.close_all_windows() 
        # Очищаем файл info.json при закрытии главного окна
        with open(PATHS["info_json"], 'w', encoding='utf-8') as f:
            json.dump({}, f)
        event.accept()
        
    def setup_student_ui(self, name, group, faculty):
        self.refresh_button_table_1 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_groupmates = TableApp('groupmates', self.refresh_button_table_1)
        self.windows.append(self.info_window_groupmates)
        self.refresh_button_table_2 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_teacher_contacts = TableApp('teachers', self.refresh_button_table_2)
        self.windows.append(self.info_window_teacher_contacts)
        self.refresh_button_table_3 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_grades = TableApp('grades', self.refresh_button_table_3)
        self.windows.append(self.info_window_grades)
        self.setup_ui(name, group, faculty, PATHS["icons"]["gl"],
                      [PATHS["icons"]["group"], PATHS["icons"]["results"], PATHS["icons"]["contacts_teacher"]],
                      ["info_window_groupmates", "info_window_grades", "info_window_teacher_contacts"],
                      ["TableApp('groupmates', self.refresh_button_table_1)", "TableApp('grades', self.refresh_button_table_3)", "TableApp('teachers', self.refresh_button_table_2)"])

    def setup_teacher_ui(self, name):
        self.refresh_button_table_1 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_employees = TableApp('employees', self.refresh_button_table_1)
        self.windows.append(self.info_window_employees)
        self.refresh_button_table_2 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_students = TableApp('students', self.refresh_button_table_2)
        self.windows.append(self.info_window_students)
        self.refresh_button_table_3 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_attestation = TableApp('attestation', self.refresh_button_table_3, self)
        self.windows.append(self.info_window_attestation)
        self.setup_ui(name, "Преподаватель (сотрудник)", "", PATHS["icons"]["gl"],
                      [PATHS["icons"]["attestation"], PATHS["icons"]["group_plus"], PATHS["icons"]["employees"]],
                      ["info_window_attestation", "info_window_students", "info_window_employees"],
                      ["TableApp('attestation', self.refresh_button_table_3, self)", "TableApp('students', self.refresh_button_table_2)", "TableApp('employees', self.refresh_button_table_1)"])

    def setup_secretary_ui(self, name):
        self.refresh_button_table_1 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_addtemp = TableApp('employees', self.refresh_button_table_1)
        self.windows.append(self.info_window_addtemp)
        self.refresh_button_table_2 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_employees = TableApp('addtemp', self.refresh_button_table_2, self)
        self.windows.append(self.info_window_employees)
        self.refresh_button_table_3 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_dir = TableApp('direction', self.refresh_button_table_3, self)
        self.windows.append(self.info_window_dir)
        self.refresh_button_table_4 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_dirt = TableApp('dirt', self.refresh_button_table_4, self)
        self.windows.append(self.info_window_dirt)
        self.refresh_button_table_5 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_discipline = TableApp('discipline', self.refresh_button_table_5, self)
        self.windows.append(self.info_window_discipline)
        self.refresh_button_table_6 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_disdir = TableApp('disdir', self.refresh_button_table_6, self)
        self.windows.append(self.info_window_disdir)
        self.refresh_button_table_7 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_student = TableApp('student', self.refresh_button_table_7, self)
        self.windows.append(self.info_window_student)
        self.refresh_button_table_8 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_studentgroup = TableApp('studentgroup', self.refresh_button_table_8, self)
        self.windows.append(self.info_window_studentgroup)
        self.refresh_button_table_9 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_grouplink = TableApp('grouplink', self.refresh_button_table_9, self)
        self.windows.append(self.info_window_grouplink)
        self.refresh_button_table_10 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_tdis = TableApp('tdis', self.refresh_button_table_10, self)
        self.windows.append(self.info_window_tdis)
        self.refresh_button_table_11 = RefreshButton(self.username, self.password, self.send_request, self)
        self.info_window_user = TableApp('user', self.refresh_button_table_11, self)
        self.windows.append(self.info_window_user)
        self.setup_ui(name, "Секретарь (сотрудник)", "", PATHS["icons"]["gl"],
                      [PATHS["icons"]["za"],  "mega mega_icon_1", "mega mega_icon_2", "mega mega_icon_3", "mega mega_icon_4", "mega mega_icon_5", "mega mega_icon_6", "mega mega_icon_7", "mega mega_icon_8", "mega mega_icon_9", PATHS["icons"]["employees"]],
                      ["info_window_addtemp", "info_window_dir", "info_window_dirt", "info_window_discipline", "info_window_disdir", "info_window_student", "info_window_studentgroup", "info_window_grouplink", "info_window_tdis", "info_window_user", "info_window_employees"],
                      ["TableApp('addtemp', self.refresh_button_table_2, self)", "TableApp('direction', self.refresh_button_table_3, self)", "TableApp('dirt', self.refresh_button_table_4, self)", "TableApp('discipline', self.refresh_button_table_5, self)", "TableApp('disdir', self.refresh_button_table_6, self)", "TableApp('student', self.refresh_button_table_7, self)", "TableApp('studentgroup', self.refresh_button_table_8, self)", "TableApp('grouplink', self.refresh_button_table_9, self)", "TableApp('tdis', self.refresh_button_table_10, self)", "TableApp('user', self.refresh_button_table_11, self)", "TableApp('employees', self.refresh_button_table_1)"])

    def setup_ui(self, name, group, faculty, icon_path, button_icons, window_titles, window_class_strs):
        central_widget = QWidget()
        layout = QVBoxLayout()
        # Создаем горизонтальный макет для имени студента и изображения
        name_layout = QHBoxLayout()
        if faculty != "":
            self.welcome_label = QLabel(f"{name}, {group} ({faculty})", self)
        else:
            self.welcome_label = QLabel(f"{name}, {group}", self)
        self.welcome_label.setFont(QFont(FONTS["welcome"]["family"], FONTS["welcome"]["size"], QFont.Bold))
        self.welcome_label.setWordWrap(True)
        self.welcome_label.setStyleSheet(WINDOW_STYLES["welcome_label"])
        name_layout.addWidget(self.welcome_label)
        # Добавляем метку с изображением и задаем фиксированный размер
        self.student_icon_label = QLabel()
        self.student_icon_pixmap = QPixmap(icon_path)
        self.student_icon_label.setPixmap(self.student_icon_pixmap.scaled(300, 310, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.student_icon_label.setFixedSize(300, 310)  # Фиксированный размер
        name_layout.addWidget(self.student_icon_label)
        layout.addLayout(name_layout)
        if group == "Секретарь (сотрудник)":
            # Создаем основной макет
            main_layout = QHBoxLayout()
            # Создаем макет для кнопок mega
            mega_button_layout = QGridLayout()
            row, col = 0, 0
            # Создаем макеты для обычных кнопок
            left_button_layout = QVBoxLayout()
            right_button_layout = QVBoxLayout()
            # Флаг для переключения между левым и правым макетом
            add_to_left = True
            for icon, window_title, window_class_str in zip(button_icons, window_titles, window_class_strs):
                if icon.startswith("mega"):
                    icon_paths = f"sources/img/{icon.split(' ')[1]}.png"
                    button = PrototypeButton(icon_paths)
                    button.mousePressEvent = lambda event, wt=window_title, wcs=window_class_str: self.show_windows(wt, wcs)
                    mega_button_layout.addWidget(button, row, col)
                    col += 1
                    if col == 3:
                        col = 0
                        row += 1
                else:
                    button = PrototypeButton(icon)
                    button.mousePressEvent = lambda event, wt=window_title, wcs=window_class_str: self.show_windows(wt, wcs)
                    if add_to_left:
                        left_button_layout.addWidget(button)
                        add_to_left = False
                    else:
                        right_button_layout.addWidget(button)
                        add_to_left = True
            # Добавляем макеты в основной макет
            main_layout.addLayout(left_button_layout)
            main_layout.addLayout(mega_button_layout)
            main_layout.addLayout(right_button_layout)
            layout.addLayout(main_layout)
        else:
            # Создаем кнопки независимо от содержимого JSON
            button_layout = QHBoxLayout()
            for icon, window_title, window_class_str in zip(button_icons, window_titles, window_class_strs):
                button = PrototypeButton(icon)
                button.mousePressEvent = lambda event, wt=window_title, wcs=window_class_str: self.show_windows(wt, wcs)
                button_layout.addWidget(button)
            layout.addLayout(button_layout)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.welcome_dialog = WelcomeDialog(name, self)
        self.welcome_dialog.show()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        new_size = event.size()
        icon_size = QSize(new_size.width() // 4 * 1.3, new_size.height() // 4 * 1.3)
        if hasattr(self, 'group_label'):
            self.group_label.setPixmap(self.group_label.pixmap.scaled(icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        if hasattr(self, 'session_results_label'):
            self.session_results_label.setPixmap(self.session_results_label.pixmap.scaled(icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        if hasattr(self, 'teacher_contacts_label'):
            self.teacher_contacts_label.setPixmap(self.teacher_contacts_label.pixmap.scaled(icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.refresh_button.setGeometry(new_size.width() - 90, 10, 80, 80)
        self.refresh_button.setIconSize(QSize(80, 80))
        self.con_button.setGeometry(new_size.width() - 90, 100, 80, 80)
        self.con_button.setIconSize(QSize(80, 80))
        self.logout_button.setGeometry(new_size.width() - 90, 190, 80, 80)
        self.logout_button.setIconSize(QSize(80, 80))
    
    def update_ui(self, restart_conn = None):
        try:
            with open(PATHS["info_json"], 'r', encoding='utf-8') as f:
                user_data = json.load(f)
            if user_data['data']['permissions'] == 0:
                self.student_name = user_data['data']['group'][0]['student_name']
                self.group_name = user_data['data']['group'][0]['group_name']
                self.faculty_name = user_data['data']['group'][0]['faculty_name']
                self.name = user_data['data']['group'][0]['student_name']
                self.email = user_data['data']['group'][0]['email']
                self.phone = user_data['data']['group'][0]['phone']
                self.welcome_label.setText(f"{self.student_name}, {self.group_name} ({self.faculty_name})")
                self.show_windows("info_window_groupmates","TableApp('groupmates', self.refresh_button_table_1)", 1)
                self.show_windows("info_window_teacher_contacts","TableApp('teachers', self.refresh_button_table_2)", 1)
                self.show_windows("info_window_grades","TableApp('grades', self.refresh_button_table_3)", 1)
            elif user_data['data']['permissions'] == 1:
                self.name = user_data['data']['teacher_info'][0]['full_name']
                self.email = user_data['data']['teacher_info'][0]['email']
                self.phone = user_data['data']['teacher_info'][0]['phone']
                self.welcome_label.setText(f"{self.name}, Преподаватель (сотрудник)")
                self.show_windows("info_window_employees","TableApp('employees', self.refresh_button_table_1)", 1)
                self.show_windows("info_window_students","TableApp('students', self.refresh_button_table_2)", 1)
                self.show_windows("info_window_attestation","TableApp('attestation', self.refresh_button_table_3, self)", 1)
            else:
                self.name = user_data['data']['secretary_info'][0]['full_name']
                self.email = user_data['data']['secretary_info'][0]['email']
                self.phone = user_data['data']['secretary_info'][0]['phone']
                self.welcome_label.setText(f"{self.name}, Секретарь (сотрудник)")
                self.show_windows("info_window_addtemp","TableApp('addtemp', self.refresh_button_table_2, self)", 1)
                self.show_windows("info_window_employees","TableApp('employees', self.refresh_button_table_1)", 1)
                self.show_windows("info_window_dir","TableApp('direction', self.refresh_button_table_3, self)", 1)
                self.show_windows("info_window_dirt","TableApp('dirt', self.refresh_button_table_4, self)", 1)
                self.show_windows("info_window_discipline","TableApp('discipline', self.refresh_button_table_5, self)", 1)
                self.show_windows("info_window_disdir","TableApp('disdir', self.refresh_button_table_6, self)", 1)
                self.show_windows("info_window_student","TableApp('student', self.refresh_button_table_7, self)", 1)
                self.show_windows("info_window_studentgroup","TableApp('studentgroup', self.refresh_button_table_8, self)", 1)
                self.show_windows("info_window_grouplink","TableApp('grouplink', self.refresh_button_table_9, self)", 1)
                self.show_windows("info_window_tdis","TableApp('tdis', self.refresh_button_table_10, self)", 1)
                self.show_windows("info_window_user","TableApp('user', self.refresh_button_table_11, self)", 1)
        except KeyError as e:
            QMessageBox.warning(self, "Error", f"Missing key in user data: {e}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred while updating the UI: {e}")
        if restart_conn is not None:
            self.show_conn_window()
