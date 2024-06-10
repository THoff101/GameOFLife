import numpy as np
import pygame

def neighbouring(grid, x, y):
    alive = 0
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if grid[i][j] and not (i == x and j == y):
                alive = alive + 1
    return alive

def game_rules(grid, sh, sw):
    grid_copy = initial_arr(sh,sw,10)
    for i in range(1, int(sh/10) - 1):
        for j in range(1, int(sw/10) - 1):
            neighbours = neighbouring(grid, i, j)
            if neighbours > 1:
                if grid[i][j]:
                    if neighbours > 3:
                        grid_copy[i][j] = False
                    else:
                        grid_copy[i][j] = True
                else:
                    if neighbours == 3:
                        grid_copy[i][j] = True
            else:
                grid_copy[i][j] = False
    grid = None
    return grid_copy

def update(win, grid, run, sh, sw, bw, setup_mode):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_SPACE:
                setup_mode = False
        elif event.type == pygame.MOUSEBUTTONDOWN and setup_mode:
            if event.button == 1:  # Left mouse button
                toggle_cell(grid, event.pos, bw)
        elif event.type == pygame.MOUSEMOTION and setup_mode:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button is held
                toggle_cell(grid, event.pos, bw)
    draw_grid(win, grid, sh, sw, bw)
    pygame.display.update()
    return run, setup_mode


def toggle_cell(grid, pos, bw):
    x = pos[0] // bw
    y = pos[1] // bw
    grid[x][y] = not grid[x][y]

def initial_setup(sh, sw):
    pygame.display.init()
    pygame.display.set_caption("LIFE")
    win = pygame.display.set_mode([sh, sw], flags=pygame.RESIZABLE)
    win.fill("white")
    return win

def draw_grid(win, grid, sh, sw, bw):
    win.fill("white")
    for i in range(0, int(sh/10)):
        for j in range(0, int(sw/10)):
            if grid[i][j] == 0:
                pygame.draw.rect(win, "white", ((i*10,j*10), (bw,bw)), width=0)
            else:
                pygame.draw.rect(win, "black", ((i*10,j*10), (bw,bw)), width=0)
            pygame.draw.rect(win, "grey", ((i*10,j*10), (bw,bw)), width=1)


def initial_arr(sh, sw, bw):
    n = int(sh / bw)
    m = int(sw / bw)
    return np.zeros((n, m), dtype=bool)

def main():

    bw = 10
    sh = 1915
    sw = 1015

    delay = 1
    win = initial_setup(sh, sw)
    grid = initial_arr(sh, sw, bw)
    clock = pygame.time.Clock()

    run = True
    setup_mode = True

    while run:
        run, setup_mode = update(win, grid, run, sh, sw, bw, setup_mode)
        if not setup_mode:
            grid = game_rules(grid, sh, sw)
        # clock.tick(1000 / delay)
    pygame.quit()

if __name__ == "__main__":
    main()