#!/usr/bin/env python3
"""
Основное окно управления пользователями системы HelpDesk
Реализует графический интерфейс для работы с UserController
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Добавляем путь для импорта модулей проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controllers.UserController import UserController

class UserManagementWindow(tk.Tk):
    """
    Главное окно управления пользователями
    Наследуется от tk.Tk для создания основного окна приложения
    """
    
    def __init__(self):
        """Инициализация главного окна управления пользователями"""
        super().__init__()
        
        # Настройка основного окна
        self.title("HelpDesk - Управление пользователями")
        self.geometry("1000x600")
        self.resizable(True, True)
        
        # Настройка стилей
        self.configure(bg='#f0f0f0')
        
        # Инициализация переменных
        self.selected_user_id = None
        
        # Создание виджетов
        self.create_widgets()
        
        # Загрузка данных пользователей
        self.load_users()
        
    def create_widgets(self):
        """Создание всех виджетов интерфейса"""
        
        # Создание фрейма для заголовка
        header_frame = tk.Frame(self, bg='#4a7a8c', height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # Заголовок
        title_label = tk.Label(
            header_frame,
            text="Управление пользователями системы HelpDesk",
            font=('Arial', 18, 'bold'),
            bg='#4a7a8c',
            fg='white'
        )
        title_label.pack(expand=True)
        
        # Создание фрейма для кнопок управления
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Кнопки управления
        button_style = {'font': ('Arial', 10), 'bg': '#5d9b9b', 'fg': 'white', 'height': 1, 'width': 20}
        
        self.add_button = tk.Button(
            button_frame,
            text="Добавить пользователя",
            command=self.add_user,
            **button_style
        )
        self.add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.edit_button = tk.Button(
            button_frame,
            text="Редактировать",
            command=self.edit_user,
            **button_style
        )
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = tk.Button(
            button_frame,
            text="Удалить",
            command=self.delete_user,
            **button_style
        )
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.status_button = tk.Button(
            button_frame,
            text="Изменить статус",
            command=self.change_status,
            **button_style
        )
        self.status_button.pack(side=tk.LEFT, padx=5)
        
        self.refresh_button = tk.Button(
            button_frame,
            text="Обновить",
            command=self.load_users,
            **button_style
        )
        self.refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Создание фрейма для таблицы
        table_frame = tk.Frame(self, bg='#f0f0f0')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Создание таблицы для отображения пользователей
        self.create_table(table_frame)
        
        # Статус бар
        self.status_bar = tk.Label(
            self,
            text="Готово",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg='#e0e0e0'
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_table(self, parent):
        """
        Создание таблицы Treeview для отображения списка пользователей
        
        Args:
            parent: родительский виджет для таблицы
        """
        # Создание Scrollbar для таблицы
        scrollbar_y = ttk.Scrollbar(parent, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(parent, orient=tk.HORIZONTAL)
        
        # Создание таблицы Treeview
        self.tree = ttk.Treeview(
            parent,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            selectmode='browse'
        )
        
        # Настройка scrollbar
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Определение колонок таблицы
        columns = ('id', 'login', 'role', 'is_active', 'fullname')
        self.tree['columns'] = columns
        
        # Форматирование колонок
        self.tree.column('#0', width=0, stretch=tk.NO)  # Скрытая колонка
        self.tree.column('id', width=50, anchor=tk.CENTER, minwidth=50)
        self.tree.column('login', width=150, anchor=tk.W, minwidth=100)
        self.tree.column('role', width=150, anchor=tk.W, minwidth=100)
        self.tree.column('is_active', width=100, anchor=tk.CENTER, minwidth=80)
        self.tree.column('fullname', width=300, anchor=tk.W, minwidth=200)
        
        # Заголовки колонок
        self.tree.heading('id', text='ID', anchor=tk.CENTER)
        self.tree.heading('login', text='Логин', anchor=tk.W)
        self.tree.heading('role', text='Роль', anchor=tk.W)
        self.tree.heading('is_active', text='Активен', anchor=tk.CENTER)
        self.tree.heading('fullname', text='Полное имя', anchor=tk.W)
        
        # Стиль таблицы
        style = ttk.Style()
        style.configure('Treeview', rowheight=25, font=('Arial', 10))
        style.configure('Treeview.Heading', font=('Arial', 11, 'bold'))
        
        # Размещение таблицы и scrollbar
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        # Настройка grid для изменения размеров
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # Привязка события выбора строки
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
    def load_users(self):
        """
        Загрузка списка пользователей из базы данных и отображение в таблице
        """
        try:
            # Очистка таблицы
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Получение списка пользователей через контроллер
            users = UserController.get()
            
            # Заполнение таблицы данными
            for user in users:
                # Преобразование булевого значения в читаемый текст
                is_active_text = 'Да' if user.is_active else 'Нет'
                
                # Вставка строки в таблицу
                self.tree.insert(
                    '',
                    tk.END,
                    values=(
                        user.id,
                        user.login,
                        user.role,
                        is_active_text,
                        user.fullname or ''
                    )
                )
            
            # Обновление статус бара
            self.status_bar.config(text=f"Загружено пользователей: {len(users)}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить пользователей: {str(e)}")
            self.status_bar.config(text="Ошибка загрузки данных")
    
    def on_select(self, event):
        """
        Обработчик события выбора строки в таблице
        
        Args:
            event: событие выбора
        """
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_user_id = item['values'][0]  # ID выбранного пользователя
            self.status_bar.config(text=f"Выбран пользователь ID: {self.selected_user_id}")
    
    def get_selected_user(self):
        """
        Получение ID выбранного пользователя
        
        Returns:
            ID выбранного пользователя или None, если ничего не выбрано
        """
        if not self.selected_user_id:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите пользователя из таблицы")
            return None
        return self.selected_user_id
    
    def add_user(self):
        """
        Открытие окна для добавления нового пользователя
        """
        # Импортируем здесь, чтобы избежать циклических импортов
        from Views.AddUserWindow import AddUserWindow
        
        # Создание и отображение окна добавления пользователя
        add_window = AddUserWindow(self)
        add_window.grab_set()  # Модальное окно
        
        # После закрытия окна обновляем таблицу
        self.wait_window(add_window)
        self.load_users()
    
    def edit_user(self):
        """
        Открытие окна для редактирования выбранного пользователя
        """
        # Получаем выбранного пользователя
        user_id = self.get_selected_user()
        if not user_id:
            return
        
        # Импортируем здесь, чтобы избежать циклических импортов
        from Views.EditUserWindow import EditUserWindow
        
        # Создание и отображение окна редактирования пользователя
        edit_window = EditUserWindow(self, user_id)
        edit_window.grab_set()  # Модальное окно
        
        # После закрытия окна обновляем таблицу
        self.wait_window(edit_window)
        self.load_users()
    
    def delete_user(self):
        """
        Удаление выбранного пользователя
        """
        # Получаем выбранного пользователя
        user_id = self.get_selected_user()
        if not user_id:
            return
        
        # Подтверждение удаления
        if not messagebox.askyesno(
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить пользователя с ID {user_id}?"
        ):
            return
        
        try:
            # Вызов метода удаления из контроллера
            # В текущем контроллере нет метода delete, используем update для установки is_active=False
            result = UserController.update(user_id, is_active=False)
            
            if "Ошибка" in result:
                messagebox.showerror("Ошибка", result)
            else:
                messagebox.showinfo("Успех", f"Пользователь с ID {user_id} деактивирован")
                self.load_users()  # Обновляем таблицу
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить пользователя: {str(e)}")
    
    def change_status(self):
        """
        Изменение статуса активности выбранного пользователя
        """
        # Получаем выбранного пользователя
        user_id = self.get_selected_user()
        if not user_id:
            return
        
        try:
            # Вызов метода изменения статуса из контроллера
            result = UserController.update_status(user_id)
            
            if "Ошибка" in result:
                messagebox.showerror("Ошибка", result)
            else:
                messagebox.showinfo("Успех", f"Статус пользователя с ID {user_id} изменен")
                self.load_users()  # Обновляем таблицу
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить статус: {str(e)}")


if __name__ == "__main__":
    # Тестовый запуск окна управления пользователями
    app = UserManagementWindow()
    app.mainloop()