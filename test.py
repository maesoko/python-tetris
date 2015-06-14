import pyglet

game_window = pyglet.window.Window(width=640, height=480)

block = pyglet.resource.image("block.png")
BLOCKS = [
    [1, 1],
    [1, 1]
]

@game_window.event
def on_draw():
    for y in range(len(BLOCKS)):
        for x in range(len(BLOCKS[y])):
            if BLOCKS[y][x] == 1:
                block.blit(x * 16, y * 16, 0, width=16, height=16)

pyglet.app.run()