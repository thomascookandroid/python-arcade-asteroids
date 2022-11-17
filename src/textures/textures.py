import arcade

from src.textures.indexedtexture import IndexedTexture

TEXTURE_SHIP_NO_THRUST = "ShipNoThrust"
TEXTURE_SHIP_THRUST = "ShipThrust"
TEXTURE_ASTEROID = "AsteroidTexture"
TEXTURE_BULLET = "Bullet"

textures = {
    TEXTURE_SHIP_NO_THRUST: IndexedTexture(
        texture=arcade.load_texture(
            file_name="res/sprites/asteroids_sprite_sheet.png",
            x=5,
            y=1,
            width=22,
            height=45
        ),
        index=0
    ),
    TEXTURE_SHIP_THRUST: IndexedTexture(
        texture=arcade.load_texture(
            file_name="res/sprites/asteroids_sprite_sheet.png",
            x=34,
            y=1,
            width=22,
            height=45
        ),
        index=1
    ),
    TEXTURE_ASTEROID: IndexedTexture(
        texture=arcade.load_texture(
            file_name="res/sprites/asteroids_sprite_sheet.png",
            x=66,
            y=194,
            width=58,
            height=61
        ),
        index=0
    ),
    TEXTURE_BULLET: IndexedTexture(
        texture=arcade.load_texture(
            file_name="res/sprites/asteroids_sprite_sheet.png",
            x=76,
            y=48,
            width=8,
            height=15
        ),
        index=0
    )
}
