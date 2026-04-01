TREE_TAGS = {
    "green": {"foreground": "green"},
    "red": {"foreground": "red"},
    "orange": {"foreground": "orange"},
}

TEXT_TAGS = {
    # заголовки (жирні кольорові)
    "added_title": {"foreground": "green", "font": ("Arial", 10, "bold")},
    "removed_title": {"foreground": "red", "font": ("Arial", 10, "bold")},
    "changed_title": {"foreground": "orange", "font": ("Arial", 10, "bold")},

    # звичайний текст
    "normal": {"foreground": "black"},

    # для diff (mpr)
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