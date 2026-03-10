#!/usr/bin/env python3
"""
Окно добавления нового пользователя в систему HelpDesk
Модальное окно для ввода данных нового пользователя
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Добавляем путь для импорта модулей проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controllers.UserController import UserController

class AddUserWindow(tk.Toplevel):
    """
    Окно для добавления нового пользователя
    Наследуется от tk.Toplevel для создания модального диалогового окна
    """
    
    def __init__(self, parent):
        """
        Инициализация окна добавления пользователя
        
        Args:
            parent: родительское окно (UserManagementWindow)
        """
        super().__init__(parent)
        
        # Настройка окна
        self.title("Добавление нового пользователя")
        self.geometry("500x400")
        self.resizable(False, False)
        self.configure(bg='#f0f0f0')
        
        # Сохраняем ссылку на родительское окно
        self.parent = parent
        
        # Установка модального режима
        self.transient(parent)
        self.grab_set()
        
        # Инициализация переменных формы
        self.login_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        self.role_var = tk.StringVar(value="Пользователь")
        self.fullname_var = tk.StringVar()
        
        # Создание виджетов
        self.create_widgets()
        
        # Фокусировка на первом поле
        self.login_entry.focus_set()
        
        # Привязка события закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        
    def create_widgets(self):
        """Создание всех виджетов формы добавления пользователя"""
        
        # Создание фрейма для заголовка
        header_frame = tk.Frame(self, bg='#4a7a8c', height=60)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # Заголовок
        title_label = tk.Label(
            header_frame,
            text="Добавление нового пользователя",
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
        
        # Метка и поле для пароля
        password_label = tk.Label(
            form_frame,
            text="Пароль*:",
            font=('Arial', 10),
            bg='#f0f0f0',
            anchor=tk.W
        )
        password_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            textvariable=self.password_var,
            font=('Arial', 10),
            width=30,
            show="*"
        )
        self.password_entry.grid(row=2, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        
        # Метка и поле для подтверждения пароля
        confirm_password_label = tk.Label(
            form_frame,
            text="Подтверждение пароля*:",
            font=('Arial', 10),
            bg='#f0f0f0',
            anchor=tk.W
        )
        confirm_password_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        self.confirm_password_entry = tk.Entry(
            form_frame,
            textvariable=self.confirm_password_var,
            font=('Arial', 10),
            width=30,
            show="*"
        )
        self.confirm_password_entry.grid(row=3, column=1, sticky=tk.W, pady=(0, 15), padx=(10, 0))
        
        # Метка и выбор роли
        role_label = tk.Label(
            form_frame,
            text="Роль:",
            font=('Arial', 10),
            bg='#f0f0f0',
            anchor=tk.W
        )
        role_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        
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
        self.role_combobox.grid(row=4, column=1, sticky=tk.W, pady=(0, 15), padx=(10, 0))
        
        # Метка и поле для полного имени
        fullname_label = tk.Label(
            form_frame,
            text="Полное имя:",
            font=('Arial', 10),
            bg='#f0f0f0',
            anchor=tk.W
        )
        fullname_label.grid(row=5, column=0, sticky=tk.W, pady=(0, 5))
        
        self.fullname_entry = tk.Entry(
            form_frame,
            textvariable=self.fullname_var,
            font=('Arial', 10),
            width=30
        )
        self.fullname_entry.grid(row=5, column=1, sticky=tk.W, pady=(0, 20), padx=(10, 0))
        
        # Фрейм для кнопок
        button_frame = tk.Frame(form_frame, bg='#f0f0f0')
        button_frame.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
        # Кнопка добавления
        add_button_style = {'font': ('Arial', 10), 'bg': '#5d9b9b', 'fg': 'white', 'width': 15}
        self.add_button = tk.Button(
            button_frame,
            text="Добавить",
            command=self.add_user,
            **add_button_style
        )
        self.add_button.pack(side=tk.LEFT, padx=(0, 10))
        
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
        form_frame.grid_rowconfigure(6, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Привязка события нажатия Enter к добавлению пользователя
        self.bind('<Return>', lambda event: self.add_user())
        self.bind('<Escape>', lambda event: self.cancel())
        
    def validate_form(self):
        """
        Валидация данных формы
        
        Returns:
            True если данные валидны, False в противном случае
        """
        # Получение значений из формы
        login = self.login_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
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
        
        # Проверка пароля
        if not password:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите пароль")
            self.password_entry.focus_set()
            return False
            
        if password != confirm_password:
            messagebox.showwarning("Предупреждение", "Пароли не совпадают")
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            self.password_entry.focus_set()
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
    
    def add_user(self):
        """Добавление нового пользователя в систему"""
        # Валидация формы
        if not self.validate_form():
            return
        
        # Получение значений из формы
        login = self.login_var.get().strip()
        password = self.password_var.get()
        role = self.role_var.get()
        fullname = self.fullname_var.get().strip() or None
        
        try:
            # Вызов метода регистрации из контроллера
            result = UserController.registration(
                login=login,
                password=password,
                role=role
            )
            
            # Если указано полное имя, обновляем пользователя
            if fullname and "Ошибка" not in result:
                # Нужно найти ID нового пользователя и обновить полное имя
                # Для простоты, в текущей реализации это делается отдельно
                # или можно добавить параметр fullname в метод registration
                pass
            
            # Проверка результата
            if "Ошибка" in result:
                messagebox.showerror("Ошибка", result)
            else:
                messagebox.showinfo("Успех", result)
                self.destroy()  # Закрытие окна
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить пользователя: {str(e)}")
    
    def cancel(self):
        """Отмена добавления пользователя и закрытие окна"""
        if messagebox.askyesno("Отмена", "Вы уверены, что хотите отменить добавление пользователя?"):
            self.destroy()


if __name__ == "__main__":
    # Тестовый запуск окна добавления пользователя
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно
    
    app = AddUserWindow(root)
    app.mainloop()