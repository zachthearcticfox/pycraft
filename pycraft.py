import pygame, sys, random
from cfg import *

class World:
    def __init__(self):
        self.blocks = []
        cx, cy = 0, 0
        for i in range(25):
            for j in range(40):
                self.blocks.append([blocks['none'], j, i])

class Player:
    def __init__(self):
        self.inventory = {blocks['stone']:16, blocks['grass']:16, blocks['none']:4294967295}
        self.block_equipped = blocks['grass']
        self.position = [0, 0]

pygame.init()

screen = pygame.display.set_mode((1000,625)) # 40x25 blocks
pygame.display.set_caption("pycraft v25.4.29.0 (40x25/1000x625)")
clock = pygame.time.Clock()
world = World()
player = Player()

blockrects = []
def update_blockrects():
    global blockrects
    blockrects = []
    for i in world.blocks:
        blockrects.append(pygame.Rect(i[1]*25, i[2]*25, 25, 25))

update_blockrects()

for i in range(81):
    if i != 0:
        world.blocks[-i][0] = blocks['grass']
    else: world.blocks[960][0] = blocks['grass']
    update_blockrects()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                grid_x = mx // 25
                grid_y = my // 25

                if player.inventory[player.block_equipped] >= 1:
                    for block in world.blocks:
                        if block[1] == grid_x and block[2] == grid_y:
                            block[0] = player.block_equipped
                            break
                    player.inventory[player.block_equipped] -= 1
                    print(f'placed block{player.block_equipped} at {grid_x}, {grid_y} ({player.inventory[player.block_equipped]})')
                else:
                    print(f'player tried to place block at {grid_x}, {grid_y} but only has {player.inventory[player.block_equipped]} block{player.block_equipped}')

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                player.block_equipped = blocks['stone']
            elif event.key == pygame.K_2:
                player.block_equipped = blocks['grass']
            elif event.key == pygame.K_RALT:
                player.block_equipped = blocks[input('name > ')]
            elif event.key == pygame.K_g:
                give_nm = input('name > ')
                give_am = int(input('amount > '))
                player.inventory[blocks[give_nm]] = give_am
            elif event.key == pygame.K_w:
                player.position[1] += 1
            elif event.key == pygame.K_s:
                player.position[1] -= 1
            elif event.key == pygame.K_a:
                player.position[0] -= 1
            elif event.key == pygame.K_d

    screen.fill((0, 0, 0))

    update_blockrects()

    clock.tick(60)

    for i in range(len(blockrects)):
        pygame.draw.rect(screen, world.blocks[i][0], blockrects[i])

    pygame.display.flip()