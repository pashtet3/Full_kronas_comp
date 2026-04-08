import tkinter as tk
from tkinter import font

def create_help_tab(notebook):
    tab = tk.Frame(notebook)
    notebook.add(tab, text="Як користуватись?")

    text = tk.Text(tab, wrap="word")
    text.pack(expand=True, fill="both", padx=10, pady=10)

    # --- стилі (теги) ---
    text.tag_configure("title", font=("Arial", 12, "bold"), foreground="blue")
    text.tag_configure("bold", font=("Arial", 11, "bold"))
    text.tag_configure("small", font=("Arial", 10))
    text.tag_configure("red", foreground="red")

    # --- вставка тексту ---
    text.insert("1.0", "Тут буде інструкція з користування даною прогамою\n\n", "title")

    text.insert("end", "1. Валідація:\n", "bold")
    text.insert("end", "- опис...\n\n", "small")

    text.insert("end", "2. Прорахунок:\n", "bold")
    text.insert("end", "- Необхідно створити ", "small")
    text.insert("end", ".json", "red")
    text.insert("end", " файли та зберегти в них еталонний та тестовий Previev на запит /nomenclature3d\n\n", "small")

    text.insert("end", "3. Порівняння BieSe:\n", "bold")
    text.insert("end", "- Для виконання порівняння .cix програм необхідно попередньо викачати архіви BieSe програм (вкладка autoCVRT), ", "small")
    text.insert("end", "видобути .cix файли", "red")
    text.insert("end", " в окрему папку, та прописати шлях до папки, або знайти її через кнопку ''Обрати'')\n\n", "small")

    text.insert("end", "4. MPR порівняння::\n", "bold")
    text.insert("end", "- порівняння програм MPR виконується шляхом завантаження архівів тестового та еталонного проєктів. Попередньо викачати їх можна через вкладку autoCVRT ", "small")

    text.config(state="disabled")