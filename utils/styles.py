

TREE_TAGS = {
    "green": {"foreground": "green"},
    "red": {"foreground": "red"},
    "orange": {"foreground": "orange"},
}

TEXT_TAGS = {
    # заголовки (жирні кольорові)
    "added_title": {"foreground": "green", "font": ("Arial", 12, "bold")},
    "removed_title": {"foreground": "red", "font": ("Arial", 12, "bold")},
    "changed_title": {"foreground": "orange", "font": ("Arial", 12, "bold")},

    # звичайний текст
    "normal": {"foreground": "black"},

    # для diff (biese)
    "added": {"foreground": "green"},
    "removed": {"foreground": "red"},
    "changed": {"foreground": "orange"},
}


def apply_tree_styles(tree):
    for tag, cfg in TREE_TAGS.items():
        tree.tag_configure(tag, **cfg)


def apply_text_styles(text_widget):
    for tag, cfg in TEXT_TAGS.items():
        text_widget.tag_config(tag, **cfg)



def apply_light_theme(root):
    style = ttk.Style(root)

    root.configure(bg="#f0f0f0")

    style.theme_use("default")

    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0", foreground="#000000")        