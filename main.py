import pyglet
import random
from pyglet.gl import *

# VARIABLES
game_settings = {"width": 320, "height": 320}
game_window = pyglet.window.Window(width=game_settings["width"],
                                   height=game_settings["height"],
                                   caption="TETRIS")

block_settings = {"block_size": 16,
                  "image": pyglet.image.load("block.png")}
board_settings = {"board_width": 10, "board_height": 20}
block_map = [[0 for x in range(board_settings["board_width"])] for y in range(board_settings["board_height"])]
background_image = pyglet.image.load("background.png")
batch = pyglet.graphics.Batch()
bg_sprite = pyglet.sprite.Sprite(background_image, game_window.width // 2, 0, batch=batch)

# LABELS
lbl_game_over = pyglet.text.Label('Game over',
                                  color=(200, 200, 200, 200),
                                  font_name='Times New Roman',
                                  font_size=24,
                                  x=game_window.width // 2, y=game_window.height // 2,
                                  anchor_x='center', anchor_y='center')

lbl_next = pyglet.text.Label('NEXT:',
                             color=(0, 0, 0, 255),
                             font_name='Times New Roman',
                             font_size=14,
                             x=game_window.width // 2, y=game_window.height - 30,
                             anchor_x='left', anchor_y='center',
                             batch=batch)

lbl_line = pyglet.text.Label('LINE: ',
                             color=(0, 0, 0, 255),
                             font_name='Times New Roman',
                             font_size=14,
                             x=game_window.width // 2, y=game_window.height - 10,
                             anchor_x='left', anchor_y='center',
                             batch=batch)

lbl_point = pyglet.text.Label('0',
                              color=(0, 0, 0, 255),
                              font_name='Times New Roman',
                              font_size=14,
                              x=lbl_line.x + 50, y=game_window.height - 10,
                              anchor_x='left', anchor_y='center',
                              batch=batch)

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
    def __init__(self, color):
        self.block_size = block_settings["block_size"]
        self.image = block_settings["image"]
        self.color = color

    def paint_matrix(self, matrix, pos_x, pos_y):
        gl.glColor3f(self.color[0], self.color[1], self.color[2])
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if matrix[y][x]:
                    self.image.blit(x=x * self.block_size + pos_x,
                                    y=y * self.block_size + pos_y,
                                    z=0,
                                    width=self.block_size,
                                    height=self.block_size)


class Block(AbstractPaint):
    colors = [[1.0, 0.0, 1.0], [0.4, 0.5, 1.0], [1.0, 0.0, 0.0],
              [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.5, 0.0],
              [0.5, 1.0, 1.0]]

    def __init__(self):
        AbstractPaint.__init__(self, random.choice(self.colors))
        self.matrix = random.choice(BLOCKS)
        self.x = game_settings["width"] // 4 - self.block_size
        self.y = game_settings["height"] - self.block_size * len(self.matrix)
        self.speed = self.block_size
        self.board_width = board_settings["board_width"]
        self.board_height = board_settings["board_height"]
        self.game_over_flg = False

    def draw(self):
        self.paint_matrix(matrix=self.matrix, pos_x=self.x, pos_y=self.y)

    @property
    def pos_x(self):
        return self.x // self.block_size

    @property
    def pos_y(self):
        return self.y // self.block_size

    def move_left(self):
        if self.check(block_map, self.matrix, self.pos_x - 1, self.pos_y):
            self.x -= self.speed

    def move_right(self):
        if self.check(block_map, self.matrix, self.pos_x + 1, self.pos_y):
            self.x += self.speed

    def move_down(self):
        if self.check(block_map, self.matrix, self.pos_x, self.pos_y - 1):
            self.y -= self.speed

    def rotate(self):
        rotated = []
        for x in range(len(self.matrix[0])):
            rotated.append([0] * len(self.matrix))
            for y in range(len(self.matrix)):
                rotated[x][len(self.matrix) - y - 1] = self.matrix[y][x]

        if self.check(block_map, rotated, self.pos_x, self.pos_y):
            self.matrix = rotated

    def change_matrix(self):
        self.matrix = next_block.matrix
        self.color = next_block.color

    def auto_drop(self):
        if self.check(block_map, self.matrix, self.pos_x, self.pos_y - 1):
            self.y -= self.speed
        else:
            if not self.check(block_map, self.matrix, self.pos_x, self.pos_y):
                self.game_over()

            self.merge_matrix(block_map, self.matrix, self.pos_x, self.pos_y)
            self.clear_rows(block_map)
            self.change_matrix()
            self.pos_reset()
            next_block.change_matrix()

    def pos_reset(self):
        self.x = game_settings["width"] // 4 - self.block_size
        self.y = game_settings["height"] - self.block_size * len(self.matrix)

    def merge_matrix(self, board_matrix, matrix, offset_x, offset_y):
        for y in range(self.board_height):
            for x in range(self.board_width):
                try:
                    if matrix[y - offset_y] and matrix[y - offset_y][x - offset_x] and \
                                            x - offset_x >= 0 and y - offset_y >= 0:
                        board_matrix[y][x] += 1
                except IndexError:
                    pass

    def check(self, board_matrix, matrix, offset_x, offset_y):
        if offset_x < 0 or offset_y < 0 or \
                        self.board_height < offset_y + len(matrix) or \
                        self.board_width < offset_x + len(matrix[0]):
            return False

        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if matrix[y][x] and board_matrix[y + offset_y][x + offset_x]:
                    return False

        return True

    def clear_rows(self, board_matrix):
        for y in range(self.board_height):
            full = True
            for x in range(self.board_width):
                if not board_matrix[y][x]:
                    full = False

            if full:
                del board_matrix[y]
                new_row = [0 for i in range(self.board_width)]
                board_matrix.insert(self.board_height - 1, new_row)
                lbl_point.text = str(int(lbl_point.text) + 1)
                self.clear_rows(board_matrix)

    def game_over(self):
        pyglet.clock.unschedule(update)
        self.game_over_flg = True
        self.color = Board.color


class Board(AbstractPaint):
    color = [0.5, 0.5, 0.5]

    def __init__(self):
        AbstractPaint.__init__(self, self.color)

    def draw(self):
        self.paint_matrix(block_map, 0, 0)


class NextBlock(Block):
    def __init__(self):
        Block.__init__(self)
        self.x = lbl_next.x
        self.y = lbl_next.y - 10 - self.block_size * len(self.matrix)

    def change_matrix(self):
        self.matrix = random.choice(BLOCKS)
        self.color = random.choice(self.colors)
        self.y = lbl_next.y - 10 - self.block_size * len(self.matrix)


@game_window.event
def on_draw():
    game_window.clear()
    batch.draw()
    block.draw()
    next_block.draw()
    board.draw()

    if block.game_over_flg:
        lbl_game_over.draw()


@game_window.event
def on_key_press(symbol, modifiers):
    from pyglet.window import key

    if not block.game_over_flg:
        if symbol == key.LEFT:
            block.move_left()
        elif symbol == key.RIGHT:
            block.move_right()
        elif symbol == key.UP:
            block.rotate()
        elif symbol == key.DOWN:
            block.move_down()


def update(dt):
    block.auto_drop()


if __name__ == '__main__':
    block = Block()
    board = Board()
    next_block = NextBlock()
    pyglet.clock.schedule_interval(update, 0.5)
    pyglet.app.run()

