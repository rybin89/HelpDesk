# HelpDesk System

Проект HelpDesk системы для управления заявками пользователей. Реализован на Python с использованием ORM Peewee для работы с MySQL базой данных.

## Структура проекта

```
HelpDesk/
├── Connection/
│   └── connect.py         # Подключение к MySQL базе данных
├── Controllers/
│   └── UserController.py  # Контроллер для работы с пользователями
├── Models/
│   ├── Base.py            # Базовый класс моделей
│   ├── User.py            # Модель пользователя
│   ├── Task.py            # Модель задачи/заявки
│   ├── Category.py        # Модель категории
│   └── create_table.py    # Создание таблиц в базе данных
├── Views/                 # (Планируется) Представления/интерфейс
├── requirements.txt       # Зависимости Python
└── packages.txt           # Список пакетов
```

## Технологии

- **Python** - основной язык программирования
- **Peewee** (4.0.0) - ORM для работы с базой данных
- **PyMySQL** (1.1.2) - драйвер MySQL для Python
- **bcrypt** - библиотека для хеширования паролей
- **MySQL** - система управления базами данных

## Модели данных

### User (Пользователь)
- `id` - первичный ключ
- `login` - уникальный логин (макс. 12 символов)
- `password` - хешированный пароль
- `role` - роль пользователя: "Пользователь", "Администратор", "Специалист"
- `is_active` - статус активности (True/False)
- `fullname` - полное имя пользователя

### Task (Задача/Заявка)
- `id` - первичный ключ
- `topic` - тема заявки (макс. 100 символов)
- `description` - подробное описание проблемы
- `path` - путь к прикрепленному файлу
- `priority` - приоритет: "Низкий", "Средний", "Высокий"
- `status` - статус: "Новая", "В работе", "Выполнена"
- `user_id` - внешний ключ на пользователя-создателя
- `speciality_id` - внешний ключ на специалиста-исполнителя
- `category_id` - внешний ключ на категорию

### Category (Категория)
- `id` - первичный ключ
- `name` - уникальное название категории (макс. 150 символов)

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/rybin89/HelpDesk.git
   cd HelpDesk
   ```

2. Создайте виртуальное окружение Python:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # или
   .venv\Scripts\activate     # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Настройте подключение к базе данных в `Connection/connect.py`:
   ```python
   database = MySQLDatabase(
       'имя_базы_данных',
       user='пользователь',
       password='пароль',
       host='хост'
   )
   ```

5. Создайте таблицы в базе данных:
   ```bash
   python Models/create_table.py
   ```

## Использование

### Работа с пользователями

Пример использования UserController:

```python
from Controllers.UserController import UserController

# Регистрация нового пользователя
result = UserController.registration(
    login='newuser',
    password='password123',
    role='Пользователь'
)
print(result)

# Аутентификация пользователя
auth_result = UserController.auth('newuser', 'password123')
print(auth_result)

# Получение списка пользователей
users = UserController.get()
for user in users:
    print(user.id, user.login, user.role)

# Обновление информации о пользователе
update_result = UserController.update(1, login='updated_login', fullname='Иванов Иван')
print(update_result)

# Изменение статуса пользователя
status_result = UserController.update_status(1)
print(status_result)
```

### Создание моделей

Пример работы с моделями напрямую:

```python
from Models.User import User
from Models.Task import Task
from Models.Category import Category

# Создание категории
category = Category.create(name='Технические проблемы')

# Создание задачи
task = Task.create(
    topic='Не работает принтер',
    description='Принтер не печатает документы',
    priority='Высокий',
    status='Новая',
    user_id=1,
    category_id=category.id
)
```

## Безопасность

- Пароли пользователей хранятся в хешированном виде с использованием bcrypt
- Поддерживается проверка паролей через `checkpw()`
- Реализована система ролей для управления доступом

## Разработка

### Архитектура

Проект использует паттерн MVC (Model-View-Controller):
- **Models** - представление данных и бизнес-логики
- **Controllers** - обработка запросов и взаимодействие с моделями
- **Views** - представление данных пользователю (планируется)

### Расширение функциональности

1. Добавление новых контроллеров для работы с задачами и категориями
2. Реализация REST API для фронтенд-приложения
3. Создание веб-интерфейса (Views)
4. Добавление системы уведомлений
5. Реализация отчетов и статистики

## Лицензия

Проект находится в разработке.