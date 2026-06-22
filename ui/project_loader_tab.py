import tkinter as tk
import webbrowser
from tkinter import messagebox


def create_project_loader_tab(notebook):

    tab = tk.Frame(notebook)
    notebook.add(tab, text="autoCVRT")


    FONT_MAIN = ("Arial", 13)
    FONT_BUTTON = ("Arial", 11, "bold")
    FONT_STATUS = ("Arial", 12)


    # ================= LOGIC =================

    def validate_input():

        project_id = entry.get().strip()

        if not project_id.isdigit():
            status_label.config(
                text="Введіть коректний номер проєкту!",
                fg="red"
            )
            return None

        return project_id


    def open_link(system, environment):

        project_id = validate_input()

        if project_id is None:
            return


        urls = {

            "biese": {

                "com.ua":
                    f"https://cvrt.kronas.com.ua/api/cix/get?project={project_id}",

                "dev":
                    f"https://cvrt.kronas.dev/api/cix/get?project={project_id}",

                "n.dev":
                    f"https://cvrt-n.kronas.dev/api/cix/get?project={project_id}",
            },


            "mpr": {

                "com.ua":
                    f"https://cvrt.kronas.com.ua/zipMpr/?projectId={project_id}",

                "dev":
                    f"https://cvrt.kronas.dev/zipMpr/?projectId={project_id}",

                "n.dev":
                    f"https://cvrt-n.kronas.dev/zipMpr/?projectId={project_id}",
            }

        }


        url = urls[system][environment]


        webbrowser.open(url)


        status_label.config(
            text=f"{system.upper()} завантаження з cvrt-{environment} ✔",
            fg="green"
        )



    # ================= UI =================


    tk.Label(
        tab,
        text="Введіть номер проєкту:",
        font=FONT_MAIN
    ).pack(pady=10)



    entry = tk.Entry(
        tab,
        width=30,
        font=FONT_MAIN
    )

    entry.pack(pady=10)



    # ================= BUTTON AREA =================

    frame = tk.Frame(tab)
    frame.pack(pady=20)


    # дві колонки

    frame_cix = tk.Frame(frame)
    frame_cix.grid(row=0, column=0, padx=20)


    frame_mpr = tk.Frame(frame)
    frame_mpr.grid(row=0, column=1, padx=20)



    # заголовки

    tk.Label(
        frame_cix,
        text=".CIX",
        font=("Arial", 13, "bold")
    ).pack(pady=5)


    tk.Label(
        frame_mpr,
        text="MPR",
        font=("Arial", 13, "bold")
    ).pack(pady=5)


    environments = [
        ("cvrt.com.ua","com.ua"),
        ("cvrt.dev","dev"),
        ("cvrt-N.dev","n.dev")
    ]



    # CIX кнопки

# CIX кнопки вертикально

    for i,(name,env) in enumerate(environments):

        tk.Button(
            frame,
            text=name,
            width=14,
            font=FONT_BUTTON,
            bg="#2b2b2b",
            fg="white",
            command=lambda e=env:
                open_link("biese",e)

        ).grid(
            row=i+1,
            column=0,
            padx=5,
            pady=5
        )



    # MPR кнопки вертикально

    for i,(name,env) in enumerate(environments):

        tk.Button(
            frame,
            text=name,
            width=14,
            font=FONT_BUTTON,
            bg="#1e5eff",
            fg="white",
            command=lambda e=env:
                open_link("mpr",e)

        ).grid(
            row=i+1,
            column=1,
            padx=5,
            pady=5
        )


    status_label = tk.Label(
        tab,
        text="",
        font=FONT_STATUS
    )

    status_label.pack(pady=15)