import arcade
from typing import *

from pymunk import ShapeFilter

from src.gameobjects.asteroid import Asteroid
from src.gameobjects.bullet import Bullet
from src.gameobjects.player import Player

SCENE_SPRITE_LIST_PLAYER = "spriteListPlayer"
SCENE_SPRITE_LIST_BULLET = "spriteListBullet"
SCENE_SPRITE_LIST_ASTEROID = "spriteListAsteroid"
COLLISION_TYPE_PLAYER = "player"
COLLISION_TYPE_ASTEROID = "asteroid"
COLLISION_TYPE_BULLET = "bullet"
COLLISION_CATEGORY_PLAYER = 0b100
COLLISION_CATEGORY_BULLET = 0b010
COLLISION_CATEGORY_ASTEROID = 0b001
COLLISION_MASK_PLAYER = 0b001
COLLISION_MASK_BULLET = 0b001
COLLISION_MASK_ASTEROID = 0b110
COLLISION_FILTER_PLAYER = ShapeFilter(
    categories=COLLISION_CATEGORY_PLAYER,
    mask=COLLISION_MASK_PLAYER
)
COLLISION_FILTER_BULLET = ShapeFilter(
    categories=COLLISION_CATEGORY_BULLET,
    mask=COLLISION_MASK_BULLET
)
COLLISION_FILTER_ASTEROID = ShapeFilter(
    categories=COLLISION_CATEGORY_ASTEROID,
    mask=COLLISION_MASK_ASTEROID
)
DAMPING = 0.6
GRAVITY = (0, 0)


class AsteroidsGame(
    arcade.Window
):

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
        arcade.set_background_color(
            arcade.csscolor.BLACK
            )
        self.__player: Optional[Player] = None
        self.__asteroids: List[Asteroid] = []
        self.__bullets: List[Bullet] = []
        self.__scene = Optional[arcade.Scene]
        self.__physics_engine = Optional[arcade.PymunkPhysicsEngine]

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
        self.scene.add_sprite_list(
            name=SCENE_SPRITE_LIST_BULLET
        )
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=DAMPING,
            gravity=GRAVITY
        )

        def on_bullet_timeout(
            bullet
        ):
            self.kill_bullet(bullet)

        def shoot(
            player
        ):
            bullet = Bullet(
                screen_width=self.width,
                screen_height=self.height,
                center_x=player.center_x,
                center_y=player.center_y,
                angle=player.angle,
                physics_engine=self.physics_engine,
                physics_filter=COLLISION_FILTER_BULLET,
                collision_type=COLLISION_TYPE_BULLET,
                sprite_list=self.bullet_sprite_list,
                frames_to_persist=60*3,
                on_timeout=on_bullet_timeout
            )
            self.bullets.append(
                bullet
            )
            return False

        self.player = Player(
            screen_width=self.width,
            screen_height=self.height,
            center_x=self.width / 2,
            center_y=self.height / 2,
            physics_engine=self.physics_engine,
            physics_filter=COLLISION_FILTER_PLAYER,
            collision_type=COLLISION_TYPE_PLAYER,
            sprite_list=self.player_sprite_list,
            shoot=shoot
        )

        self.asteroids = [
            Asteroid(
                screen_width=self.width,
                screen_height=self.height,
                center_x=self.width / 2 - 58,
                center_y=self.height / 2 - 61,
                physics_engine=self.physics_engine,
                physics_filter=COLLISION_FILTER_ASTEROID,
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
            self.kill_player(
                player
            )
            self.kill_asteroid(
                asteroid
            )
            self.setup()

        def bullet_asteroid_hit_handler(
            bullet,
            asteroid,
            arbiter,
            space,
            data
        ):
            self.kill_bullet(
                bullet
            )
            self.kill_asteroid(
                asteroid
            )

        self.physics_engine.add_collision_handler(
            first_type=COLLISION_TYPE_PLAYER,
            second_type=COLLISION_TYPE_ASTEROID,
            post_handler=player_asteroid_hit_handler
        )

        self.physics_engine.add_collision_handler(
            first_type=COLLISION_TYPE_BULLET,
            second_type=COLLISION_TYPE_ASTEROID,
            post_handler=bullet_asteroid_hit_handler
        )

    def kill_player(
        self,
        player
    ):
        player.kill()
        self.player = None

    def kill_asteroid(
        self,
        asteroid
    ):
        asteroid.kill()
        self.asteroids.remove(
            asteroid
        )

    def kill_bullet(
        self,
        bullet
    ):
        bullet.kill()
        self.bullets.remove(
            bullet
        )

    def on_key_press(
        self,
        symbol: int,
        modifiers: int
    ):
        if symbol == arcade.key.A:
            if self.player:
                self.player.left_pressed = True
        elif symbol == arcade.key.D:
            if self.player:
                self.player.right_pressed = True
        elif symbol == arcade.key.W:
            if self.player:
                self.player.forward_pressed = True
        elif symbol == arcade.key.SPACE:
            if self.player:
                self.player.shoot_pressed = True

    def on_key_release(
        self,
        symbol: int,
        modifiers: int
    ):
        if symbol == arcade.key.A:
            if self.player:
                self.player.left_pressed = False
        elif symbol == arcade.key.D:
            if self.player:
                self.player.right_pressed = False
        elif symbol == arcade.key.W:
            if self.player:
                self.player.forward_pressed = False
        elif symbol == arcade.key.SPACE:
            if self.player:
                self.player.shoot_pressed = False

    def on_update(
        self,
        delta_time: float
    ):
        if self.player:
            self.player.on_update(
                delta_time
            )
        for asteroid in self.asteroids:
            asteroid.on_update(
                delta_time
            )
        for bullet in self.bullets:
            bullet.on_update(
                delta_time
            )
        self.physics_engine.step()

    def on_draw(
        self
    ):
        self.clear()
        self.scene.draw(
            pixelated=True
        )

    @property
    def player(
        self
    ):
        return self.__player

    @player.setter
    def player(
        self,
        value
    ):
        self.__player = value

    @property
    def asteroids(
        self
    ):
        return self.__asteroids

    @asteroids.setter
    def asteroids(
        self,
        value
    ):
        self.__asteroids = value

    @property
    def bullets(
        self
    ):
        return self.__bullets

    @bullets.setter
    def bullets(
        self,
        value
    ):
        self.__bullets = value

    @property
    def asteroid_sprite_list(
        self
    ):
        return self.scene.get_sprite_list(
            SCENE_SPRITE_LIST_ASTEROID
        )

    @property
    def player_sprite_list(
        self
    ):
        return self.scene.get_sprite_list(
            SCENE_SPRITE_LIST_PLAYER
        )

    @property
    def bullet_sprite_list(
        self
    ):
        return self.scene.get_sprite_list(
            SCENE_SPRITE_LIST_BULLET
        )

    @property
    def scene(
        self
    ):
        return self.__scene

    @scene.setter
    def scene(
        self,
        value
    ):
        self.__scene = value

    @property
    def physics_engine(
        self
    ):
        return self.__physics_engine

    @physics_engine.setter
    def physics_engine(
        self,
        value
    ):
        self.__physics_engine = value
