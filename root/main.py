import tkinter as tk
from tkinter import ttk
from ui.validation_tab import create_validation_tab
from ui.calc_tab import create_calc_tab
from ui.biese_tab import create_biese_tab
from ui.mpr_tab import create_mpr_tab

root = tk.Tk()
root.title("Compare Tool")
root.geometry("900x650")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

create_validation_tab(notebook)
create_calc_tab(notebook)
create_biese_tab(notebook)
create_mpr_tab(notebook)

root.mainloop()