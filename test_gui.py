#!/usr/bin/env python3
"""
Тестовый скрипт для проверки графического интерфейса управления пользователями
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Добавляем текущую директорию в путь для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Проверка импорта всех необходимых модулей"""
    print("=== Тестирование импортов ===")
    
    modules_to_test = [
        ("Controllers.UserController", "UserController"),
        ("Models.User", "User"),
        ("Views.UserView", "UserManagementWindow"),
        ("Views.AddUserWindow", "AddUserWindow"),
        ("Views.EditUserWindow", "EditUserWindow"),
    ]
    
    for module_path, class_name in modules_to_test:
        try:
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✓ {module_path}.{class_name}: OK")
        except Exception as e:
            print(f"✗ {module_path}.{class_name}: ERROR - {e}")
            import traceback
            traceback.print_exc()

def test_database():
    """Проверка подключения к базе данных"""
    print("\n=== Тестирование базы данных ===")
    
    try:
        from Controllers.UserController import UserController
        
        # Получаем список пользователей
        users = list(UserController.get())
        print(f"Пользователей в базе данных: {len(users)}")
        
        if users:
            print("Пример пользователя:")
            user = users[0]
            print(f"  ID: {user.id}, Логин: {user.login}, Роль: {user.role}, Активен: {user.is_active}")
        else:
            print("База данных пуста или нет подключения")
            
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        import traceback
        traceback.print_exc()

def test_gui():
    """Тестирование графического интерфейса"""
    print("\n=== Тестирование графического интерфейса ===")
    
    try:
        # Создаем тестовое окно
        root = tk.Tk()
        root.title("Тест GUI")
        root.geometry("300x200")
        
        # Скрываем основное окно
        root.withdraw()
        
        # Проверяем создание основного окна
        from Views.UserView import UserManagementWindow
        
        print("Создание главного окна управления пользователями...")
        try:
            main_window = UserManagementWindow()
            print("✓ Главное окно создано успешно")
            
            # Проверяем наличие виджетов
            widgets_found = []
            for widget_name in ['tree', 'add_button', 'edit_button', 'delete_button', 'status_bar']:
                if hasattr(main_window, widget_name):
                    widgets_found.append(widget_name)
            
            print(f"✓ Найдены виджеты: {', '.join(widgets_found)}")
            
            # Закрываем окно
            main_window.destroy()
            print("✓ Окно закрыто корректно")
            
        except Exception as e:
            print(f"✗ Ошибка создания главного окна: {e}")
            import traceback
            traceback.print_exc()
        
        # Проверяем создание окна добавления пользователя
        print("\nПроверка окна добавления пользователя...")
        try:
            from Views.AddUserWindow import AddUserWindow
            
            add_window = AddUserWindow(root)
            print("✓ Окно добавления пользователя создано успешно")
            
            # Проверяем наличие полей формы
            form_fields = ['login_entry', 'password_entry', 'role_combobox']
            fields_found = [field for field in form_fields if hasattr(add_window, field)]
            print(f"✓ Найдены поля формы: {', '.join(fields_found)}")
            
            add_window.destroy()
            print("✓ Окно закрыто корректно")
            
        except Exception as e:
            print(f"✗ Ошибка создания окна добавления: {e}")
            import traceback
            traceback.print_exc()
        
        # Проверяем создание окна редактирования пользователя
        print("\nПроверка окна редактирования пользователя...")
        try:
            from Views.EditUserWindow import EditUserWindow
            from Models.User import User
            
            # Получаем ID существующего пользователя для теста
            user = User.select().first()
            if user:
                edit_window = EditUserWindow(root, user.id)
                print(f"✓ Окно редактирования пользователя (ID: {user.id}) создано успешно")
                
                # Проверяем загрузку данных
                if hasattr(edit_window, 'user_data'):
                    print(f"✓ Данные пользователя загружены: {edit_window.user_data.login}")
                
                edit_window.destroy()
                print("✓ Окно закрыто корректно")
            else:
                print("⚠ Нет пользователей для тестирования окна редактирования")
                
        except Exception as e:
            print(f"✗ Ошибка создания окна редактирования: {e}")
            import traceback
            traceback.print_exc()
        
        # Закрываем корневое окно
        root.destroy()
        
    except Exception as e:
        print(f"Общая ошибка тестирования GUI: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Основная функция тестирования"""
    print("Тестирование графического интерфейса HelpDesk")
    print("=" * 60)
    
    test_imports()
    test_database()
    test_gui()
    
    print("\n" + "=" * 60)
    print("Тестирование завершено!")
    print("\nДля запуска приложения выполните:")
    print("  python main.py")

if __name__ == "__main__":
    main()