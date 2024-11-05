import json
import os
import requests
from PySide6.QtWidgets import QMessageBox
from sources.python.config import (
    ENDPOINTS,
    PATHS,
    WINDOW_STYLES,
    FONTS,
    SIZES,
    TABLES
)

class BaseWindow:
    def update_user_data(self, data):
        
        """Обновляет данные пользователя в файле."""
        
        if not os.path.exists('sources'):
            os.makedirs('sources')
        with open(PATHS["info_json"], 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def send_request(self, data, callback=None):
        
        """Отправляет запрос на сервер и обрабатывает ответ."""
        
        try:
            response = requests.post(ENDPOINTS["auth"], json=data, timeout=3)
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    self.update_user_data(result)
                    if callback is not None:
                        callback(data["username"], data["password"])
                else:
                    QMessageBox.warning(self, "Ошибка", result.get("message", "Неверное имя пользователя или пароль"))
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось подключиться к серверу")
        except requests.exceptions.ConnectTimeout:
            QMessageBox.warning(self, "Ошибка", "Время ожидания подключения истекло. Пожалуйста, попробуйте позже.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
