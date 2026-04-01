import tkinter as tk
from tkinter import filedialog, messagebox
from core.validation import normalize_errors, compare_validation
from core.io import load_json
from utils.styles import apply_styles


def create_validation_tab(notebook):

    tab = tk.Frame(notebook)
    notebook.add(tab, text="Валідація")

    tk.Label(tab, text="Еталонний файл:").pack()
    baseline_entry = tk.Entry(tab, width=100)
    baseline_entry.pack()

    tk.Button(tab, text="Обрати", command=lambda: choose_baseline()).pack()

    tk.Label(tab, text="Тестовий файл:").pack()
    current_entry = tk.Entry(tab, width=100)
    current_entry.pack()

    tk.Button(tab, text="Обрати", command=lambda: choose_current()).pack()

    tk.Button(tab, text="Порівняти", command=lambda: compare()).pack(pady=5)

    result_text = tk.Text(tab)
    result_text.pack(expand=True, fill="both")

    apply_styles(result_text)

    def choose_baseline():
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        baseline_entry.delete(0, tk.END)
        baseline_entry.insert(0, path)

    def choose_current():
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        current_entry.delete(0, tk.END)
        current_entry.insert(0, path)

    def compare():
        try:
            baseline = load_json(baseline_entry.get())
            current_raw = load_json(current_entry.get())
            current = normalize_errors(current_raw)

            added, removed = compare_validation(baseline, current)

            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)

            if not added and not removed:
                result_text.insert(tk.END, "✅ Без змін\n")

            if added:
                result_text.insert(tk.END, "🆕 Нові помилки:\n", "added_title")
                for a in added:
                    err = a["error"]
                    result_text.insert(
                        tk.END,
                        f"[Деталь {a['detailId']}] {err.get('type')} | {err.get('section')} | {err.get('message')}\n",
                        "normal"
                    )

            if removed:
                result_text.insert(tk.END, "\n❌ Зниклі помилки:\n", "removed_title")
                for r in removed:
                    err = r["error"]
                    result_text.insert(
                        tk.END,
                        f"[Деталь {r['detailId']}] {err.get('type')} | {err.get('section')} | {err.get('message')}\n",
                        "normal"
                    )

            result_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Помилка", str(e))