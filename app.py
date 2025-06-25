import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
from tkinter import font as tkfont
from src.predict import SentimentAnalyzer


class ResizableSentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализатор тональности текста")
        self.root.geometry("1100x750")
        self.root.minsize(900, 650)
        self.root.configure(bg='#121212')

        # Настройка стилей
        self.setup_styles()
        self.load_icon()
        self.analyzer = SentimentAnalyzer()

        # Главный контейнер
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Создание разделяемых панелей
        self.create_panes()
        self.center_window()

    def setup_styles(self):
        self.colors = {
            "bg": "#121212",
            "card_bg": "#1e1e1e",
            "text": "#e1e1e1",
            "primary": "#BB86FC",
            "primary_hover": "#9a67d3",
            "secondary": "#03DAC6",
            "danger": "#CF6679",
            "input_bg": "#2d2d2d",
            "positive": "#4cc9f0",
            "negative": "#CF6679",
            "neutral": "#BB86FC",
            "border": "#333333"
        }

    def load_icon(self):
        try:
            icon_path = os.path.join("img", "CPE.png")
            icon = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, icon)
        except:
            pass

    def create_panes(self):
        # Панель для разделения
        self.pane_container = tk.PanedWindow(
            self.main_frame,
            orient=tk.HORIZONTAL,
            bg=self.colors["bg"],
            sashwidth=10,
            sashrelief=tk.RAISED,
            sashpad=3,
            opaqueresize=False
        )
        self.pane_container.pack(fill=tk.BOTH, expand=True)

        # Левая панель (ввод)
        self.left_pane = tk.Frame(
            self.pane_container,
            bg=self.colors["bg"],
            padx=10,
            pady=10
        )
        self.create_input_widgets(self.left_pane)

        # Правая панель (результаты)
        self.right_pane = tk.Frame(
            self.pane_container,
            bg=self.colors["bg"],
            padx=10,
            pady=10
        )
        self.create_output_widgets(self.right_pane)

        # Добавляем панели с начальными пропорциями
        self.pane_container.add(self.left_pane, minsize=300)
        self.pane_container.add(self.right_pane, minsize=300)

        # Устанавливаем начальное соотношение 50/50
        self.pane_container.paneconfig(self.left_pane, width=500)
        self.pane_container.paneconfig(self.right_pane, width=500)

    def create_input_widgets(self, parent):
        # Карточка ввода
        input_card = tk.Frame(
            parent,
            bg=self.colors["card_bg"],
            padx=15,
            pady=15,
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        input_card.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        tk.Label(
            input_card,
            text="Введите текст для анализа:",
            font=('Segoe UI', 12),
            bg=self.colors["card_bg"],
            fg=self.colors["text"]
        ).pack(anchor=tk.W, pady=(0, 10))

        # Поле ввода
        self.text_input = tk.Text(
            input_card,
            height=15,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            bg=self.colors["input_bg"],
            fg=self.colors["text"],
            insertbackground=self.colors["primary"],
            padx=10,
            pady=10,
            relief=tk.FLAT,
            highlightthickness=0
        )
        self.text_input.pack(fill=tk.BOTH, expand=True)

        # Кнопки
        btn_frame = tk.Frame(input_card, bg=self.colors["card_bg"])
        btn_frame.pack(fill=tk.X, pady=(15, 0))

        tk.Button(
            btn_frame,
            text="Анализировать",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors["primary"],
            fg="#121212",
            activebackground=self.colors["primary_hover"],
            activeforeground="#121212",
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            command=self.start_analysis
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            btn_frame,
            text="Очистить",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors["secondary"],
            fg="#121212",
            activebackground="#02c0af",
            activeforeground="#121212",
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            command=self.clear_text
        ).pack(side=tk.LEFT)

    def create_output_widgets(self, parent):
        # Карточка результатов
        output_card = tk.Frame(
            parent,
            bg=self.colors["card_bg"],
            padx=15,
            pady=15,
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        output_card.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        tk.Label(
            output_card,
            text="Результаты анализа:",
            font=('Segoe UI', 12),
            bg=self.colors["card_bg"],
            fg=self.colors["text"]
        ).pack(anchor=tk.W, pady=(0, 10))

        # Основной результат
        self.result_frame = tk.Frame(output_card, bg=self.colors["card_bg"])
        self.result_frame.pack(fill=tk.X, pady=(0, 20))

        self.result_label = tk.Label(
            self.result_frame,
            text="Тональность: Не анализировано",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors["card_bg"],
            fg=self.colors["secondary"]
        )
        self.result_label.pack(anchor=tk.W)

        # Детализированные результаты
        details_frame = tk.Frame(output_card, bg=self.colors["card_bg"])
        details_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            details_frame,
            text="Распределение вероятностей:",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors["card_bg"],
            fg=self.colors["text"]
        ).pack(anchor=tk.W, pady=(0, 10))

        self.details_text = tk.Text(
            details_frame,
            height=8,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            state='disabled',
            bg=self.colors["card_bg"],
            fg=self.colors["text"],
            padx=5,
            pady=5,
            relief=tk.FLAT,
            highlightthickness=0
        )
        self.details_text.pack(fill=tk.BOTH, expand=True)

        # Статус бар
        self.status_bar = tk.Label(
            output_card,
            text="Готов к анализу",
            relief=tk.FLAT,
            anchor=tk.W,
            font=('Segoe UI', 9),
            fg=self.colors["text"],
            bg=self.colors["card_bg"]
        )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))

    def start_analysis(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if len(text.split()) < 2:
            messagebox.showwarning("Требуется ввод", "Пожалуйста, введите хотя бы 2 слова для точного анализа.")
            return

        self.status_bar.config(text="Анализ текста...")
        self.update_result("Анализ...", self.colors["secondary"])

        threading.Thread(
            target=self.analyze_text,
            args=(text,),
            daemon=True
        ).start()

    def analyze_text(self, text):
        try:
            result = self.analyzer.analyze_text(text)
            self.root.after(0, lambda: self.show_results(result))
            self.root.after(0, lambda: self.status_bar.config(text="Анализ завершен"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Ошибка анализа", str(e)))
            self.root.after(0, lambda: self.status_bar.config(text="Произошла ошибка"))
            self.root.after(0, lambda: self.update_result("Ошибка анализа", self.colors["danger"]))

    def show_results(self, result):
        sentiment = {
            "positive": "Позитивная",
            "negative": "Негативная",
            "neutral": "Нейтральная"
        }.get(result['label'], "Не определена")

        confidence = f"{result['confidence']:.1%}" if 'confidence' in result else "N/A"

        color_map = {
            "positive": self.colors["positive"],
            "negative": self.colors["negative"],
            "neutral": self.colors["neutral"]
        }

        color = color_map.get(result['label'], self.colors["secondary"])

        self.update_result(f"{sentiment} ({confidence})", color)
        self.update_details(result)

    def update_result(self, text, color):
        self.result_label.config(text=f"Тональность: {text}", fg=color)

    def update_details(self, result):
        self.details_text.config(state='normal')
        self.details_text.delete('1.0', tk.END)

        if 'scores' in result:
            self.details_text.insert(tk.END, "\nДетальный анализ:\n\n", "bold")
            self.details_text.insert(tk.END, f"▪️ Негативная: {result['scores'][0]:.1%}\n", "negative")
            self.details_text.insert(tk.END, f"▪️ Нейтральная: {result['scores'][1]:.1%}\n", "neutral")
            self.details_text.insert(tk.END, f"▪️ Позитивная: {result['scores'][2]:.1%}", "positive")

            self.details_text.tag_config("bold", font=('Segoe UI', 10, 'bold'))
            self.details_text.tag_config("negative", foreground=self.colors["negative"])
            self.details_text.tag_config("neutral", foreground=self.colors["neutral"])
            self.details_text.tag_config("positive", foreground=self.colors["positive"])
        else:
            self.details_text.insert(tk.END, "\nДетальная информация недоступна")

        self.details_text.config(state='disabled')

    def clear_text(self):
        self.text_input.delete("1.0", tk.END)
        self.update_result("Не анализировано", self.colors["secondary"])
        self.details_text.config(state='normal')
        self.details_text.delete('1.0', tk.END)
        self.details_text.config(state='disabled')
        self.status_bar.config(text="Готов к анализу")

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')


if __name__ == "__main__":
    root = tk.Tk()
    app = ResizableSentimentApp(root)
    root.mainloop()
