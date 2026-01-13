import arcade

# --- Helper (optional): if you prefer hex strings ---
def c(hex_str: str) -> arcade.Color:
    return arcade.color_from_hex_string(hex_str)

THEME = {
    # Window / board
    "window_bg": c("#FAF8EF"),   # classic 2048 page background
    "board_bg":  c("#BBADA0"),
    "cell_bg":   c("#CDC1B4"),

    # Text colors
    "text_dark":  c("#776E65"),
    "text_light": c("#F9F6F2"),

    # UI accents (optional)
    "button_bg":  c("#8F7A66"),
    "button_text": c("#F9F6F2"),

    # Tiles
    "tile_bg": {
        2:    c("#EEE4DA"),
        4:    c("#EDE0C8"),
        8:    c("#F2B179"),
        16:   c("#F59563"),
        32:   c("#F67C5F"),
        64:   c("#F65E3B"),
        128:  c("#EDCF72"),
        256:  c("#EDCC61"),
        512:  c("#EDC850"),
        1024: c("#EDC53F"),
        2048: c("#EDC22E"),
    },
}

def tile_text_color(value: int) -> arcade.Color:
    # Like the original: dark text for small tiles, light for 8+
    return THEME["text_dark"] if value in (2, 4) else THEME["text_light"]
