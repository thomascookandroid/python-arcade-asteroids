import arcade
from src.gameobjects.base import Base
from shapely.geometry import box
from src.textures.textures import textures, TEXTURE_ASTEROID


class Asteroid(Base):

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
        max_size,
        angle,
        size
    ):
        super().__init__(
            texture_list=[
                textures[TEXTURE_ASTEROID]
            ],
            center_x=center_x,
            center_y=center_y,
            screen_width=screen_width,
            screen_height=screen_height,
            friction=0.7,
            max_velocity=100,
            thrust_force=100*60,
            collision_type=collision_type,
            body_type=arcade.PymunkPhysicsEngine.DYNAMIC,
            physics_engine=physics_engine,
            physics_filter=physics_filter,
            sprite_list=sprite_list,
            scale=size/max_size
        )
        self.physics_body.angle = angle
        self.__size = size

    def on_update(
        self,
        delta_time: float = 1 / 60
    ):
        self.wrap_to_screen()
        forward_thrust = self.thrust_force
        forward_thrust_vector = (0, forward_thrust)
        self._physics_engine.apply_force(
            sprite=self,
            force=forward_thrust_vector
        )

    @property
    def size(self):
        return self.__size

    @property
    def poly(self):
        return box(self.left, self.top, self.right, self.bottom)
