class IndexedTexture:

    def __init__(self, texture, index):
        self.__texture = texture
        self.__index = index

    @property
    def texture(self):
        return self.__texture

    @property
    def index(self):
        return self.__index
