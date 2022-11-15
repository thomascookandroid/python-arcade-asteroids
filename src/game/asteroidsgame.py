import arcade
from typing import *
from src.gameobjects.asteroid import Asteroid
from src.gameobjects.player import Player

SCENE_SPRITE_LIST_PLAYER = "spriteListPlayer"
SCENE_SPRITE_LIST_ASTEROID = "spriteListAsteroid"
COLLISION_TYPE_PLAYER = "player"
COLLISION_TYPE_ASTEROID = "asteroid"
DAMPING = 0.4
GRAVITY = (0, 0)


class AsteroidsGame(arcade.Window):

    def __init__(
        self,
        width,
        height,
        title
    ):
        super().__init__(
            width=width,
            height=height,
            title=title
        )
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.__player: Optional[Player] = None
        self.__asteroids: List[Asteroid] = []
        self.__scene = Optional[arcade.Scene]
        self.__physics_engine = Optional[arcade.PymunkPhysicsEngine]

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, value):
        self.__player = value

    @property
    def asteroids(self):
        return self.__asteroids

    @asteroids.setter
    def asteroids(self, value):
        self.__asteroids = value

    @property
    def asteroid_sprite_list(self):
        return self.scene.get_sprite_list(SCENE_SPRITE_LIST_ASTEROID)

    @property
    def player_sprite_list(self):
        return self.scene.get_sprite_list(SCENE_SPRITE_LIST_PLAYER)

    @property
    def scene(self):
        return self.__scene

    @scene.setter
    def scene(self, value):
        self.__scene = value

    @property
    def physics_engine(self):
        return self.__physics_engine

    @physics_engine.setter
    def physics_engine(self, value):
        self.__physics_engine = value

    def setup(
        self
    ):
        self.scene = arcade.Scene()
        self.scene.add_sprite_list(
            name=SCENE_SPRITE_LIST_PLAYER
        )
        self.scene.add_sprite_list(
            name=SCENE_SPRITE_LIST_ASTEROID
        )
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=DAMPING,
            gravity=GRAVITY
        )
        self.player = Player(
            screen_width=self.width,
            screen_height=self.height,
            physics_engine=self.physics_engine,
            collision_type=COLLISION_TYPE_PLAYER,
            sprite_list=self.player_sprite_list
        )

        self.asteroids = [
            Asteroid(
                screen_width=self.width,
                screen_height=self.height,
                physics_engine=self.physics_engine,
                collision_type=COLLISION_TYPE_ASTEROID,
                sprite_list=self.asteroid_sprite_list
            )
        ]

        def player_asteroid_hit_handler(
            player,
            asteroid,
            arbiter,
            space,
            data
        ):
            # self.kill_player(player)
            self.kill_asteroid(asteroid)
            # self.setup()

        self.physics_engine.add_collision_handler(
            first_type=COLLISION_TYPE_PLAYER,
            second_type=COLLISION_TYPE_ASTEROID,
            post_handler=player_asteroid_hit_handler
        )

    def kill_player(self, player):
        player.kill()
        self.player = None

    def kill_asteroid(self, asteroid):
        asteroid.kill()
        self.asteroids.remove(asteroid)

    def on_key_press(
        self,
        symbol: int,
        modifiers: int
    ):
        if symbol == arcade.key.LEFT:
            if self.player:
                self.player.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            if self.player:
                self.player.right_pressed = True
        elif symbol == arcade.key.UP:
            if self.player:
                self.player.forward_pressed = True

    def on_key_release(
        self,
        symbol: int,
        modifiers: int
    ):
        if symbol == arcade.key.LEFT:
            if self.player:
                self.player.left_pressed = False
        elif symbol == arcade.key.RIGHT:
            if self.player:
                self.player.right_pressed = False
        elif symbol == arcade.key.UP:
            if self.player:
                self.player.forward_pressed = False

    def on_update(
        self,
        delta_time: float
    ):
        if self.player:
            self.player.on_update(delta_time)
        for asteroid in self.asteroids:
            asteroid.on_update(delta_time)
        self.physics_engine.step()

    def on_draw(
        self
    ):
        self.clear()
        self.scene.draw()
