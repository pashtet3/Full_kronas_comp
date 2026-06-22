import webbrowser
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
    text.insert("1.0", "Інструкції з користування KRONAS_CompareTool4QA\n\n", "title")

    text.insert("end", "    1. Валідація:\n", "bold")
    text.insert("end", "- Необхідно створити ", "small")
    text.insert("end", ".json", "red")
    text.insert("end", " файли та зберегти в них еталонний та тестовий Previev на запит /vs, обрати дані json. Або скопіювати Previev на запит /vs та натиснути кнопку ''Вставити з буфера. Виконати порівняння натиснувши відповідну кнопку'' \n\n", "small")

    text.insert("end", "    2. Прорахунок:\n", "bold")
    text.insert("end", "- Необхідно створити ", "small")
    text.insert("end", ".json", "red")
    text.insert("end", " файли та зберегти в них еталонний та тестовий Previev на запит /nomenclature3d, обрати дані json. Або скопіювати Previev на запит /nomenclature3d та натиснути кнопку ''Вставити з буфера. Виконати порівняння натиснувши відповідну кнопку\n\n", "small")

    text.insert("end", "    3. Порівняння .CIX:\n", "bold")
    text.insert("end", "- Для виконання порівняння .cix програм необхідно попередньо викачати архіви програм (вкладка autoCVRT), ", "small")
    text.insert("end", "видобути .cix файли", "red")
    text.insert("end", " в окрему папку, та прописати шлях до папки, або знайти її через кнопку ''Обрати''\n\n", "small")

    text.insert("end", "    4. MPR порівняння:\n", "bold")
    text.insert("end", "- порівняння програм MPR виконується шляхом завантаження архівів тестового та еталонного проєктів. Попередньо викачати їх можна через вкладку autoCVRT \n\n", "small")
    
    text.insert("end", "    5. autoCVRT:\n", "bold")
    text.insert("end", "- функція autoCVRT дозволяє викачати архіви програм .cix та MPR, необхідно вказати номер проєкту та натиснути на потрібний тип програм. Визначення на якому середовищі знаходиться проєкт відбувається автоматично", "small")

    text.insert("end", "\n\n\n\n\n\n\n\n\n\n\n\n\n\n     © 2026 Kozliuk_P. Всі права захищені.                           ", "small")
    text.tag_configure("link", foreground="blue", underline=True)

    def open_link(event=None):
        webbrowser.open("https://t.me/four_of_a_kind") 

    text.tag_bind("link", "<Button-1>", open_link)
    text.tag_bind("link", "<Enter>", lambda e: text.config(cursor="hand2"))
    text.tag_bind("link", "<Leave>", lambda e: text.config(cursor=""))

    # --- клікабельний текст ---
    text.insert("end", "Зв’язатись з розробником", "link")

    
    text.config(state="disabled")