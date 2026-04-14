import tkinter as tk
from tkinter import ttk
from ui.validation_tab import create_validation_tab
from ui.calc_tab import create_calc_tab
from ui.biese_tab import create_biese_tab
from ui.mpr_tab import create_mpr_tab
from ui.help_tab import create_help_tab
from ui.project_loader_tab import create_project_loader_tab

root = tk.Tk()
root.title("KRONAS_CompareTool4QA")
root.geometry("900x650")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

create_validation_tab(notebook)
create_calc_tab(notebook)
create_biese_tab(notebook)
create_mpr_tab(notebook)
create_project_loader_tab(notebook)

create_help_tab(notebook)  # ← ОСТАННЯ, щоб була справа

root.mainloop()