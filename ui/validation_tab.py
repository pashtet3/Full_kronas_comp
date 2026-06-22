import tkinter as tk
import pyperclip
import json
from tkinter import filedialog, messagebox
from core.validation import normalize_errors, compare_validation
from core.io import load_json
from utils.styles import apply_tree_styles, apply_text_styles

def create_validation_tab(notebook):

    tab = tk.Frame(notebook)
    notebook.add(tab, text="Валідація")

    tk.Label(tab, text="Еталонний /vs:").pack()
    baseline_entry = tk.Entry(tab, width=100)
    baseline_entry.pack()

    tk.Button(tab, text="Обрати", command=lambda: choose_baseline()).pack()
    tk.Button(tab, text="📋 Вставити (еталон) з буфера", command=lambda: paste_baseline()).pack()
    tk.Label(tab, text="/vs проєкту що тестується:").pack()
    current_entry = tk.Entry(tab, width=100)
    current_entry.pack()

    tk.Button(tab, text="Обрати", command=lambda: choose_current()).pack()
    tk.Button(tab, text="📋 Вставити (тест) з буфера", command=lambda: paste_current()).pack()
    tk.Button(tab, text="Порівняти Валідації",bg="lightblue", command=lambda: compare()).pack(pady=5)

    result_text = tk.Text(tab)
    result_text.pack(expand=True, fill="both")

    apply_text_styles(result_text)
    baseline_json = None
    current_json = None
    def choose_baseline():
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        baseline_entry.delete(0, tk.END)
        baseline_entry.insert(0, path)

    def paste_baseline():
        try:
            data = pyperclip.paste()
            json.loads(data)  # перевірка що це валідний JSON
            baseline_entry.delete(0, tk.END)
            baseline_entry.insert(0, "📋 vs з буфера")
            nonlocal baseline_json
            baseline_json = json.loads(data)
        except Exception:
            messagebox.showerror("Помилка", "Буфер не містить валідний JSON")

    def paste_current():
        try:
            data = pyperclip.paste()
            json.loads(data)
            current_entry.delete(0, tk.END)
            current_entry.insert(0, "📋 vs з буфера")
            nonlocal current_json
            current_json = json.loads(data)
        except Exception:
            messagebox.showerror("Помилка", "Буфер не містить валідний JSON")    

    def choose_current():
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        current_entry.delete(0, tk.END)
        current_entry.insert(0, path)

    def compare():
        try:
            baseline = baseline_json if baseline_json else load_json(baseline_entry.get())
            current_raw = current_json if current_json else load_json(current_entry.get())

            baseline = normalize_errors(baseline)
            current = normalize_errors(current_raw)

            added, removed = compare_validation(baseline, current)

            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)

            if not added and not removed:
                result_text.insert(tk.END, "✅ Без змін\n")

            if added:
                result_text.insert(tk.END, "🆕 Нові помилки:\n", "added_title")
                for a in sorted(added, key=lambda x: int(x['detailId'])):
                    err = a["error"]
                    result_text.insert(
                        tk.END,
                        f"[Деталь {int(a['detailId']) + 1}] {err.get('type')} | {err.get('section')} | {err.get('message')}\n",
                        "normal"
                    )

            if removed:
                result_text.insert(tk.END, "\n❌ Зниклі помилки:\n", "removed_title")
                for r in sorted(removed, key=lambda x: int(x['detailId'])):
                    err = r["error"]
                    result_text.insert(
                        tk.END,
                        f"[Деталь {int(r['detailId']) + 1}] {err.get('type')} | {err.get('section')} | {err.get('message')}\n",
                        "normal"
                    )

            result_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Помилка", str(e))