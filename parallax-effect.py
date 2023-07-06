import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(50, arcade.color.BLUE, outer_alpha=255)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

class Layer(arcade.SpriteList):
    def __init__(self, scroll_speed):
        super().__init__()
        self.scroll_speed = scroll_speed

class Platform(arcade.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(width, color, outer_alpha=255)
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE)
        self.player = None
        self.platforms = None
        self.layers = []

    def setup(self):
        self.player = Player()
        self.platforms = arcade.SpriteList()
        gray = arcade.color.GRAY
        red =  arcade.color.RED
        brown = arcade.color.BROWN
        yellow = arcade.color.YELLOW

        w = SCREEN_WIDTH // 2
        h = SCREEN_HEIGHT // 2

        self.platforms.append(Platform(w, h - 100, 200, 20, yellow))

        self.platforms.append(Platform(w, h + 100, 200, 20, yellow))

        layers_data = [
            (Layer(0.2), Platform(w, h, 800, 600, gray)),
            (Layer(0.5), Platform(w, h - 200, 400, 20, red)),
            (Layer(0.5), Platform(w, h + 200, 400, 20, red)),
            (Layer(1.0), Platform(w, h - 300, 200, 20, brown)),
            (Layer(1.0), Platform(w, h + 300, 200, 20, brown))
        ]

        for layer, platform in layers_data:
            layer.append(platform)
            self.layers.append(layer)

    def on_draw(self):
        arcade.start_render()
        for layer in self.layers:
            layer.draw()
        self.platforms.draw()
        self.player.draw()

    def update(self, delta_time):
        self.player.update()
        for layer in self.layers:
            for sprite in layer:
                change = self.player.change_x * layer.scroll_speed
                sprite.center_x -= change

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -5
        elif key == arcade.key.RIGHT:
            self.player.change_x = 5

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
