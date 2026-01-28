import arcade
import random

# Set how many rows and columns we will have
ROW_COUNT = 4
COLUMN_COUNT = 4

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 120
HEIGHT = 80

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 8

# Do the math to figure out our screen dimensions
WINDOW_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
WINDOW_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
WINDOW_TITLE = "2048 game"


BOARD_BG = (187, 173, 160)   # #BBADA0
EMPTY_BG = (205, 193, 180)   # #CDC1B4
TEXT_DARK = (119, 110, 101)  # #776E65
TEXT_LIGHT = (249, 246, 242) # #F9F6F2

TILE_BG = {
    2:    (238, 228, 218),   # #EEE4DA
    4:    (237, 224, 200),   # #EDE0C8
    8:    (242, 177, 121),   # #F2B179
    16:   (245, 149,  99),   # #F59563
    32:   (246, 124,  95),   # #F67C5F
    64:   (246,  94,  59),   # #F65E3B
    128:  (237, 207, 114),   # #EDCF72
    256:  (237, 204,  97),   # #EDCC61
    512:  (237, 200,  80),   # #EDC850
    1024: (237, 197,  63),   # #EDC53F
    2048: (237, 194,  46),   # #EDC22E
}


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.grid = [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
        
        # Start the game with two tiles
        self.spawn_tile()
        self.spawn_tile()

        self.background_color = BOARD_BG
        self.grid_sprite_list = arcade.SpriteList()

        # Create background slots
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, color=EMPTY_BG)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)

    def spawn_tile(self):
        """Find an empty spot and place a 2 or 4."""
        empty_slots = [(r, c) for r in range(ROW_COUNT) for c in range(COLUMN_COUNT) if self.grid[r][c] == 0]
        if empty_slots:
            r, c = random.choice(empty_slots)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def slide_and_merge(self, line):
        """The 2048 logic for a single row or column."""
        # 1. Shift everything to the left (remove zeros)
        non_zeros = [v for v in line if v != 0]
        # 2. Merge identical adjacent numbers
        for i in range(len(non_zeros) - 1):
            if non_zeros[i] == non_zeros[i+1]:
                non_zeros[i] *= 2
                non_zeros[i+1] = 0
        # 3. Shift again to close gaps created by merges
        res = [v for v in non_zeros if v != 0]
        # 4. Fill remaining spots with 0
        return res + [0] * (len(line) - len(res))

    def on_key_press(self, key):
        """Handle movement."""
        old_grid = [row[:] for row in self.grid]

        if key in (arcade.key.LEFT, arcade.key.A):
            for r in range(ROW_COUNT):
                self.grid[r] = self.slide_and_merge(self.grid[r])
        
        elif key in (arcade.key.RIGHT, arcade.key.D):
            for r in range(ROW_COUNT):
                self.grid[r] = self.slide_and_merge(self.grid[r][::-1])[::-1]

        elif key in (arcade.key.UP, arcade.key.W):
            for c in range(COLUMN_COUNT):
                col = [self.grid[r][c] for r in range(ROW_COUNT)]
                merged_col = self.slide_and_merge(col[::-1])[::-1]
                for r in range(ROW_COUNT):
                    self.grid[r][c] = merged_col[r]

        elif key in (arcade.key.DOWN, arcade.key.S):
            for c in range(COLUMN_COUNT):
                col = [self.grid[r][c] for r in range(ROW_COUNT)]
                merged_col = self.slide_and_merge(col)
                for r in range(ROW_COUNT):
                    self.grid[r][c] = merged_col[r]

        if self.grid != old_grid:
            self.spawn_tile()

    def on_draw(self):
        self.clear()
        self.grid_sprite_list.draw()

        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                value = self.grid[row][column]
                if value > 0:
                    cx = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                    cy = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                    
                    bg_color = TILE_BG.get(value, BOARD_BG)
                    text_color = TEXT_DARK if value <= 4 else TEXT_LIGHT

                    tile_rect = arcade.rect.XYWH(cx, cy, WIDTH, HEIGHT)
                    arcade.draw_rect_filled(tile_rect, color=bg_color)

                    arcade.draw_text(
                        str(value), x=cx, y=cy, color=text_color,
                        font_size=30, anchor_x="center", anchor_y="center", bold=True
                    )


                    
def main():
    # In Arcade 3.x, ensure the window is initialized correctly
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    
    # Create the GameView
    game = GameView()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()

if __name__ == "__main__":
    main()