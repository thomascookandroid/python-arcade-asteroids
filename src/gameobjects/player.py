import arcade
from src.gameobjects.base import Base


class Player(Base):

    def __init__(
        self,
        screen_width,
        screen_height,
        physics_engine,
        collision_type,
        sprite_list
    ):
        super().__init__(
            image_x=5,
            image_y=1,
            image_width=22,
            image_height=29,
            center_x=screen_width / 2,
            center_y=screen_height / 2,
            screen_width=screen_width,
            screen_height=screen_height,
            friction=0.1,
            max_velocity=700,
            thrust_force=350,
            collision_type=collision_type,
            sprite_list=sprite_list,
            physics_engine=physics_engine,
            moment=arcade.PymunkPhysicsEngine.MOMENT_INF
        )

        self.__forward_pressed = False
        self.__left_pressed = False
        self.__right_pressed = False

    @property
    def forward_pressed(self):
        return self.__forward_pressed

    @forward_pressed.setter
    def forward_pressed(self, value):
        self.__forward_pressed = value

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

    def on_update(
        self,
        delta_time: float = 1 / 60
    ):
        self.wrap_to_screen()
        forward_thrust = self.thrust_force if self.forward_pressed else 0
        forward_thrust_vector = (0, forward_thrust)
        self.physics_engine.apply_force(
            sprite=self,
            force=forward_thrust_vector
        )
        angular_velocity = 10 if self.left_pressed else -10 if self.right_pressed else 0
        self.physics_body.angular_velocity = angular_velocity
