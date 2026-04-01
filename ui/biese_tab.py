import os
import difflib
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from tkinter.font import Font
from utils.styles import apply_tree_styles, apply_text_styles

def create_biese_tab(notebook):
    tab = tk.Frame(notebook)
    notebook.add(tab, text="Порівняння BieSe")
    CIXComparerApp(tab)


class CIXComparerApp:
    def __init__(self, root):
        self.root = root
        self.diff_font = Font(family="Consolas", size=10)

        self.files_data = {}
        self.filtered_files = []

        self.build_ui()

    # ---------------- DIFF ---------------- #

    def read_file_lines(self, filepath):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.readlines()

    def compare_files_diff(self, file1, file2):
        return list(difflib.unified_diff(
            self.read_file_lines(file1),
            self.read_file_lines(file2),
            fromfile=os.path.basename(file1),
            tofile=os.path.basename(file2),
            lineterm=''
        ))

    def analyze_diff(self, diff):
        added = removed = changed = 0

        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                added += 1
            elif line.startswith('-') and not line.startswith('---'):
                removed += 1
            elif line.startswith('?'):
                changed += 1

        return added + removed + changed

    # ---------------- UI ---------------- #

    def build_ui(self):
        frame_top = tk.Frame(self.root)
        frame_top.pack(fill='x', padx=10, pady=5)

        self.create_folder_selector(frame_top, "Папка 1:", "folder1", 0)
        self.create_folder_selector(frame_top, "Папка 2:", "folder2", 1)

        # 🔥 ЧЕКБОКС (повернули)
        self.var_only_diff = tk.BooleanVar(value=False)

        cb = tk.Checkbutton(
            frame_top,
            text="Показувати лише різні файли",
            variable=self.var_only_diff,
            command=self.apply_filters
        )
        cb.grid(row=2, column=0, sticky="w")

        tk.Button(
            frame_top,
            text="Порівняти",
            command=self.on_compare,
            bg="lightblue",
            width=15,
            height=2
        ).grid(row=2, column=1, columnspan=2, pady=10)

        frame_bottom = tk.PanedWindow(self.root, sashrelief='sunken', sashwidth=8)
        frame_bottom.pack(fill='both', expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            frame_bottom,
            columns=("file", "status", "changes"),
            show='headings'
        )
        apply_tree_styles(self.tree)
        self.tree.heading("file", text="Файл")
        self.tree.heading("status", text="Статус")
        self.tree.heading("changes", text="Зміни")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        frame_bottom.add(self.tree)
            
        self.preview = scrolledtext.ScrolledText(frame_bottom, font=self.diff_font)
        frame_bottom.add(self.preview)
        apply_text_styles(self.preview)

    def create_folder_selector(self, parent, label, attr, row):
        tk.Label(parent, text=label).grid(row=row, column=0, sticky='w')

        entry = tk.Entry(parent, width=70)
        entry.grid(row=row, column=1, padx=5)

        setattr(self, attr + "_entry", entry)

        tk.Button(
            parent,
            text="Обрати",
            command=lambda: self.select_folder(entry)
        ).grid(row=row, column=2)

    def select_folder(self, entry):
        path = filedialog.askdirectory()
        entry.delete(0, tk.END)
        entry.insert(0, path)

    # ---------------- LOGIC ---------------- #

    def on_compare(self):
        folder1 = self.folder1_entry.get()
        folder2 = self.folder2_entry.get()

        if not os.path.isdir(folder1) or not os.path.isdir(folder2):
            messagebox.showerror("Помилка", "Оберіть обидві папки")
            return

        files1 = {f: os.path.join(folder1, f)
                  for f in os.listdir(folder1) if f.lower().endswith('.cix')}

        files2 = {f: os.path.join(folder2, f)
                  for f in os.listdir(folder2) if f.lower().endswith('.cix')}

        common = set(files1) & set(files2)
        missing = set(files1) - set(files2)
        extra = set(files2) - set(files1)

        self.files_data.clear()
        self.tree.delete(*self.tree.get_children())
        self.preview.delete(1.0, tk.END)

        for f in missing:
            self.files_data[f] = ("Відсутній у папці 2", 0, None)

        for f in extra:
            self.files_data[f] = ("Відсутній у папці 1", 0, None)

        for f in common:
            diff = self.compare_files_diff(files1[f], files2[f])
            total = self.analyze_diff(diff)

            status = "Ідентичний" if total == 0 else "Змінений"

            self.files_data[f] = (status, total, diff)

        self.apply_filters()

    # ---------------- FILTERS + COLORS ---------------- #

    def apply_filters(self):
        self.tree.delete(*self.tree.get_children())

        only_diff = self.var_only_diff.get()

        for fname, data in self.files_data.items():
            status, changes, diff = data

            if only_diff and status == "Ідентичний":
                continue

            tag = "green" if status == "Ідентичний" else "red"

            self.tree.insert(
                "",
                tk.END,
                iid=fname,
                values=(fname, status, changes),
                tags=(tag,)
            )


    # ---------------- PREVIEW ---------------- #

    def on_select(self, event):
        self.preview.delete(1.0, tk.END)

        sel = self.tree.selection()
        if not sel:
            return

        fname = sel[0]
        data = self.files_data.get(fname)

        if not data:
            return

        status, changes, diff = data

        if diff is None:
            self.preview.insert(tk.END, status)
            return

        for line in diff:
            self.preview.insert(tk.END, line + "\n")