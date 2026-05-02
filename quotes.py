import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os

# --- 1. Настройка данных и путей ---
DATA_FILE = "quotes.json"

# --- 2. Функции для работы с данными (JSON) ---
def load_data():
    """Загружает цитаты и историю из файла JSON."""
    if not os.path.exists(DATA_FILE):
        # Если файла нет, создаем его с начальными данными
        initial_quotes = [
            {"text": "Секрет успеха — постоянство цели.", "author": "Бенджамин Дизраэли", "topic": "мотивация"},
            {"text": "Жизнь — это то, что происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "жизнь"},
            {"text": "Единственный способ делать великие дела — любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "работа"},
            {"text": "Знание — сила.", "author": "Фрэнсис Бэкон", "topic": "знания"},
        ]
        save_data(initial_quotes)
        return initial_quotes
    else:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

def save_data(data):
    """Сохраняет список цитат в файл JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- 3. Основной класс приложения ---
class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("600x500")

        # Загружаем данные
        self.all_quotes = load_data()
        self.history = [] # История сгенерированных цитат в текущем сеансе

        # --- 4. Создание виджетов GUI ---

        # Рамка для отображения текущей цитаты
        quote_frame = tk.Frame(root)
        quote_frame.pack(pady=10, fill=tk.X)

        self.quote_label = tk.Label(
            quote_frame,
            text="Нажмите кнопку, чтобы получить цитату",
            wraplength=500,
            font=('Arial', 12),
            justify="center"
        )
        self.quote_label.pack()

        # Кнопка генерации
        self.generate_btn = tk.Button(
            root,
            text="Сгенерировать цитату",
            font=('Arial', 12),
            command=self.generate_quote
        )
        self.generate_btn.pack(pady=10)

        # Рамка для фильтров
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Автор:").pack(side=tk.LEFT)
        self.author_entry = tk.Entry(filter_frame)
        self.author_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(filter_frame, text="Тема:").pack(side=tk.LEFT)
        self.topic_entry = tk.Entry(filter_frame)
        self.topic_entry.pack(side=tk.LEFT, padx=5)

        self.filter_btn = tk.Button(
            root,
            text="Найти по фильтру",
            command=self.generate_filtered_quote
        )
        self.filter_btn.pack(pady=5)

        # Рамка для истории и кнопок управления
        history_frame = tk.Frame(root)
        history_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.history_listbox = tk.Listbox(history_frame, width=70, height=10)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(history_frame, command=self.history_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        btns_frame = tk.Frame(root)
        btns_frame.pack()

        self.save_history_btn = tk.Button(
            btns_frame,
            text="Сохранить историю",
            command=self.save_history_to_file
        )
        self.save_history_btn.pack(side=tk.LEFT, padx=5)

        self.clear_history_btn = tk.Button(
            btns_frame,
            text="Очистить историю",
            command=self.clear_history_gui
        )
        self.clear_history_btn.pack(side=tk.LEFT, padx=5)

    # --- 5. Логика генерации цитат ---
    def generate_quote(self):
        """Генерирует случайную цитату из всего списка."""
        if not self.all_quotes:
            messagebox.showwarning("Пусто", "База цитат пуста.")
            return

        quote = random.choice(self.all_quotes)
        
         # Добавляем в историю (если еще нет)
         # Проверка на дубликаты в текущем сеансе по тексту и автору
         is_duplicate = any(
             q["text"] == quote["text"] and q["author"] == quote["author"]
             for q in self.history
         )
         if not is_duplicate:
             self.history.append(quote)
             self.update_history_list()
        
         self.display_quote(quote)

    def generate_filtered_quote(self):
         """Генерирует случайную цитату на основе фильтров."""
         author_filter = self.author_entry.get().strip().lower()
         topic_filter = self.topic_entry.get().strip().lower()
         
         filtered_quotes = [
             q for q in self.all_quotes
             if (not author_filter or author_filter in q["author"].lower())
             and (not topic_filter or topic_filter in q["topic"].lower())
         ]
         
         if not filtered_quotes:
             messagebox.showinfo("Результат", "Нет цитат по заданным критериям.")
             return

         quote = random.choice(filtered_quotes)
         is_duplicate = any(
             q["text"] == quote["text"] and q["author"] == quote["author"]
             for q in self.history
         )
         if not is_duplicate:
             self.history.append(quote)
             self.update_history_list()
         
         self.display_quote(quote)
    
    def display_quote(self, quote):
         """Отображает цитату в главном лейбле."""
         self.quote_label.config(text=f'"{quote["text"]}"\n— {quote["author"]}')
    
    # --- 6. Логика работы с историей ---
    def update_history_list(self):
         """Обновляет виджет Listbox с историей."""
         self.history_listbox.delete(0, tk.END) # Очищаем список
         for q in self.history:
              entry_text = f'"{q["text"]}" — {q["author"]}'
              if len(entry_text) > 80: # Обрезаем слишком длинные строки для красоты
                  entry_text = entry_text[:77] + "..."
              self.history_listbox.insert(tk.END, entry_text)
    
    def save_history_to_file(self):
         """Сохраняет текущую историю сеанса в конец файла JSON."""
         if not self.history:
              messagebox.showinfo("История", "История пуста. Нечего сохранять.")
              return

         existing_data = load_data()
         # Добавляем только новые цитаты из истории сеанса (по тексту и автору), чтобы избежать дублей в базе
         for new_quote in self.history:
              is_duplicate_in_db = any(
                  q["text"] == new_quote["text"] and q["author"] == new_quote["author"]
                  for q in existing_data
              )
              if not is_duplicate_in_db:
                  existing_data.append(new_quote)
         
         save_data(existing_data)
         messagebox.showinfo("Успех", f"История сохранена! Всего цитат в базе: {len(existing_data)}")
    
    def clear_history_gui(self):
         """Очищает историю только в текущем сеансе (в GUI)."""
          self.history.clear()
          self.update_history_list()
          self.quote_label.config(text="История очищена")