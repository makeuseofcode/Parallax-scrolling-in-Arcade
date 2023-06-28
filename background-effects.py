import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Layer(arcade.SpriteList):
    def __init__(self, scroll_speed):
        super().__init__()
        self.scroll_speed = scroll_speed

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

class Platform(arcade.Sprite):
    def __init__(self, x, y, width, height,color):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(width, color, outer_alpha=255)
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height
    
class Raindrop(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(30, arcade.color.BLUE, outer_alpha=100)
        self.center_x = x
        self.center_y = y

class BackgroundLayer(arcade.SpriteList):
    def __init__(self, scroll_speed):
        super().__init__()
        self.scroll_speed = scroll_speed
        self.raindrops = arcade.SpriteList()

    def update(self):
        for raindrop in self.raindrops:
            raindrop.center_y -= self.scroll_speed * 5  # Adjust the speed of raindrops
            if raindrop.center_y < -10:
                raindrop.remove_from_sprite_lists()

    def draw(self):
        super().draw()
        self.raindrops.draw()

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE)
        self.background_layer = BackgroundLayer(0.2)
        self.player = None
        self.platforms = None
        self.layers = []

    def setup(self):
        self.player = Player()
        self.platforms = arcade.SpriteList()
        self.background_layer.raindrops.append(Raindrop(SCREEN_WIDTH // 2, SCREEN_HEIGHT + 10))
        self.platforms.append(Platform(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, 200, 20, arcade.color.YELLOW))
        self.platforms.append(Platform(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, 200, 20, arcade.color.YELLOW))

        background_layer = Layer(0.2)
        background_layer.append(Platform(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 800, 600, arcade.color.GRAY))
        self.layers.append(background_layer)

        midground_layer = Layer(0.5)
        midground_layer.append(Platform(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200, 400, 20, arcade.color.RED))
        midground_layer.append(Platform(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200, 400, 20, arcade.color.RED))
        self.layers.append(midground_layer)

        foreground_layer = Layer(1.0)
        foreground_layer.append(Platform(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 300, 200, 20, arcade.color.BROWN))
        foreground_layer.append(Platform(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 300, 200, 20, arcade.color.BROWN))
        self.layers.append(foreground_layer)

    def on_draw(self):
        arcade.start_render()
        for layer in self.layers:
            layer.draw()
        self.background_layer.draw()
        self.platforms.draw()
        self.player.draw()

    def update(self, delta_time):
        self.player.update()
        self.background_layer.update()
        for layer in self.layers:
            for sprite in layer:
                sprite.center_x -= self.player.change_x * layer.scroll_speed

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
