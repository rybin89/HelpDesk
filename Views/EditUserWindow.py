#!/usr/bin/env python3
"""
Окно редактирования существующего пользователя в системе HelpDesk
Модальное окно для изменения данных пользователя
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Добавляем путь для импорта модулей проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controllers.UserController import UserController
from Models.User import User

class EditUserWindow(tk.Toplevel):
    """
    Окно для редактирования существующего пользователя
    Наследуется от tk.Toplevel для создания модального диалогового окна
    """
    
    def __init__(self, parent, user_id):
        """
        Инициализация окна редактирования пользователя
        
        Args:
            parent: родительское окно (UserManagementWindow)
            user_id: ID редактируемого пользователя
        """
        super().__init__(parent)
        
        # Настройка окна
        self.title(f"Редактирование пользователя ID: {user_id}")
        self.geometry("500x350")
        self.resizable(False, False)
        self.configure(bg='#f0f0f0')
        
        # Сохраняем ссылку на родительское окно и ID пользователя
        self.parent = parent
        self.user_id = user_id
        
        # Установка модального режима
        self.transient(parent)
        self.grab_set()
        
        # Инициализация переменных формы
        self.login_var = tk.StringVar()
        self.role_var = tk.StringVar()
        self.fullname_var = tk.StringVar()
        
        # Загрузка данных пользователя
        self.user_data = self.load_user_data()
        if not self.user_data:
            messagebox.showerror("Ошибка", f"Пользователь с ID {user_id} не найден")
            self.destroy()
            return
        
        # Заполнение переменных данными пользователя
        self.login_var.set(self.user_data.login)
        self.role_var.set(self.user_data.role)
        self.fullname_var.set(self.user_data.fullname or "")
        
        # Создание виджетов
        self.create_widgets()
        
        # Фокусировка на первом поле
        self.login_entry.focus_set()
        
        # Привязка события закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        
    def load_user_data(self):
        """
        Загрузка данных пользователя по ID
        
        Returns:
            Объект пользователя или None, если пользователь не найден
        """
        try:
            # Получение пользователя по ID
            user = User.get_or_none(User.id == self.user_id)
            return user
        except Exception as e:
            print(f"Ошибка загрузки данных пользователя: {e}")
            return None
    
    def create_widgets(self):
        """Создание всех виджетов формы редактирования пользователя"""
        
        # Создание фрейма для заголовка
        header_frame = tk.Frame(self, bg='#4a7a8c', height=60)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # Заголовок
        title_label = tk.Label(
            header_frame,
            text=f"Редактирование пользователя (ID: {self.user_id})",
            font=('Arial', 14, 'bold'),
            bg='#4a7a8c',
            fg='white'
        )
        title_label.pack(expand=True)
        
        # Создание основного фрейма для формы
        form_frame = tk.Frame(self, bg='#f0f0f0')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Метка и поле для логина
        login_label = tk.Label(
            form_frame,
            text="Логин*:",
            font=('Arial', 10),
            bg='#f0f0f0',
            anchor=tk.W
        )
        login_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.login_entry = tk.Entry(
            form_frame,
            textvariable=self.login_var,
            font=('Arial', 10),
            width=30
        )
        self.login_entry.grid(row=0, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        
        # Подсказка для логина
        login_hint = tk.Label(
            form_frame,
            text="(не более 12 символов, уникальный)",
            font=('Arial', 8),
            bg='#f0f0f0',
            fg='#666666'
        )
        login_hint.grid(row=1, column=1, sticky=tk.W, pady=(0, 15), padx=(10, 0))
        
        # Метка и выбор роли
        role_label = tk.Label(
            form_frame,
            text="Роль:",
            font=('Arial', 10),
            bg='#f0f0f0',
            anchor=tk.W
        )
        role_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        # Выпадающий список для выбора роли
        role_options = ["Пользователь", "Специалист", "Администратор"]
        self.role_combobox = ttk.Combobox(
            form_frame,
            textvariable=self.role_var,
            values=role_options,
            font=('Arial', 10),
            width=28,
            state="readonly"
        )
        self.role_combobox.grid(row=2, column=1, sticky=tk.W, pady=(0, 15), padx=(10, 0))
        
        # Метка и поле для полного имени
        fullname_label = tk.Label(
            form_frame,
            text="Полное имя:",
            font=('Arial', 10),
            bg='#f0f0f0',
            anchor=tk.W
        )
        fullname_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        self.fullname_entry = tk.Entry(
            form_frame,
            textvariable=self.fullname_var,
            font=('Arial', 10),
            width=30
        )
        self.fullname_entry.grid(row=3, column=1, sticky=tk.W, pady=(0, 20), padx=(10, 0))
        
        # Фрейм для кнопок
        button_frame = tk.Frame(form_frame, bg='#f0f0f0')
        button_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        # Кнопка сохранения
        save_button_style = {'font': ('Arial', 10), 'bg': '#5d9b9b', 'fg': 'white', 'width': 15}
        self.save_button = tk.Button(
            button_frame,
            text="Сохранить",
            command=self.save_changes,
            **save_button_style
        )
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Кнопка отмены
        cancel_button_style = {'font': ('Arial', 10), 'bg': '#9b5d5d', 'fg': 'white', 'width': 15}
        self.cancel_button = tk.Button(
            button_frame,
            text="Отмена",
            command=self.cancel,
            **cancel_button_style
        )
        self.cancel_button.pack(side=tk.LEFT)
        
        # Настройка grid для изменения размеров
        form_frame.grid_rowconfigure(4, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Привязка события нажатия Enter к сохранению изменений
        self.bind('<Return>', lambda event: self.save_changes())
        self.bind('<Escape>', lambda event: self.cancel())
        
    def validate_form(self):
        """
        Валидация данных формы
        
        Returns:
            True если данные валидны, False в противном случае
        """
        # Получение значений из формы
        login = self.login_var.get().strip()
        role = self.role_var.get()
        fullname = self.fullname_var.get().strip()
        
        # Проверка логина
        if not login:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите логин")
            self.login_entry.focus_set()
            return False
            
        if len(login) > 12:
            messagebox.showwarning("Предупреждение", "Логин не должен превышать 12 символов")
            self.login_entry.focus_set()
            return False
        
        # Проверка роли
        if role not in ["Пользователь", "Специалист", "Администратор"]:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите роль из списка")
            self.role_combobox.focus_set()
            return False
        
        # Проверка полного имени (необязательное поле)
        if fullname and len(fullname) > 150:
            messagebox.showwarning("Предупреждение", "Полное имя не должно превышать 150 символов")
            self.fullname_entry.focus_set()
            return False
        
        return True
    
    def save_changes(self):
        """Сохранение изменений данных пользователя"""
        # Валидация формы
        if not self.validate_form():
            return
        
        # Получение значений из формы
        login = self.login_var.get().strip()
        role = self.role_var.get()
        fullname = self.fullname_var.get().strip() or None
        
        # Подготовка данных для обновления
        update_data = {}
        
        # Проверяем, изменился ли логин
        if login != self.user_data.login:
            update_data['login'] = login
        
        # Проверяем, изменилась ли роль
        if role != self.user_data.role:
            update_data['role'] = role
        
        # Проверяем, изменилось ли полное имя
        current_fullname = self.user_data.fullname or ""
        new_fullname = fullname or ""
        if new_fullname != current_fullname:
            update_data['fullname'] = fullname
        
        # Если нет изменений
        if not update_data:
            messagebox.showinfo("Информация", "Нет изменений для сохранения")
            self.destroy()
            return
        
        try:
            # Вызов метода обновления из контроллера
            result = UserController.update(self.user_id, **update_data)
            
            # Проверка результата
            if "Ошибка" in result:
                messagebox.showerror("Ошибка", result)
            else:
                messagebox.showinfo("Успех", "Данные пользователя успешно обновлены")
                self.destroy()  # Закрытие окна
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить данные пользователя: {str(e)}")
    
    def cancel(self):
        """Отмена редактирования и закрытие окна"""
        if messagebox.askyesno("Отмена", "Вы уверены, что хотите отменить редактирование?"):
            self.destroy()


if __name__ == "__main__":
    # Тестовый запуск окна редактирования пользователя
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно
    
    # Для теста используем ID существующего пользователя
    from Models.User import User
    
    # Получаем первого пользователя из базы данных
    test_user = User.select().first()
    if test_user:
        app = EditUserWindow(root, test_user.id)
        app.mainloop()
    else:
        print("Нет пользователей для тестирования")