from typing import Optional
from arcade import Sprite, PymunkPhysicsEngine
from pymunk import Body


class Base(Sprite):

    def __init__(
        self,
        texture_list,
        center_x,
        center_y,
        screen_width,
        screen_height,
        friction,
        max_velocity,
        thrust_force,
        collision_type,
        physics_engine,
        physics_filter,
        sprite_list,
        moment: Optional[float] = None,
        body_type: int = Body.DYNAMIC,
        angle: float = 0,
        scale: float = 1
    ):
        super().__init__(
            scale=scale,
            center_x=center_x,
            center_y=center_y,
            angle=angle
        )
        self.textures = [indexed_texture.texture for indexed_texture in texture_list]
        self.set_texture(self.cur_texture_index)
        physics_engine.add_sprite(
            sprite=self,
            friction=friction,
            moment=moment,
            max_velocity=max_velocity,
            collision_type=collision_type,
            body_type=body_type
        )
        for shape in self.physics_body.shapes:
            shape.filter = physics_filter
        sprite_list.append(
            sprite=self
        )
        self.__screen_width = screen_width
        self.__screen_height = screen_height
        self.__friction = friction
        self.__max_velocity = max_velocity
        self.__thrust_force = thrust_force
        self.__collision_type = collision_type
        self.__moment = moment
        self.__body_type = body_type
        self.__sprite_list = sprite_list

    @property
    def _physics_engine(self) -> PymunkPhysicsEngine:
        return self.physics_engines[0]

    @property
    def physics_body(self) -> Body:
        return self._physics_engine.get_physics_object(
            sprite=self
        ).body

    @property
    def current_velocity(self):
        return self.physics_body.velocity.length

    @property
    def thrust_force(self):
        return self.__thrust_force

    def wrap_to_screen(self):
        if self.right < - self.width:
            self.physics_body.position = (self.__screen_width, self.physics_body.position.y)
        if self.left > self.__screen_width + self.width:
            self.physics_body.position = (0, self.physics_body.position.y)
        if self.bottom < - self.height:
            self.physics_body.position = (self.physics_body.position.x, self.__screen_height)
        if self.top > self.__screen_height + self.height:
            self.physics_body.position = (self.physics_body.position.x, 0)
