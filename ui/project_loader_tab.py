import tkinter as tk
import webbrowser

def create_project_loader_tab(notebook):
    tab = tk.Frame(notebook)
    notebook.add(tab, text="autoCVRT")

    FONT_MAIN = ("Arial", 13)
    FONT_BUTTON = ("Arial", 13, "bold")
    FONT_STATUS = ("Arial", 12)

    # --- LOGIC (та сама, тільки всередині) ---

    def validate_input():
        project_id = entry.get().strip()
        if not project_id.isdigit():
            status_label.config(text="Введіть коректний номер!", fg="red")
            return None
        return int(project_id)

    def get_domain(project_id):
        return "dev" if project_id < 100000 else "com.ua"

    def open_project(system):
        project_id = validate_input()
        if project_id is None:
            return

        domain = get_domain(project_id)

        if system == "biese":
            url = f"https://cvrt.kronas.{domain}/api/cix/get?project={project_id}"
            status_label.config(text=f"архів програм .CIX з {domain.upper()} завантажено ✔", fg="green")

        elif system == "mpr":
            url = f"https://cvrt.kronas.{domain}/zipMpr/?projectId={project_id}"
            status_label.config(text=f"архів MPR з {domain.upper()} завантажено ✔", fg="green")

        webbrowser.open(url)

    # ===== UI =====

    label = tk.Label(tab, text="Введіть номер проєкту:", font=FONT_MAIN)
    label.pack(pady=10)

    entry = tk.Entry(tab, width=30, font=FONT_MAIN)
    entry.pack(pady=15)

    button_frame = tk.Frame(tab)
    button_frame.pack(pady=15)

    btn_biese = tk.Button(
        button_frame,
        text=".CIX",
        width=15,
        font=FONT_BUTTON,
        bg="#2b2b2b",
        fg="white",
        activebackground="#1a1a1a",
        activeforeground="white",
        command=lambda: open_project("biese")
    )
    btn_biese.grid(row=0, column=0, padx=10)

    btn_mpr = tk.Button(
        button_frame,
        text="MPR",
        width=15,
        font=FONT_BUTTON,
        bg="#1e5eff",
        fg="white",
        activebackground="#1747c7",
        activeforeground="white",
        command=lambda: open_project("mpr")
    )
    btn_mpr.grid(row=0, column=1, padx=10)

    status_label = tk.Label(tab, text="", font=FONT_STATUS)
    status_label.pack(pady=15)