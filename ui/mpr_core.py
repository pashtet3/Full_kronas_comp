import os
import zipfile
import tempfile
import difflib
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from tkinter.font import Font
from tkinter import filedialog
import re
import subprocess

def run_kronas_import(self):
    file_path = filedialog.askopenfilename(title="Оберіть файл для імпорту на Кронас")
    if not file_path:
        return
    subprocess.Popen(["python", "import_to_kronas.py", file_path])

def extract_number(filename):
    match = re.match(r"(\d+)_", filename)
    if match:
        return int(match.group(1))
    else:
        return float('inf')  # Якщо число не знайдено, кладемо в кінець

def resolve_folder_path(path):
    path = path.strip('{}').strip('"')  # очищення від дужок/лапок

    if path.lower().endswith('.zip') and zipfile.is_zipfile(path):
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Шукаємо вкладену папку 'venture'
        for root, dirs, _ in os.walk(temp_dir):
            if os.path.basename(root).lower() == 'venture':
                return root  # Повертаємо шлях до 'venture'
        
        # Якщо не знайдено
        raise Exception("У ZIP-файлі не знайдено папку 'venture'")
    
    elif os.path.isdir(path):
        return path

    else:
        raise Exception("Недійсний шлях: має бути папка або .zip")

def read_file_lines(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.readlines()

def compare_files_diff(file1, file2):
    lines1 = [line.strip() for line in read_file_lines(file1) if line.strip()]
    lines2 = [line.strip() for line in read_file_lines(file2) if line.strip()]
    
    diff = list(difflib.unified_diff(
        lines1, lines2,
        fromfile=os.path.basename(file1),
        tofile=os.path.basename(file2),
        lineterm=''  # щоб не було подвоєних переносів
    ))
    return diff

def analyze_diff(diff):

    added = removed = changed = 0
    preview = []
    max_preview_lines = 100  # обмеження для попереднього перегляду

    for line in diff[:max_preview_lines]:
        if line.startswith('+') and not line.startswith('+++'):
            added += 1
        elif line.startswith('-') and not line.startswith('---'):
            removed += 1
        preview.append(line.rstrip('\n'))

    total_changes = added + removed + changed
    return total_changes, added, removed, changed, preview

# --- GUI клас ---

class MPRComparerApp:
    def __init__(self, root):
        self.root = root
        if isinstance(self.root, tk.Tk):
            self.root.title("Порівняння .mpr файлів — Розширена версія")
            self.root.geometry("1000x700")

        # Стилі для кольорів рядків в Treeview
        style = ttk.Style(self.root)
        style.configure("Treeview", font=("Consolas", 10))
        style.map("Treeview", background=[('selected', '#347083')], foreground=[('selected', 'white')])
        style.configure("green.Treeview", foreground="green")
        style.configure("orange.Treeview", foreground="orange")
        style.configure("red.Treeview", foreground="red")

        # Шрифт для превʼю diff
        self.diff_font = Font(family="Consolas", size=10)

        # Верхня панель: вибір папок
        frame_top = tk.Frame(root)
        frame_top.pack(fill='x', padx=10, pady=5)

        self.create_folder_selector(frame_top, "Архів Еталонних МПР:", "etalon", 0)
        self.create_folder_selector(frame_top, "Архів Тестових МПР:", "new", 1)

        # Фільтри і пошук
        frame_filter = tk.Frame(root)
        frame_filter.pack(fill='x', padx=10, pady=5)

        self.var_only_diff = tk.BooleanVar(value=False)
        cb_only_diff = tk.Checkbutton(frame_filter, text="Показувати лише файли з відмінностями", variable=self.var_only_diff, command=self.apply_filters)
        cb_only_diff.pack(side='left')

        tk.Label(frame_filter, text="Пошук файлу:").pack(side='left', padx=(20,5))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.apply_filters())
        entry_search = tk.Entry(frame_filter, textvariable=self.search_var, width=30)
        entry_search.pack(side='left')

        # Кнопка Порівняти
        btn_compare = tk.Button(frame_filter, text="Порівняти", command=self.on_compare, bg="lightblue", width=12, height=2)
        btn_compare.pack(side='right', padx=10, pady=5)

        # Нижня панель - Treeview і превʼю
        frame_bottom = tk.PanedWindow(root, sashrelief='sunken', sashwidth=8, orient=tk.HORIZONTAL)
        frame_bottom.pack(fill='both', expand=True, padx=10, pady=10)

        # Список файлів
        self.tree = ttk.Treeview(frame_bottom, columns=("file", "status", "changes"), show='headings', selectmode='browse', height=20)
        self.tree.heading("file", text="Файл")
        self.tree.heading("status", text="Статус")
        self.tree.heading("changes", text="Кількість змін")
        self.tree.column("file", width=200, anchor='w')
        self.tree.column("status", width=170, anchor='center')
        self.tree.column("changes", width=100, anchor='center')

        # Прив’язка вибору файлу
        self.tree.bind("<<TreeviewSelect>>", self.on_file_selected)

        frame_bottom.add(self.tree)

        # Превʼю змін
        self.diff_preview = scrolledtext.ScrolledText(frame_bottom, width=80, font=self.diff_font)
        self.diff_preview.pack(fill='both', expand=True, side='left')
        frame_bottom.add(self.diff_preview)

        # Кнопки збереження звіту
        frame_save = tk.Frame(root)
        frame_save.pack(fill='x', padx=10, pady=(0,10))

        btn_save_html = tk.Button(frame_save, text="Зберегти звіт у HTML", command=self.save_report_html)
        btn_save_html.pack(side='left', padx=10)

        # Змінні для даних
        self.files_data = {}  # filename -> dict з info та diff
        self.filtered_files = []

    def create_folder_selector(self, parent, label_text, attr_name, row):
        lbl = tk.Label(parent, text=label_text)
        lbl.grid(row=row, column=0, sticky='w', padx=(0,5), pady=3)

        path_var = tk.StringVar()
        entry = tk.Entry(parent, textvariable=path_var, width=70)
        entry.grid(row=row, column=1, sticky='we', pady=3)
        setattr(self, f"{attr_name}_entry", entry)


        btn = tk.Button(parent, text="Огляд", command=lambda: self.select_folder(entry), width=12, height=2)
        btn.grid(row=row, column=2, padx=10, pady=5)

        entry.config(font=("Consolas", 9))
        parent.grid_columnconfigure(1, weight=1)

    def on_drop_folder(self, event, entry):
        # Drag & drop не працює в tkinter «з коробки» дуже просто,
        # потрібні додаткові бібліотеки (tkdnd) - тому поки пропускаємо.
        # Залишаю заглушку на майбутнє.
        pass

    def select_folder(self, entry):
        path = filedialog.askopenfilename(
            title="Оберіть папку або ZIP-файл",
            filetypes=[
                ("Папка або ZIP", "*.zip"),
                ("Всі файли", "*.*")
            ]
        )
        # Якщо користувач вибрав не ZIP, а папку, перевіримо вручну
        if path and not path.lower().endswith(".zip") and not os.path.isdir(path):
            messagebox.showerror("Помилка", "Оберіть папку або ZIP-файл.")
            return

        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def on_compare(self):
        try:
            folder1 = resolve_folder_path(self.etalon_entry.get())
            folder2 = resolve_folder_path(self.new_entry.get())
        except Exception as e:
            messagebox.showerror("Помилка шляху", str(e))
            return

        # Скануємо файли
        files1 = [f for f in os.listdir(folder1) if f.endswith('.mpr')]
        files1.sort(key=extract_number)

        files2 = [f for f in os.listdir(folder2) if f.endswith('.mpr')]
        files2.sort(key=extract_number)

        common = list(set(files1) & set(files2))
        missing = list(set(files1) - set(files2))
        extra = list(set(files2) - set(files1))

        self.files_data.clear()
        self.tree.delete(*self.tree.get_children())
        self.diff_preview.delete(1.0, tk.END)

        # Записуємо відсутні файли
        for f in missing:
            # missing — файли, які є у еталонній, але немає у новій
            self.files_data[f] = {
                'status': 'Відсутній у новій папці',
                'changes': 0,
                'diff': [],
                'paths': (os.path.join(folder1, f), None)
            }
        for f in extra:
            # extra — файли, які є у новій, але немає у еталонній
            self.files_data[f] = {
                'status': 'Відсутній в еталоні',
                'changes': 0,
                'diff': [],
                'paths': (None, os.path.join(folder2, f))
            }

        # Порівнюємо спільні файли
        for f in common:
            p1 = os.path.join(folder1, f)
            p2 = os.path.join(folder2, f)
            diff = compare_files_diff(p1, p2)
            total, added, removed, changed, preview = analyze_diff(diff)
            status = "Ідентичний" if total == 0 else "Змінений"
            self.files_data[f] = {
                'status': status,
                'changes': total,
                'diff': diff,
                'preview': preview,
                'paths': (p1, p2)
            }

        self.apply_filters()

    def apply_filters(self):
        # Очищуємо
        self.tree.delete(*self.tree.get_children())
        self.diff_preview.delete(1.0, tk.END)

        show_only_diff = self.var_only_diff.get()
        search_text = self.search_var.get().lower()

        self.filtered_files = []

        for fname, data in sorted(self.files_data.items()):
            if show_only_diff and data['status'] == 'Ідентичний':
                continue
            if search_text and search_text not in fname.lower():
                continue

            self.filtered_files.append(fname)
            status = data['status']
            changes = data['changes']

            # Визначаємо стиль по статусу
            if status == "Ідентичний":
                tag = "green"
            elif status == "Змінений":
                tag = "red"
            else:
                tag = "orange"

            self.tree.insert("", tk.END, iid=fname, values=(fname, status, changes), tags=(tag,))

        # Встановлюємо кольори
        self.tree.tag_configure("green", foreground="green")
        self.tree.tag_configure("red", foreground="red")
        self.tree.tag_configure("orange", foreground="orange")

    def on_file_selected(self, event):
        self.diff_preview.delete(1.0, tk.END)
        sel = self.tree.selection()
        if not sel:
            return
        fname = sel[0]
        data = self.files_data.get(fname)
        if not data:
            return

        if data['status'] in ("Відсутній", "Новий"):
            self.diff_preview.insert(tk.END, f"Файл {fname} {data['status'].lower()} у порівнянні.\n")
            return

        diff = data.get('diff', [])
        preview = data.get('preview', [])

        # Показуємо повний diff з кольоровим форматуванням
        for line in diff:
            tag = None
            if line.startswith('+') and not line.startswith('+++'):
                tag = "added"
            elif line.startswith('-') and not line.startswith('---'):
                tag = "removed"
            elif line.startswith('?'):
                tag = "changed"

            if tag:
                self.diff_preview.insert(tk.END, line + '\n', tag)
            else:
                self.diff_preview.insert(tk.END, line + '\n')

        # Стилі кольорів diff
        self.diff_preview.tag_config("added", foreground="green")
        self.diff_preview.tag_config("removed", foreground="red")
        self.diff_preview.tag_config("changed", foreground="orange")

        self.diff_preview.see(1)

    def save_report_txt(self):
        if not self.files_data:
            messagebox.showinfo("Інформація", "Спочатку зробіть порівняння.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Текстові файли", "*.txt"), ("Всі файли", "*.*")])
        if not path:
            return

        with open(path, 'w', encoding='utf-8') as f:
            for fname in sorted(self.filtered_files):
                data = self.files_data[fname]
                f.write(f"Файл: {fname}\n")
                f.write(f"Статус: {data['status']}\n")
                f.write(f"Кількість змін: {data['changes']}\n")
                if data['status'] == "Змінений":
                    f.write("Diff:\n")
                    f.writelines(data['diff'])
                f.write("\n\n")

        messagebox.showinfo("Успіх", f"Звіт збережено у:\n{path}")

    def save_report_html(self):
        if not self.files_data:
            messagebox.showinfo("Інформація", "Спочатку зробіть порівняння.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".html",
                                            filetypes=[("HTML файли", "*.html"), ("Всі файли", "*.*")])
        if not path:
            return

        # Простий html звіт з кольорами
        html_header = """<!DOCTYPE html><html lang="uk"><head><meta charset="UTF-8"><title>Звіт порівняння</title>
        <style>
        body { font-family: Consolas, monospace; white-space: pre; }
        .added { color: green; }
        .removed { color: red; }
        .changed { color: orange; }
        .identical { color: green; }
        .new, .missing { color: orange; }
        </style></head><body>"""

        html_footer = "</body></html>"

        with open(path, 'w', encoding='utf-8') as f:
            f.write(html_header)
            for fname in sorted(self.filtered_files):
                data = self.files_data[fname]
                status = data['status']
                f.write(f"<h3>Файл: {fname}</h3>\n")
                f.write(f"<b>Статус:</b> {status}<br>\n")
                f.write(f"<b>Кількість змін:</b> {data['changes']}<br>\n")
                if status == "Змінений":
                    f.write("<pre>")
                    for line in data['diff']:
                        cls = ""
                        if line.startswith('+ '):
                            cls = "added"
                        elif line.startswith('- '):
                            cls = "removed"
                        elif line.startswith('? '):
                            cls = "changed"
                        line_html = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        if cls:
                            f.write(f'<span class="{cls}">{line_html}</span>\n')
                        else:
                            f.write(line_html + "\n")
                    f.write("</pre>\n")
                f.write("<hr>\n")
            f.write(html_footer)

        messagebox.showinfo("Успіх", f"HTML звіт збережено у:\n{path}")

