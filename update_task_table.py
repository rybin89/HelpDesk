#!/usr/bin/env python3
"""
Скрипт для обновления таблицы Task в базе данных
Добавляет возможность NULL для поля speciality_id
"""

import sys
sys.path.insert(0, '.')

from Connection.connect import connect
from Models.Task import Task

def update_table():
    """Обновление таблицы Task"""
    print("Обновление таблицы Task...")
    
    db = connect()
    
    try:
        # Удаляем существующую таблицу Task (если данные не важны)
        # Сначала проверим, есть ли данные в таблице
        task_count = Task.select().count()
        print(f"Текущее количество записей в таблице Task: {task_count}")
        
        if task_count > 0:
            print("В таблице Task есть данные. Не удаляем таблицу.")
            print("Вместо этого изменим структуру через ALTER TABLE.")
            
            # Попробуем изменить столбец через SQL
            with db.atomic():
                # Для MySQL
                db.execute_sql("ALTER TABLE task MODIFY COLUMN speciality_id INT NULL;")
                print("Структура таблицы Task обновлена (speciality_id теперь NULL)")
        else:
            print("Таблица Task пустая, можно пересоздать.")
            # Удаляем таблицу
            db.drop_tables([Task])
            print("Таблица Task удалена")
            
            # Создаем заново
            db.create_tables([Task])
            print("Таблица Task создана заново с новой структурой")
            
    except Exception as e:
        print(f"Ошибка при обновлении таблицы: {e}")
        import traceback
        traceback.print_exc()
        
        # Попробуем альтернативный подход
        try:
            print("\nПопытка альтернативного подхода...")
            # Создаем временную таблицу с новой структурой
            db.execute_sql("""
                CREATE TABLE task_new (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    topic VARCHAR(100),
                    description TEXT,
                    path VARCHAR(255),
                    priority ENUM('Низкий', 'Средний', 'Высокий'),
                    status ENUM('Новая', 'В работе', 'Выполнена'),
                    user_id INT,
                    speciality_id INT NULL,
                    category_id INT,
                    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (speciality_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE ON UPDATE CASCADE
                )
            """)
            print("Создана новая таблица task_new")
            
            # Копируем данные из старой таблицы (если есть)
            db.execute_sql("INSERT INTO task_new SELECT * FROM task")
            print("Данные скопированы в новую таблицу")
            
            # Удаляем старую таблицу
            db.execute_sql("DROP TABLE task")
            print("Старая таблица task удалена")
            
            # Переименовываем новую таблицу
            db.execute_sql("ALTER TABLE task_new RENAME TO task")
            print("Таблица переименована в task")
            
        except Exception as e2:
            print(f"Альтернативный подход также не удался: {e2}")
            return False
    
    finally:
        if db:
            db.close()
    
    return True

def test_table():
    """Тестирование обновленной таблицы"""
    print("\nТестирование обновленной таблицы...")
    
    try:
        # Пробуем создать запись с speciality_id = NULL
        from Models.User import User
        from Models.Category import Category
        
        # Получаем первого пользователя и первую категорию
        user = User.select().first()
        category = Category.select().first()
        
        if user and category:
            task = Task.create(
                topic="Тестовая задача",
                description="Описание тестовой задачи",
                path="",
                priority="Средний",
                status="Новая",
                user_id=user.id,
                speciality_id=None,  # Это должно работать теперь
                category_id=category.id
            )
            print(f"Создана тестовая задача ID {task.id} с speciality_id = NULL")
            
            # Удаляем тестовую задачу
            task.delete_instance()
            print("Тестовая задача удалена")
        else:
            print("Не найдены пользователь или категория для теста")
            
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("=== Обновление таблицы Task ===")
    
    if update_table():
        print("\nТаблица Task успешно обновлена")
        
        if test_table():
            print("\nТестирование прошло успешно!")
            print("Таблица Task готова к использованию с контроллерами")
        else:
            print("\nТестирование не прошло, но таблица обновлена")
    else:
        print("\nНе удалось обновить таблицу Task")
        sys.exit(1)