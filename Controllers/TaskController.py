from Models.Task import Task
from Models.User import User
from Models.Category import Category

class TaskController:
    '''
    Класс для работы с заявками (тикетами)
    Реализация CRUD и бизнес-логики согласно ТЗ
    '''
    
    @classmethod
    def get_all(cls):
        '''
        Получение всех заявок
        :return: список всех заявок
        '''
        return Task.select()
    
    @classmethod
    def get_by_id(cls, id):
        '''
        Получение заявки по ID
        :param id: ID заявки
        :return: объект заявки или None
        '''
        return Task.get_or_none(Task.id == id)
    
    @classmethod
    def get_by_user(cls, user_id):
        '''
        Получение заявок, созданных конкретным пользователем
        :param user_id: ID пользователя
        :return: список заявок пользователя
        '''
        return Task.select().where(Task.user_id == user_id)
    
    @classmethod
    def get_by_specialist(cls, specialist_id):
        '''
        Получение заявок, назначенных конкретному специалисту
        :param specialist_id: ID специалиста
        :return: список заявок специалиста
        '''
        return Task.select().where(Task.speciality_id == specialist_id)
    
    @classmethod
    def get_active(cls):
        '''
        Получение активных заявок (статус не "Выполнена")
        :return: список активных заявок
        '''
        return Task.select().where(Task.status != 'Выполнена')
    
    @classmethod
    def create(cls, topic, description, user_id, category_id, priority='Средний', status='Новая', file_path=None):
        '''
        Создание новой заявки (для пользователя)
        :param topic: тема заявки
        :param description: описание проблемы
        :param user_id: ID пользователя, создающего заявку
        :param category_id: ID категории
        :param priority: приоритет (Низкий, Средний, Высокий)
        :param status: статус (Новая, В работе, Выполнена)
        :param file_path: путь к прикрепленному файлу (опционально)
        :return: сообщение об успехе или ошибке
        '''
        try:
            # Проверяем существование пользователя и категории
            user = User.get_or_none(User.id == user_id)
            category = Category.get_or_none(Category.id == category_id)
            
            if not user:
                return 'Пользователь не найден'
            if not category:
                return 'Категория не найдена'
            
            Task.create(
                topic=topic,
                description=description,
                user_id=user_id,
                category_id=category_id,
                priority=priority,
                status=status,
                path=file_path or '',
                speciality_id=None  # Пока не назначен специалист
            )
            return f'Заявка "{topic}" успешно создана'
        except Exception as e:
            return f'Ошибка создания заявки: {str(e)}'
    
    @classmethod
    def update(cls, id, **kwargs):
        '''
        Обновление заявки
        :param id: ID заявки
        :param kwargs: поля для обновления
        :return: сообщение об успехе или ошибке
        '''
        try:
            for key, value in kwargs.items():
                Task.update({key: value}).where(Task.id == id).execute()
            return f'Заявка с ID {id} успешно обновлена'
        except Exception as e:
            return f'Ошибка обновления заявки: {str(e)}'
    
    @classmethod
    def delete(cls, id):
        '''
        Удаление заявки
        :param id: ID заявки
        :return: сообщение об успехе или ошибке
        '''
        try:
            task = Task.get_by_id(id)
            if task:
                task.delete_instance()
                return f'Заявка с ID {id} успешно удалена'
            else:
                return f'Заявка с ID {id} не найдена'
        except Exception as e:
            return f'Ошибка удаления заявки: {str(e)}'
    
    @classmethod
    def change_status(cls, id, new_status):
        '''
        Изменение статуса заявки (для специалиста)
        :param id: ID заявки
        :param new_status: новый статус (Новая, В работе, Выполнена, Ожидает ответа пользователя, Отклонена)
        :return: сообщение об успехе или ошибке
        '''
        try:
            task = Task.get_by_id(id)
            if not task:
                return 'Заявка не найдена'
            
            valid_statuses = ['Новая', 'В работе', 'Выполнена', 'Ожидает ответа пользователя', 'Отклонена']
            if new_status not in valid_statuses:
                return f'Недопустимый статус. Допустимые значения: {", ".join(valid_statuses)}'
            
            Task.update(status=new_status).where(Task.id == id).execute()
            return f'Статус заявки изменен на "{new_status}"'
        except Exception as e:
            return f'Ошибка изменения статуса: {str(e)}'
    
    @classmethod
    def assign_specialist(cls, id, specialist_id):
        '''
        Назначение специалиста на заявку
        :param id: ID заявки
        :param specialist_id: ID специалиста
        :return: сообщение об успехе или ошибке
        '''
        try:
            task = Task.get_by_id(id)
            specialist = User.get_or_none(User.id == specialist_id)
            
            if not task:
                return 'Заявка не найдена'
            if not specialist:
                return 'Специалист не найден'
            
            Task.update(speciality_id=specialist_id).where(Task.id == id).execute()
            return f'Специалист {specialist.login} назначен на заявку "{task.topic}"'
        except Exception as e:
            return f'Ошибка назначения специалиста: {str(e)}'
    
    @classmethod
    def take_to_work(cls, id, specialist_id):
        '''
        Взятие заявки в работу специалистом
        :param id: ID заявки
        :param specialist_id: ID специалиста
        :return: сообщение об успехе или ошибке
        '''
        try:
            task = Task.get_by_id(id)
            if not task:
                return 'Заявка не найдена'
            
            # Назначаем специалиста и меняем статус
            Task.update(
                speciality_id=specialist_id,
                status='В работе'
            ).where(Task.id == id).execute()
            
            return f'Заявка "{task.topic}" взята в работу'
        except Exception as e:
            return f'Ошибка взятия заявки в работу: {str(e)}'
    
    @classmethod
    def filter_tasks(cls, status=None, priority=None, category_id=None, user_id=None, specialist_id=None):
        '''
        Фильтрация заявок по различным параметрам (для ленты специалиста)
        :param status: статус заявки
        :param priority: приоритет
        :param category_id: ID категории
        :param user_id: ID пользователя
        :param specialist_id: ID специалиста
        :return: отфильтрованный список заявок
        '''
        query = Task.select()
        
        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        if category_id:
            query = query.where(Task.category_id == category_id)
        if user_id:
            query = query.where(Task.user_id == user_id)
        if specialist_id:
            query = query.where(Task.speciality_id == specialist_id)
        
        return query
    
    @classmethod
    def get_statistics(cls):
        '''
        Получение статистики по заявкам
        :return: словарь со статистикой
        '''
        total = Task.select().count()
        new = Task.select().where(Task.status == 'Новая').count()
        in_progress = Task.select().where(Task.status == 'В работе').count()
        completed = Task.select().where(Task.status == 'Выполнена').count()
        
        return {
            'total': total,
            'new': new,
            'in_progress': in_progress,
            'completed': completed
        }


if __name__ == "__main__":
    # Тестирование контроллера заявок
    print("=== Тестирование TaskController ===")
    
    # Для теста нужны существующие пользователи и категории
    # Сначала создадим тестовые данные, если их нет
    
    print("\n1. Создание тестовой заявки:")
    print(TaskController.create(
        topic="Проблема с доступом к 1С",
        description="Не могу зайти в 1С, выдает ошибку авторизации",
        user_id=1,  # Должен существовать пользователь с ID 1
        category_id=1,  # Должна существовать категория с ID 1
        priority="Высокий"
    ))
    
    print("\n2. Получение всех заявок:")
    for task in TaskController.get_all():
        print(f"  {task.id}: {task.topic} ({task.status})")
    
    print("\n3. Получение заявок пользователя ID 1:")
    for task in TaskController.get_by_user(1):
        print(f"  {task.id}: {task.topic}")
    
    print("\n4. Изменение статуса заявки:")
    print(TaskController.change_status(1, "В работе"))
    
    print("\n5. Назначение специалиста:")
    print(TaskController.assign_specialist(1, 2))  # Должен существовать специалист с ID 2
    
    print("\n6. Фильтрация заявок по статусу 'В работе':")
    for task in TaskController.filter_tasks(status="В работе"):
        print(f"  {task.id}: {task.topic}")
    
    print("\n7. Статистика заявок:")
    stats = TaskController.get_statistics()
    print(f"  Всего: {stats['total']}")
    print(f"  Новых: {stats['new']}")
    print(f"  В работе: {stats['in_progress']}")
    print(f"  Выполнено: {stats['completed']}")