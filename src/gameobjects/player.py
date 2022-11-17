from typing import Callable

from src.gameobjects.base import Base
from src.textures.textures import *


class Player(Base):

    def __init__(
        self,
        screen_width,
        screen_height,
        center_x,
        center_y,
        physics_engine,
        physics_filter,
        collision_type,
        sprite_list,
        shoot: Callable
    ):
        super().__init__(
            texture_list=[
                textures[TEXTURE_SHIP_NO_THRUST],
                textures[TEXTURE_SHIP_THRUST],
            ],
            center_x=center_x,
            center_y=center_y,
            screen_width=screen_width,
            screen_height=screen_height,
            friction=0.1,
            max_velocity=350,
            thrust_force=350,
            collision_type=collision_type,
            sprite_list=sprite_list,
            physics_engine=physics_engine,
            physics_filter=physics_filter,
            moment=arcade.PymunkPhysicsEngine.DYNAMIC
        )

        self.__forward_pressed = False
        self.__shoot_pressed = False
        self.__left_pressed = False
        self.__right_pressed = False
        self.__frames_since_last_shot = 120
        self.__shoot = shoot

    @property
    def forward_pressed(self):
        return self.__forward_pressed

    @forward_pressed.setter
    def forward_pressed(self, value):
        self.__forward_pressed = value

    @property
    def shoot_pressed(self):
        return self.__shoot_pressed

    @shoot_pressed.setter
    def shoot_pressed(self, value):
        self.__shoot_pressed = value

    @property
    def left_pressed(self):
        return self.__left_pressed

    @left_pressed.setter
    def left_pressed(self, value):
        self.__left_pressed = value

    @property
    def right_pressed(self):
        return self.__right_pressed

    @right_pressed.setter
    def right_pressed(self, value):
        self.__right_pressed = value

    @property
    def can_shoot(self):
        return self.__frames_since_last_shot >= 20

    def on_update(
        self,
        delta_time: float = 1 / 60
    ):
        self.wrap_to_screen()
        self.__frames_since_last_shot += 1
        if self.forward_pressed:
            self.cur_texture_index = textures[TEXTURE_SHIP_THRUST].index
        else:
            self.cur_texture_index = textures[TEXTURE_SHIP_NO_THRUST].index
        self.set_texture(self.cur_texture_index)
        forward_thrust = self.thrust_force if self.forward_pressed else 0
        forward_thrust_vector = (0, forward_thrust)
        self.physics_engine.apply_force(
            sprite=self,
            force=forward_thrust_vector
        )
        angular_velocity = 7 if self.left_pressed else (-7 if self.right_pressed else 0)
        self.physics_body.angular_velocity = angular_velocity
        if self.shoot_pressed:
            if self.can_shoot:
                self.__frames_since_last_shot = 0
                self.__shoot(self)
