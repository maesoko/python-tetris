import pyglet
import random

game_window = pyglet.window.Window(width=320, height=320)

block = pyglet.resource.image("block.png")
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


@game_window.event
def on_draw():
    game_window.clear()
    tmp = random.choice(BLOCKS)
    for y in range(len(tmp)):
        for x in range(len(tmp[y])):
            if tmp[y][x] == 1:
                block.blit(x * 16, y * 16, 0, width=16, height=16)


pyglet.app.run()