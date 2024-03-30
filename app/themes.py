theme_data = \
    {
        "transparent": {
            "text_col": "#888888",
            "icon_col": (136, 136, 136)
        },
        "dark": {
            "text_col": "#ffffff",
            "background_col": "#0d1117",
            "icon_col": (255, 255, 255)
        },
        "light": {
            "text_col": "#000000",
            "background_col": "#ffffff",
            "icon_col": (0, 0, 0)
        },
        "red": {
            "text_col": "#ffffff",
            "background_col": "#580000",
            "icon_col": (255, 255, 255)
        },
        "blue": {
            "text_col": "#ffffff",
            "background_col": "#000058",
            "icon_col": (255, 255, 255)
        },
        "green": {
            "text_col": "#ffffff",
            "background_col": "#005800",
            "icon_col": (255, 255, 255)
        },
        "gold": {
            "text_col": "#ffffff",
            "background_col": "#ccac00",
            "icon_col": (255, 255, 255)
        },
        "purple": {
            "text_col": "#ffffff",
            "background_col": "#670067",
            "icon_col": (255, 255, 255)
        },
    }


def get_theme(theme_name):
    return theme_data[theme_name]
