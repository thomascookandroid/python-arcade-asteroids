from src.gameobjects.base import Base
from src.textures.textures import *


class Bullet(Base):

    def __init__(
        self,
        screen_width,
        screen_height,
        center_x,
        center_y,
        angle,
        physics_engine,
        physics_filter,
        collision_type,
        sprite_list,
        frames_to_persist,
        initial_velocity,
        on_timeout
    ):
        super().__init__(
            texture_list=[
                textures[TEXTURE_BULLET]
            ],
            center_x=center_x,
            center_y=center_y,
            screen_width=screen_width,
            screen_height=screen_height,
            friction=0.1,
            max_velocity=350 + initial_velocity,
            thrust_force=(350 + initial_velocity) * 60,
            collision_type=collision_type,
            sprite_list=sprite_list,
            physics_engine=physics_engine,
            physics_filter=physics_filter,
            moment=arcade.PymunkPhysicsEngine.DYNAMIC,
            angle=angle
        )
        self.__frames_to_persist = frames_to_persist
        self.__on_timeout = on_timeout
        self.__frames_alive = 0

    def on_update(
        self,
        delta_time: float = 1 / 60
    ):
        self.wrap_to_screen()
        self.__frames_alive += 1
        if self.__frames_alive >= self.__frames_to_persist:
            self.__on_timeout(self)
        else:
            forward_thrust = self.thrust_force
            forward_thrust_vector = (0, forward_thrust)
            self.physics_engine.apply_force(
                sprite=self,
                force=forward_thrust_vector
            )
