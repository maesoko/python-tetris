import pyglet
import random
from pyglet.gl import *

game_settings = {"width": 320, "height": 320}
game_window = pyglet.window.Window(width=game_settings["width"]
                                   , height=game_settings["height"])

block_settings = {"block_size": 16,
                  "image": pyglet.resource.image("block.png")}

BLOCKS = [
    [
        [1, 1],
        [1, 1]
    ],
    [
        [1, 1],
        [0, 1],
        [0, 1]
    ],
    [
        [1, 1],
        [1, 0],
        [1, 0]
    ],
    [
        [1, 0],
        [1, 1],
        [1, 0]
    ],
    [
        [1, 0],
        [1, 1],
        [0, 1]
    ],
    [
        [0, 1],
        [1, 1],
        [1, 0]
    ],
    [
        [1],
        [1],
        [1],
        [1]
    ]
]


class AbstractPaint:
    def __init__(self, block_size, image):
        self.block_size = block_size
        self.image = image


    def paint_matrix(self, matrix, pos_x, pos_y):
        game_window.clear()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if matrix[y][x] == 1:
                    self.image.blit(x=x * self.block_size + pos_x,
                                    y=y * self.block_size + pos_y,
                                    z=0,
                                    width=self.block_size, height=self.block_size)


class Block(AbstractPaint):
    def __init__(self):
        AbstractPaint.__init__(self, block_size=block_settings["block_size"]
                               , image=block_settings["image"])
        self.matrix = random.choice(BLOCKS)
        # self.paint_matrix(matrix=self.matrix, pos_x=0, pos_y=0)


if __name__ == '__main__':
    Block()
    pyglet.app.run()
