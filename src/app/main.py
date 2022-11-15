import arcade
from src.game.asteroidsgame import AsteroidsGame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_TITLE = "Asteroids"


def main():
    asteroids_game = AsteroidsGame(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        SCREEN_TITLE
    )
    asteroids_game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
