# Базовый URL для API
BASE_URL = "http://217.71.129.139:4140/assessment/"

# Эндпоинты API
ENDPOINTS = {
    "login": BASE_URL + "login.php",
    "register": BASE_URL + "register.php",
    "auth": BASE_URL + "auth.php",
    "update_info": BASE_URL + "update_con.php",
    "update": BASE_URL + "update_con.php",
    "add": BASE_URL + "add.php",
    "insert_at": BASE_URL + "insert_at.php",
    "insert_dir": BASE_URL + "insert_dir.php",
    "insert_dirt": BASE_URL + "insert_dirt.php",
    "insert_dis": BASE_URL + "insert_dis.php",
    "insert_disdir": BASE_URL + "insert_disdir.php",
    "insert_student": BASE_URL + "insert_student.php",
    "insert_st": BASE_URL + "insert_st.php",
    "insert_gr": BASE_URL + "insert_gr.php",
    "insert_tdis": BASE_URL + "insert_tdis.php",
    "insert_user": BASE_URL + "insert_user.php",
    "insert_temp": BASE_URL + "insert_temp.php",
    "delete_at": BASE_URL + "delete_at.php",
    "delete_temp": BASE_URL + "delete_temp.php",
    "delete_dir": BASE_URL + "delete_dir.php",
    "delete_dirt": BASE_URL + "delete_dirt.php",
    "delete_dis": BASE_URL + "delete_dis.php",
    "delete_disdir": BASE_URL + "delete_disdir.php"
}

# Пути к файлам и ресурсам
PATHS = {
    "info_json": "sources/info.json",
    "background": "sources/img/background_image.jpg",
    "icons": {
        "main": "sources/img/icon.png",
        "refresh": "sources/img/refresh_icon.png",
        "background": "sources/img/background_image.jpg",
        "add": "sources/img/add_icon.png",
        "delete": "sources/img/delete_icon.png",
        "change": "sources/img/change_icon.png",
        "save": "sources/img/save_icon.png",
        "select_semester": "sources/img/selectsm_icon.png",
        "select_group": "sources/img/selectgr_icon.png",
        "add_temp": "sources/img/addtemp_icon.png",
        "contacts": "sources/img/con_icon.png",
        "exit": "sources/img/exit_icon.png",
        "group": "sources/img/group_icon.png",
        "results": "sources/img/results_icon.png",
        "contacts_teacher": "sources/img/contacts_icon.png",
        "attestation": "sources/img/att_icon.png",
        "group_plus": "sources/img/groupp_icon.png",
        "employees": "sources/img/sot_icon.png",
        "gl": "sources/img/gl_icon.png",
        "za": "sources/img/za_icon.png",
        "mega_1": "sources/img/mega_icon_1.png",
        "mega_2": "sources/img/mega_icon_2.png",
        "mega_3": "sources/img/mega_icon_3.png",
        "mega_4": "sources/img/mega_icon_4.png",
        "mega_5": "sources/img/mega_icon_5.png",
        "mega_6": "sources/img/mega_icon_6.png",
        "mega_7": "sources/img/mega_icon_7.png",
        "mega_8": "sources/img/mega_icon_8.png",
        "mega_9": "sources/img/mega_icon_9.png"
    }
}

# Стили окон
WINDOW_STYLES = {
    "main": """
        QMainWindow {
            background-image: url('sources/img/background_image.jpg');
            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
        }
    """,
    "login": """
        QWidget {
            background-color: white;
        }
        QLineEdit {
            font-size: 14px;
            font-family: Arial, sans-serif;
            padding: 5px;
            border: 1px solid #FF6347;
            border-radius: 5px;
        }
        QPushButton {
            background-color: #FFD700;
            color: black;
            font-size: 14px;
            font-family: Arial, sans-serif;
            padding: 10px;
            border: none;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #FFC107;
        }
    """,
    "register": """
            QWidget {
                background-color: white;
            }
            QLineEdit {
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 5px;
                border: 1px solid #FF6347;
                border-radius: 5px;
            }
            QCheckBox {
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #FFD700;
                color: black;
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FFC107;
            }
        """,
    "dialog": """
        QDialog {
            background-color: #FFFACD;
        }
        QLabel {
            font-family: Arial, sans-serif;
            color: #333;
        }
        QLineEdit {
            padding: 5px;
            border: 1px solid #FF6347;
            border-radius: 5px;
        }
        QPushButton {
            background-color: black;
            color: white;
            padding: 10px;
            border-radius: 5px;
        }
    """,
    "table": """
        QTableWidget {
            border: 2px solid #FF6347;
            background-color: #FFFACD;
            padding: 10px;
            border-radius: 10px;
            margin: 20px;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
        QHeaderView::section {
            background-color: black;
            color: white;
            font-weight: bold;
            border: 1px solid #FF6347;
            padding: 5px;
        }
        QTableWidget::item {
            background-color: white;
            color: black;
            padding: 5px;
            border: 1px solid #FF6347;
        }
        QTableWidget::item:selected {
            background-color: #FF6347;
            color: white;
        }
    """,
    "side_panel": """
            QFrame {
                border: 2px solid #FF6347;
                background-color: #FFFACD;
                padding: 10px;
                border-radius: 10px;
                margin: 20px;
            }
            QPushButton {
                background-color: #FFD700;
                color: black;
                border-radius: 40px;
                padding: 10px;
                margin: 5px;
                min-width: 80px;
                min-height: 80px;
                max-width: 80px;
                max-height: 80px;
            }
        """,
    "welcome_label": """
        QLabel {
            text-decoration: underline;
            border: 2px solid #FF6347;
            background-color: #FFFACD;
            padding: 10px;
            border-radius: 10px;
        }
    """,
    "refresh_button": """
        background-color: #FFD700;
        color: black;
        border-radius: 40px;
        padding: 10px;
    """,
    "add": """
            QDialog {
                background-color: #FFFACD;
            }
            QLabel {
                font-size: 14px;
                font-family: Arial, sans-serif;
                color: #333;
            }
            QLineEdit {
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 5px;
                border: 1px solid #FF6347;
                border-radius: 5px;
            }
            QComboBox {
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 5px;
                border: 1px solid #FF6347;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #FFD700;
                color: black;
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FFC107;
            }
        """,
    "add_temp": """
            QDialog {
                background-color: #FFFACD;
            }
            QLabel {
                font-size: 14px;
                font-family: Arial, sans-serif;
                color: #333;
            }
            QLineEdit {
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 5px;
                border: 1px solid #FF6347;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #FFD700;
                color: black;
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FFC107;
            }
        """,
    "delete": """
            QDialog {
                background-color: #FFFACD;
            }
            QLabel {
                font-size: 14px;
                font-family: Arial, sans-serif;
                color: #333;
            }
            QLineEdit {
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 5px;
                border: 1px solid #FF6347;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #FFD700;
                color: black;
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FFC107;
            }
        """,
    "update": """
            QDialog {
                background-color: #FFFACD;
            }
            QLabel {
                font-size: 14px;
                font-family: Arial, sans-serif;
                color: #333;
            }
            QLineEdit {
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 5px;
                border: 1px solid #FF6347;
                border-radius: 5px;
            }
            QComboBox {
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 5px;
                border: 1px solid #FF6347;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #FFD700;
                color: black;
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FFC107;
            }
        """,
    "select_semester": """
            QDialog {
                background-color: #FFFACD;
            }
            QLabel {
                font-size: 14px;
                font-family: Arial, sans-serif;
                color: #333;
            }
            QComboBox {
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 5px;
                border: 1px solid #FF6347;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #FFD700;
                color: black;
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FFC107;
            }
        """,
    "select_group": """
            QDialog {
                background-color: #FFFACD;
            }
            QLabel {
                font-size: 14px;
                font-family: Arial, sans-serif;
                color: #333;
            }
            QComboBox {
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 5px;
                border: 1px solid #FF6347;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #FFD700;
                color: black;
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FFC107;
            }
        """,
    "refresh_success": """
            QMessageBox {
                background-color: #FFFACD;
                color: black;
            }
            QPushButton {
                background-color: black;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
        """,
    "prototype_button": "border: 10px solid black;",
    "login_button": "background-color: #FF6347; color: white;",
    "welcome_dialog": "background-color: #FFFACD;",
    "ok_button": "background-color: black; color: white;",
    "register_button": "color: blue; text-decoration: underline; background-color: transparent; border: none;"
}

# Настройки шрифтов
FONTS = {
    "default": {
        "family": "Arial",
        "size": 14,
        "weight": "Normal"
    },
    "header": {
        "family": "Arial",
        "size": 14,
        "weight": "Bold"
    },
    "welcome": {
        "family": "Comic Sans MS",
        "size": 25
    }
}

# Размеры окон и элементов
SIZES = {
    "login_window": {
        "min_width": 400,
        "min_height": 200
    },
    "register_window": {
        "min_width": 600,
        "min_height": 400
    },
    "main_window": {
        "min_width": 800,
        "min_height": 600
    },
    "welcome_dialog": {
        "min_width": 500,
        "min_height": 100
    },
    "buttons": {
        "icon": {
            "width": 80,
            "height": 80
        }
    }
}

# Настройки таблиц
TABLES = {
    "grades": {
        "title": "Результаты сессии",
        "columns": ["discipline_name", "teacher_name", "exam_type", "grade_100", "grade_5", "grade_date"],
        "data_key": "grades"
    },
    "students": {
        "title": "Студенты группы",
        "columns": ["student_name", "email", "phone"],
        "data_key": "group_members"
    },
    "teachers": {
        "title": "Контакты преподавателей",
        "columns": ["teacher_name", "email", "phone"],
        "data_key": "teachers"
    },
    "employees": {
        "title": "Сотрудники",
        "columns": ["full_name", "email", "phone"],
        "data_key": "all_teachers"
    },
    "groupmates": {
        "title": "Моя группа",
        "columns": ["full_name", "email", "phone"],
        "data_key": "groupmates"
    },
    "attestation": {
        "title": "Аттестация",
        "columns": ["semester", "discipline_name", "teacher_name", "student_name", "exam_type", "grade_100", "grade_5", "grade_date"],
        "data_key": "grades"
    },
    "addtemp": {
        "title": "Добавление Пользователей",
        "columns": ["temp_user_id", "login", "full_name", "email", "phone", "disciplines", "permissions", "created_at"],
        "data_key": "temp_users"
    },
    "tdis": {
        "title": "Связь преподавателя с дисциплиной",
        "columns": ["teacher_id", "discipline_id"],
        "data_key": "teacher_disciplines"
    },
    "user": {
        "title": "Все пользователи",
        "columns": ["user_id", "login", "password", "full_name", "email", "phone", "permissions"],
        "data_key": "users"
    },
    "direction": {
        "title": "Список направлений",
        "columns": ["direction_id", "direction_name", "faculty_name"],
        "data_key": "directions"
    },
    "dirt": {
        "title": "Связь преподавателя с направлением",
        "columns": ["direction_id", "teacher_id"],
        "data_key": "direction_teachers"
    },
    "discipline": {
        "title": "Список дисциплин",
        "columns": ["discipline_id", "discipline_name", "department_location"],
        "data_key": "disciplines"
    },
    "disdir": {
        "title": "Связь дисциплины с направлением",
        "columns": ["discipline_id", "direction_id"],
        "data_key": "discipline_directions"
    },
    "student": {
        "title": "Список студентов",
        "columns": ["student_id", "full_name", "email", "phone"],
        "data_key": "students"
    },
    "studentgroup": {
        "title": "Список групп",
        "columns": ["group_id", "group_name", "direction_id"],
        "data_key": "student_groups"
    },
    "grouplink": {
        "title": "Связь студента с группой",
        "columns": ["group_id", "student_id"],
        "data_key": "student_group_links"
    }
}

# Названия колонок на русском языке
COLUMN_TITLES = {
    "grade_id": "ID Оценки",
    "student_id": "ID Студента",
    "teacher_id": "ID Преподавателя",
    "grade_5": "Оценка (5-балльная)",
    "grade_100": "Оценка (100-балльная)",
    "grade_date": "Дата Оценки",
    "semester": "Семестр",
    "discipline_name": "Название Дисциплины",
    "student_name": "Имя Студента",
    "exam_type": "Тип Экзамена",
    "full_name": "ФИО",
    "email": "Электронная Почта",
    "phone": "Телефон",
    "login": "Логин",
    "password": "Пароль",
    "permissions": "Права Доступа",
    "direction_id": "ID Направления",
    "direction_name": "Название Направления",
    "group_id": "ID Группы",
    "group_name": "Название Группы",
    "created_at": "Дата Создания",
    "temp_user_id": "ID Временного Пользователя",
    "exam_date": "Дата Экзамена",
    "attendance": "Посещаемость",
    "status": "Статус",
    "comments": "Комментарии",
    "user_id": "ID Пользователя",
    "updated_at": "Дата Обновления",
    "discipline_id": "ID Дисциплины",
    "student_group_id": "ID Студенческой Группы",
    "teacher_name": "Имя Преподавателя",
    "course_name": "Название Курса",
    "course_id": "ID Курса",
    "disciplines": "Преподаваемые Дисциплины",
    "faculty_name": "Название Факультета",
    "department_location": "Местоположение Кафедры",
}
