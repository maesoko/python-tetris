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
board_settings = {"board_width": 10, "board_height": 20}
board = [[0 for x in range(board_settings["board_width"])] for y in range(board_settings["board_height"])]

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
        self.x = game_settings["width"] / 4 - self.block_size
        self.y = game_settings["height"] - self.block_size * len(self.matrix)
        self.speed = self.block_size
        self.board_width = board_settings["board_width"]
        self.board_height = board_settings["board_height"]

    def draw(self):
        self.paint_matrix(matrix=self.matrix, pos_x=self.x, pos_y=self.y)

    def move_left(self):
        pos_x = self.x / self.block_size
        pos_y = self.y / self.block_size
        if self.check(board, self.matrix, pos_x - 1, pos_y):
            self.x -= self.speed

    def move_right(self):
        pos_x = self.x / self.block_size
        pos_y = self.y / self.block_size
        if self.check(board, self.matrix, pos_x + 1, pos_y):
            self.x += self.speed

    def move_down(self):
        pos_x = self.x / self.block_size
        pos_y = self.y / self.block_size
        if self.check(board, self.matrix, pos_x, pos_y - 1):
            self.y -= self.speed

    def rotate(self):
        pos_x = self.x / self.block_size
        pos_y = self.y / self.block_size
        rotated = []
        for x in range(len(self.matrix[0])):
            rotated.append([0] * len(self.matrix))
            for y in range(len(self.matrix)):
                rotated[x][len(self.matrix) - y - 1] = self.matrix[y][x]

        if self.check(board, rotated, pos_x, pos_y):
            self.matrix = rotated

    def change_matrix(self):
        self.matrix = random.choice(BLOCKS)

    def auto_drop(self):
        pos_x = self.x / self.block_size
        pos_y = self.y / self.block_size
        if self.check(board, self.matrix, pos_x, pos_y - 1):
            self.y -= self.speed
        else:
            # self.merge_matrix(board, self.matrix, pos_x, pos_y)
            self.reset()

    def reset(self):
        self.change_matrix()
        self.x = game_settings["width"] / 4 - self.block_size
        self.y = game_settings["height"] - self.block_size * len(self.matrix)

    def merge_matrix(self, block_map, matrix, offset_x, offset_y):
        for y in range(self.board_height):
            for x in range(self.board_width):
                if matrix[y + offset_y] and matrix[y + offset_y][x + offset_x]:
                    block_map[y][x] += 1

    def check(self, block_map, matrix, offset_x, offset_y):
        if offset_x < 0 or offset_y < 0 or \
                        self.board_height < offset_y + len(matrix) or \
                        self.board_width < offset_x + len(matrix[0]):
            return False

        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if matrix[y][x] and block_map[y + offset_y][x + offset_x]:
                    return False

        return True


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
    elif symbol == key.DOWN:
        block.move_down()
    elif symbol == key.SPACE:
        block.reset()


def update(dt):
    block.auto_drop()


if __name__ == '__main__':
    block = Block()
    pyglet.clock.schedule_interval(update, 0.5)
    pyglet.app.run()

