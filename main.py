import pyglet
import random
from pyglet.gl import *

# VARIABLES
game_settings = {"width": 320, "height": 320}
game_window = pyglet.window.Window(width=game_settings["width"],
                                   height=game_settings["height"],
                                   caption="TETRIS")

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
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if matrix[y][x] == 1:
                    self.image.blit(x=x * self.block_size + pos_x,
                                    y=y * self.block_size + pos_y,
                                    z=0,
                                    width=self.block_size, height=self.block_size)


class Block(AbstractPaint):
    def __init__(self):
        AbstractPaint.__init__(self, block_size=block_settings["block_size"],
                               image=block_settings["image"])
        self.matrix = random.choice(BLOCKS)
        self.x = 0
        self.y = 0
        self.speed = self.block_size

    def draw(self):
        self.paint_matrix(matrix=self.matrix, pos_x=self.x, pos_y=self.y)

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def rotate(self):
        rotated = []
        for x in range(len(self.matrix[0])):
            rotated.append([0] * len(self.matrix[0]))
            for y in range(len(self.matrix)):
                pass
                # rotated[x][len(self.matrix) - y - 1] = self.matrix[y][x]

        # self.matrix = rotated


@game_window.event
def on_draw():
    game_window.clear()
    block.draw()


@game_window.event
def on_key_press(symbol, modifiers):
    from pyglet.window import key

    if symbol == key.LEFT:
        block.move_left()
    elif symbol == key.RIGHT:
        block.move_right()
    elif symbol == key.UP:
        block.rotate()


if __name__ == '__main__':
    block = Block()
    pyglet.app.run()
