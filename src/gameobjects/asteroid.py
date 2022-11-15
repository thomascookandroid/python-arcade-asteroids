import arcade

from src.gameobjects.base import Base


class Asteroid(Base):

    def __init__(
        self,
        screen_width,
        screen_height,
        physics_engine,
        collision_type,
        sprite_list
    ):
        asteroid_texture = arcade.load_texture(
            file_name="res/sprites/asteroids_sprite_sheet.png",
            x=66,
            y=194,
            width=58,
            height=61
        )
        super().__init__(
            texture_list=[
                asteroid_texture
            ],
            center_x=screen_width / 2 - 58,
            center_y=screen_height / 2 - 61,
            screen_width=screen_width,
            screen_height=screen_height,
            friction=0.7,
            max_velocity=200,
            thrust_force=200*60,
            collision_type=collision_type,
            body_type=arcade.PymunkPhysicsEngine.DYNAMIC,
            physics_engine=physics_engine,
            sprite_list=sprite_list
        )

    def on_update(
        self,
        delta_time: float = 1 / 60
    ):
        self.wrap_to_screen()
        forward_thrust = self.thrust_force
        forward_thrust_vector = (0, forward_thrust)
        self.physics_engine.apply_force(
            sprite=self,
            force=forward_thrust_vector
        )
        angular_velocity = 0
        self.physics_body.angular_velocity = angular_velocity
