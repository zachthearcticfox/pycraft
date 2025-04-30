import pygame, sys, random
import pgu.gui as gui
from cfg import *

class World:
    def __init__(self):
        self.blocks = []
        cx, cy = 0, 0
        for i in range(25):
            for j in range(40):
                self.blocks.append([blocks['none'], j, i])
    
    def save(self, fp='world.pycr'):
        with open(fp, 'w') as save_world:
            save_world.write(f'{self.blocks}')
        
    def load(self, fp='world.pycr'):
        with open(fp, 'r') as load_world:
            self.blocks = eval(f'{load_world.read()}')

class Player:
    def __init__(self):
        self.inventory = {blocks['stone']:16, blocks['grass']:16, blocks['none']:4294967295}
        self.block_equipped = blocks['grass']
        self.position = [0, 0]
        self.health = 5
    
    def switchBlock(self, block):
        self.block_equipped = blocks[block]

pygame.init()

screen = pygame.display.set_mode((1000,625)) # 40x25 blocks
pygame.display.set_caption("pycraft v25.4.30.0 (40x25/1000x625)")
clock = pygame.time.Clock()
world = World()
player = Player()
hud = gui.App()
container = gui.Container(width=1000, height=625)

gvlabel = gui.Label("Pycraft v25.4.30.0")
container.add(gvlabel, 15, 605)

block_stone = gui.Button("Stone")
block_stone.connect(gui.CLICK, lambda: player.switchBlock('stone'))
container.add(block_stone, 900, 590)

block_grass = gui.Button("Grass")
block_grass.connect(gui.CLICK, lambda: player.switchBlock('grass'))
container.add(block_grass, 825, 590)


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

player_rect = pygame.Rect(player.position[0]*25,player.position[1]*25,25,25)

def update_player_rect():
    global player_rect
    player_rect = pygame.Rect(player.position[0]*25,player.position[1]*25,25,25)

hud.init(container)

while True:
    for event in pygame.event.get():
        hud.event(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                grid_x = player.position[0]+1
                grid_y = player.position[1]

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
                player.position[1] -= 1
                print('player position:', player.position)
            elif event.key == pygame.K_s:
                player.position[1] += 1
                print('player position:', player.position)
            elif event.key == pygame.K_a:
                player.position[0] -= 1
                print('player position:', player.position)
            elif event.key == pygame.K_d:
                player.position[0] += 1
                print('player position:', player.position)
            elif event.key == pygame.K_MINUS:
                player.inventory[blocks['stone']] += 1
            elif event.key == pygame.K_EQUALS:
                player.inventory[blocks['grass']] += 1
            elif event.key == pygame.K_LALT:
                world.load()
            elif event.key == pygame.K_LCTRL:
                world.save()

    screen.fill((0, 0, 0))

    update_blockrects()

    clock.tick(60)
    
    if player.position[0] < 0: 
        player.position[0] = 39
    if player.position[0] > 39: 
        player.position[0] = 0
    if player.position[1] < 0: 
        player.position[1] = 22
    if player.position[1] > 22: 
        player.position[1] = 22

    for i in range(len(blockrects)):
        pygame.draw.rect(screen, world.blocks[i][0], blockrects[i])
    
    update_player_rect()
    pygame.draw.rect(screen, (255, 255, 255), player_rect)

    hud.paint(screen)

    pygame.display.flip()