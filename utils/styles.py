def apply_styles(text_widget):
    text_widget.tag_config("added_title", foreground="green", font=("Arial", 10, "bold"))
    text_widget.tag_config("removed_title", foreground="red", font=("Arial", 10, "bold"))
    text_widget.tag_config("changed_title", foreground="orange", font=("Arial", 10, "bold"))
    text_widget.tag_config("normal", foreground="black")