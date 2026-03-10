#!/usr/bin/env python3
"""
Тестовый скрипт для проверки контроллеров CategoryController и TaskController
"""

import sys
sys.path.insert(0, '.')

from Controllers.CategoryController import CategoryController
from Controllers.TaskController import TaskController
from Controllers.UserController import UserController
from Models.User import User
from Models.Category import Category

def test_category_controller():
    """Тестирование CategoryController"""
    print("\n=== Тестирование CategoryController ===")
    
    # Очистка старых тестовых категорий (если есть)
    Category.delete().where(Category.name.contains("Тест")).execute()
    
    # 1. Создание категорий
    print("1. Создание категорий:")
    print(CategoryController.create("Тест: Проблемы с сетью"))
    print(CategoryController.create("Тест: Программное обеспечение"))
    
    # 2. Получение всех категорий
    print("\n2. Список всех категорий:")
    categories = list(CategoryController.get())
    for cat in categories:
        print(f"  {cat.id}: {cat.name}")
    
    # 3. Получение категории по ID
    if categories:
        cat_id = categories[0].id
        print(f"\n3. Категория по ID {cat_id}:")
        cat = CategoryController.get_by_id(cat_id)
        if cat:
            print(f"  {cat.name}")
    
    # 4. Обновление категории
    if categories:
        print(f"\n4. Обновление категории ID {cat_id}:")
        print(CategoryController.update(cat_id, name="Тест: Проблемы с сетью (обновлено)"))
    
    # 5. Удаление категории (последней созданной)
    if len(categories) > 1:
        delete_id = categories[1].id
        print(f"\n5. Удаление категории ID {delete_id}:")
        print(CategoryController.delete(delete_id))
    
    # 6. Проверка после удаления
    print("\n6. Категории после удаления:")
    for cat in CategoryController.get():
        if "Тест" in cat.name:
            print(f"  {cat.id}: {cat.name}")

def test_task_controller():
    """Тестирование TaskController"""
    print("\n=== Тестирование TaskController ===")
    
    # Сначала создадим тестового пользователя и категорию, если их нет
    # Проверяем существование пользователя с ID 1
    try:
        test_user = User.get_or_none(User.id == 1)
        if not test_user:
            print("Создание тестового пользователя...")
            from bcrypt import hashpw, gensalt
            hashed = hashpw(b'testpass', gensalt())
            test_user = User.create(
                login='test_user',
                password=hashed,
                role='Пользователь',
                fullname='Тестовый Пользователь'
            )
            print(f"Создан пользователь ID {test_user.id}")
        else:
            print(f"Используем существующего пользователя ID {test_user.id}")
    except Exception as e:
        print(f"Ошибка с пользователем: {e}")
        return
    
    # Проверяем существование категории
    try:
        test_category = Category.get_or_none(Category.name.contains("Тест"))
        if not test_category:
            print("Создание тестовой категории...")
            test_category = Category.create(name="Тест: Категория для заявок")
            print(f"Создана категория ID {test_category.id}")
        else:
            print(f"Используем категорию ID {test_category.id}: {test_category.name}")
    except Exception as e:
        print(f"Ошибка с категорией: {e}")
        return
    
    # 1. Создание тестовой заявки
    print("\n1. Создание тестовой заявки:")
    result = TaskController.create(
        topic="Тестовая заявка",
        description="Описание тестовой проблемы для проверки контроллера",
        user_id=test_user.id,
        category_id=test_category.id,
        priority="Средний",
        status="Новая",
        file_path="/uploads/test.txt"
    )
    print(result)
    
    # 2. Получение всех заявок
    print("\n2. Все заявки:")
    tasks = list(TaskController.get_all())
    for task in tasks:
        print(f"  {task.id}: {task.topic} (статус: {task.status}, приоритет: {task.priority})")
    
    # 3. Получение заявок пользователя
    print(f"\n3. Заявки пользователя ID {test_user.id}:")
    user_tasks = list(TaskController.get_by_user(test_user.id))
    for task in user_tasks:
        print(f"  {task.id}: {task.topic}")
    
    # 4. Изменение статуса заявки
    if tasks:
        task_id = tasks[0].id
        print(f"\n4. Изменение статуса заявки ID {task_id}:")
        print(TaskController.change_status(task_id, "В работе"))
    
    # 5. Получение активных заявок
    print("\n5. Активные заявки (не выполненные):")
    active_tasks = list(TaskController.get_active())
    for task in active_tasks:
        print(f"  {task.id}: {task.topic} ({task.status})")
    
    # 6. Фильтрация заявок
    print("\n6. Фильтрация заявок по статусу 'В работе':")
    filtered = list(TaskController.filter_tasks(status="В работе"))
    for task in filtered:
        print(f"  {task.id}: {task.topic}")
    
    # 7. Статистика
    print("\n7. Статистика заявок:")
    stats = TaskController.get_statistics()
    print(f"  Всего заявок: {stats['total']}")
    print(f"  Новых: {stats['new']}")
    print(f"  В работе: {stats['in_progress']}")
    print(f"  Выполнено: {stats['completed']}")
    
    # 8. Очистка тестовых данных (опционально)
    print("\n8. Очистка тестовых данных...")
    from Models.Task import Task
    Task.delete().where(Task.topic.contains("Тест")).execute()
    print("Тестовые заявки удалены")

def test_imports():
    """Проверка импортов всех контроллеров"""
    print("\n=== Проверка импортов контроллеров ===")
    
    controllers = [
        ('CategoryController', CategoryController),
        ('TaskController', TaskController),
        ('UserController', UserController)
    ]
    
    for name, controller in controllers:
        print(f"{name}: OK")
        print(f"  Методы: {[m for m in dir(controller) if not m.startswith('_')]}")

def main():
    """Основная функция тестирования"""
    print("Тестирование контроллеров HelpDesk системы")
    print("=" * 50)
    
    try:
        test_imports()
        test_category_controller()
        test_task_controller()
        
        print("\n" + "=" * 50)
        print("Тестирование завершено успешно!")
        print("Созданы контроллеры для всех моделей (кроме User):")
        print("  - CategoryController: CRUD для категорий")
        print("  - TaskController: CRUD + бизнес-логика для заявок")
        print("  - UserController: уже существовал")
        
    except Exception as e:
        print(f"\nОшибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())