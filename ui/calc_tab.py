import tkinter as tk
import pyperclip
import json
from tkinter import filedialog, messagebox
from core.calc import compare_calc
from core.io import load_json
from utils.styles import apply_tree_styles, apply_text_styles

def create_calc_tab(notebook):

    tab = tk.Frame(notebook)
    notebook.add(tab, text="Прорахунок")

    tk.Label(tab, text="Еталонний /nomenclature прорахунку:").pack()
    calc_base_entry = tk.Entry(tab, width=100)
    calc_base_entry.pack()

    tk.Button(tab, text="Обрати", command=lambda: choose_calc_base()).pack()
    tk.Button(tab, text="📋 Вставити з буфера(еталон)", command=lambda: paste_baseline()).pack()

    tk.Label(tab, text="/nomenclature проєкту що тестується:").pack()
    calc_current_entry = tk.Entry(tab, width=100)
    calc_current_entry.pack()

    tk.Button(tab, text="Обрати", command=lambda: choose_calc_current()).pack()
    tk.Button(tab, text="📋 Вставити з буфера(тест)", command=lambda: paste_current()).pack()

    tk.Button(tab, text="Порівняти прорахунки",bg="lightblue", command=lambda: run()).pack(pady=5)



    calc_result_text = tk.Text(tab)
    calc_result_text.pack(expand=True, fill="both")

    apply_text_styles(calc_result_text)
    baseline_json = None
    current_json = None
    def choose_calc_base():
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        calc_base_entry.delete(0, tk.END)
        calc_base_entry.insert(0, path)

    def paste_baseline():
        try:
            data = pyperclip.paste()
            json.loads(data)  # перевірка що це валідний JSON
            calc_base_entry.delete(0, tk.END)
            calc_base_entry.insert(0, "📋 nomenclature3d з буфера")
            nonlocal baseline_json
            baseline_json = json.loads(data)
        except Exception:
            messagebox.showerror("Помилка", "Буфер не містить валідний JSON")

    def paste_current():
        try:
            data = pyperclip.paste()
            json.loads(data)
            calc_current_entry.delete(0, tk.END)
            calc_current_entry.insert(0, "📋 nomenclature3d з буфера")
            nonlocal current_json
            current_json = json.loads(data)
        except Exception:
            messagebox.showerror("Помилка", "Буфер не містить валідний JSON")

    def choose_calc_current():
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        calc_current_entry.delete(0, tk.END)
        calc_current_entry.insert(0, path)

    def run():
        try:
            baseline = baseline_json if baseline_json else load_json(calc_base_entry.get())
            current_raw = current_json if current_json else load_json(calc_current_entry.get())

            added, removed, changed = compare_calc(baseline, current_raw)

            calc_result_text.config(state=tk.NORMAL)
            calc_result_text.delete("1.0", tk.END)

            if not added and not removed and not changed:
                calc_result_text.insert(tk.END, "✅ Прорахунок без змін\n")

            if added:
                calc_result_text.insert(tk.END, "🆕 Додані позиції:\n", "added_title")
                for a in added:
                    calc_result_text.insert(
                        tk.END,
                        f"[{a['article']}] qty={a['data']['qty']} price={a['data']['price']} sum={a['data']['sum']}\n",
                        "normal"
                    )

            if removed:
                calc_result_text.insert(tk.END, "\n❌ Видалені позиції:\n", "removed_title")
                for r in removed:
                    calc_result_text.insert(
                        tk.END,
                        f"[{r['article']}] qty={r['data']['qty']} price={r['data']['price']} sum={r['data']['sum']}\n",
                        "normal"
                    )

            if changed:
                calc_result_text.insert(tk.END, "\n⚠️ Змінені позиції:\n", "changed_title")
                for c in changed:
                    calc_result_text.insert(tk.END, f"[{c['article']}] ", "normal")
                    for field, values in c["changes"].items():
                        calc_result_text.insert(
                            tk.END,
                            f"{field}: {values['old']} → {values['new']}  ",
                            "normal"
                        )
                    calc_result_text.insert(tk.END, "\n")

        except Exception as e:
            messagebox.showerror("Помилка", str(e))