from Models.Category import Category

class CategoryController:
    '''
    Класс для работы с категориями (справочник)
    Реализация CRUD операций
    '''
    
    @classmethod
    def get(cls, active_only=True):
        '''
        Получение списка категорий
        :param active_only: если True - возвращаем только активные категории (если будет поле is_active)
        :return: список категорий (объект запроса)
        '''
        # В текущей модели нет поля is_active, но можно добавить позже
        return Category.select()
    
    @classmethod
    def get_by_id(cls, id):
        '''
        Получение категории по ID
        :param id: ID категории
        :return: объект категории или None
        '''
        return Category.get_or_none(Category.id == id)
    
    @classmethod
    def create(cls, name):
        '''
        Создание новой категории
        :param name: название категории
        :return: сообщение об успехе или ошибке
        '''
        try:
            Category.create(name=name)
            return f'Категория "{name}" успешно создана'
        except Exception as e:
            return f'Ошибка создания категории: {str(e)}'
    
    @classmethod
    def update(cls, id, **kwargs):
        '''
        Обновление категории
        :param id: ID категории
        :param kwargs: поля для обновления (например: name="Новое название")
        :return: сообщение об успехе или ошибке
        '''
        try:
            for key, value in kwargs.items():
                Category.update({key: value}).where(Category.id == id).execute()
            return f'Категория с ID {id} успешно обновлена'
        except Exception as e:
            return f'Ошибка обновления категории: {str(e)}'
    
    @classmethod
    def delete(cls, id):
        '''
        Удаление категории
        :param id: ID категории
        :return: сообщение об успехе или ошибке
        '''
        try:
            category = Category.get_by_id(id)
            if category:
                category.delete_instance()
                return f'Категория с ID {id} успешно удалена'
            else:
                return f'Категория с ID {id} не найдена'
        except Exception as e:
            return f'Ошибка удаления категории: {str(e)}'


if __name__ == "__main__":
    # Тестирование контроллера категорий
    print("=== Тестирование CategoryController ===")
    
    # Создание категории
    print(CategoryController.create("Проблемы с 1С"))
    print(CategoryController.create("Настройка почты"))
    print(CategoryController.create("Оборудование"))
    
    # Получение всех категорий
    print("\nСписок категорий:")
    for category in CategoryController.get():
        print(f"  {category.id}: {category.name}")
    
    # Обновление категории
    print(CategoryController.update(1, name="Проблемы с 1С (обновлено)"))
    
    # Получение по ID
    cat = CategoryController.get_by_id(1)
    if cat:
        print(f"\nКатегория по ID 1: {cat.name}")
    
    # Удаление категории (закомментировано, чтобы не удалять при тесте)
    # print(CategoryController.delete(3))