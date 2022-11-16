from typing import Optional
from arcade import Sprite, SpriteList, PymunkPhysicsEngine
from pymunk import Body, ShapeFilter


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
        angle=0
    ):
        super().__init__(
            scale=1,
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
    def screen_width(self):
        return self.__screen_width

    @property
    def screen_height(self):
        return self.__screen_height

    @property
    def physics_engine(self) -> PymunkPhysicsEngine:
        return self.physics_engines[0]

    @property
    def physics_body(self) -> Body:
        return self.physics_engine.get_physics_object(
            sprite=self
        ).body

    @property
    def friction(self):
        return self.__friction

    @property
    def max_velocity(self):
        return self.__max_velocity

    @property
    def thrust_force(self):
        return self.__thrust_force

    @property
    def collision_type(self):
        return self.__collision_type

    @property
    def moment(self):
        return self.__moment

    @property
    def body_type(self):
        return self.__body_type

    @property
    def sprite_list(self) -> SpriteList:
        return self.sprite_lists[0]

    def wrap_to_screen(self):
        if self.right < - self.width:
            self.physics_body.position = (self.screen_width, self.physics_body.position.y)
        if self.left > self.screen_width + self.width:
            self.physics_body.position = (0, self.physics_body.position.y)
        if self.bottom < - self.height:
            self.physics_body.position = (self.physics_body.position.x, self.screen_height)
        if self.top > self.screen_height + self.height:
            self.physics_body.position = (self.physics_body.position.x, 0)
