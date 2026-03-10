#!/usr/bin/env python3
"""
Главный файл для запуска приложения HelpDesk
Точка входа в графический интерфейс пользователя
"""

import sys
import os

# Добавляем текущую директорию в путь для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Views.UserView import UserManagementWindow

def main():
    """
    Основная функция приложения
    Создает и запускает главное окно управления пользователями
    """
    try:
        # Создаем экземпляр главного окна
        app = UserManagementWindow()
        
        # Запускаем главный цикл обработки событий
        app.mainloop()
        
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())