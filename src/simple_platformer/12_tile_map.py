"""
Platformer Game

python -m arcade.examples.platform_tutorial.01_open_window
"""
import arcade

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

TILE_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 5

GRAVITY = 1
PLAYER_JUMP_SPEED = 20


class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class to set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.player_list = None
        self.wall_list = None
        self.camera = None
        self.gui_camera = None
        self.coin_list = None
        self.score = 0
        self.score_text = None
        self.scene = None
        self.tile_map = None

        # Load sound
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.ESCAPE:
            self.setup()

        if key == arcade.key.UP or key == arcade.key.W:
            # self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)

        # elif key == arcade.key.DOWN or key == arcade.key.S:
        #     self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released."""

        # if key == arcade.key.UP or key == arcade.key.W:
        #     self.player_sprite.change_y = 0
        # elif key == arcade.key.DOWN or key == arcade.key.S:
        #     self.player_sprite.change_y = 0
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        self.player_texture = arcade.load_texture(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png")

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(
            ":resources:tiled_maps/map.json",
            scaling=TILE_SCALING,
            layer_options=layer_options
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Separate variable that holds the player sprite
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128

        self.scene.add_sprite("Player", self.player_sprite)
        # self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Coins", use_spatial_hash=True)


        # for x in range(0, 1250, 64):
        #     wall = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=TILE_SCALING)
        #     wall.center_x = x
        #     wall.center_y = 32
        #     self.scene.add_sprite("Walls", wall)

        # coordinate_list = [[512, 96], [256, 96], [768, 96]]
        # for coordinate in coordinate_list:
        #     wall = arcade.Sprite(
        #         ":resources:images/tiles/boxCrate_double.png", scale=TILE_SCALING)
        #     wall.position = coordinate
        #     self.scene.add_sprite("Walls", wall)

        # self.wall_list.alpha_normalized = 0.8

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.scene["Platforms"], gravity_constant=GRAVITY
        ) 

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        # Create the coin list
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        coordinate_list = [[512, 300], [256, 300], [768, 300]]
        for coordinate in coordinate_list:
            coin = arcade.Sprite(
                ":resources:images/items/coinGold.png", scale=0.5)
            coin.position = coordinate
            self.scene.add_sprite("Coins", coin)

        # Reset score
        self.score = 0
        self.score_text = arcade.Text(f"Score: {self.score}", x=10, y=WINDOW_HEIGHT - 20, color=arcade.csscolor.WHITE)


    def on_update(self, delta_time):
        self.physics_engine.update()

        self.camera.position = self.player_sprite.position

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score += 75
            self.score_text.text = f"Score: {self.score}"


    def on_draw(self):
        """Render the screen."""

        self.clear()

        self.camera.use()
        # self.player_list.draw()
        # self.wall_list.draw()
        # self.coin_list.draw()
        self.scene.draw()

        self.gui_camera.use()
        self.score_text.draw()


def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()