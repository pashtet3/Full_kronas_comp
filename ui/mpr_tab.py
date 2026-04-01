import tkinter as tk
from tkinterdnd2 import TkinterDnD

from ui.mpr_core import MPRComparerApp


def create_mpr_tab(notebook):
    tab = tk.Frame(notebook)
    notebook.add(tab, text="MPR порівняння")

    # контейнер всередині вкладки
    inner = tk.Frame(tab)
    inner.pack(fill="both", expand=True)

    # головне: передаємо FRAME як root
    app = MPRComparerApp(inner)