import pygame, sys, random
import pgu.gui as gui
from cfg import *
import random

class World:
    def __init__(self):
        self.blocks = []
        self.cave_blocks = []
        for i in range(25):
            for j in range(40):
                self.blocks.append([blocks['none'], j, i])
                self.cave_blocks.append([blocks['stone'], j, i])
    
    def save(self, fp='world.pycr'):
        with open(fp, 'w') as save_world:
            save_world.write(f'{self.blocks}\n{self.cave_blocks}')
        
    def load(self, fp='world.pycr'):
        with open(fp, 'r') as load_world:
            content = load_world.read().splitlines()
            self.blocks = eval(content[0])
            self.cave_blocks = eval(content[1])

class Player:
    def __init__(self):
        self.inventory = {blocks['stone']:0, blocks['grass']:16, blocks['none']:4294967295, blocks['wood_plank']:0, blocks['coal']:0}
        self.block_equipped = blocks['grass']
        self.position = [0, 0]
        self.health = 5
        self.mining_mode = False
        self.in_cave = False
    
    def switchBlock(self, block):
        self.block_equipped = blocks[block]

pygame.init()

screen = pygame.display.set_mode((1000,625)) # 40x25 blocks
pygame.display.set_caption(f"pycraft v{version} (40x25/1000x625)")
clock = pygame.time.Clock()
world = World()
player = Player()
hud = gui.App()
container = gui.Container(width=1000, height=625)

gvlabel = gui.Label(f"Pycraft v{version}")
container.add(gvlabel, 15, 605)

block_stone = gui.Button("Stone")
block_stone.connect(gui.CLICK, lambda: player.switchBlock('stone'))
container.add(block_stone, 900, 590)

block_grass = gui.Button("Grass")
block_grass.connect(gui.CLICK, lambda: player.switchBlock('grass'))
container.add(block_grass, 825, 590)

block_planks = gui.Button("Wood Planks")
block_planks.connect(gui.CLICK, lambda: player.switchBlock('wood_plank'))
container.add(block_planks, 700, 590)

block_coal = gui.Button("Coal")
block_coal.connect(gui.CLICK, lambda: player.switchBlock('coal'))
container.add(block_coal, 640, 590)

blockrects = []
cave_blockrects = []
def update_blockrects():
    global blockrects, cave_blockrects
    blockrects = []
    cave_blockrects = []
    for i in world.blocks:
        blockrects.append(pygame.Rect(i[1]*25, i[2]*25, 25, 25))
    for i in world.cave_blocks:
        cave_blockrects.append(pygame.Rect(i[1]*25, i[2]*25, 25, 25))

for i in world.cave_blocks:
    if random.randint(0, 60) == 1:
        i[0] = blocks['coal']

update_blockrects()

# Grass generation
for i in range(81):
    if i != 0:
        world.blocks[-i][0] = blocks['grass']
    else: world.blocks[960][0] = blocks['grass']
    update_blockrects()

# Tree generation
for i in range(40):
    if random.randint(1,6) == 1:
        world.blocks[i+880][0] = blocks['wood_plank']
        world.blocks[i+840][0] = blocks['wood_plank']
        world.blocks[i+800][0] = blocks['wood_plank']

player_rect = pygame.Rect(player.position[0]*25,player.position[1]*25,25,25)

def update_player_rect():
    global player_rect
    player_rect = pygame.Rect(player.position[0]*25,player.position[1]*25,25,25)

hud.init(container)

while True:
    world_blocks = world.blocks if player.in_cave == False else world.cave_blocks
    for event in pygame.event.get():
        hud.event(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not player.mining_mode:
                grid_x = player.position[0]+1
                grid_y = player.position[1]

                if player.inventory[player.block_equipped] >= 1:
                    for block in world_blocks:
                        if block[1] == grid_x and block[2] == grid_y:
                            block[0] = player.block_equipped
                            break
                    player.inventory[player.block_equipped] -= 1
                    print(f'placed block{player.block_equipped} at {grid_x}, {grid_y} ({player.inventory[player.block_equipped]})')
                else:
                    print(f'player tried to place block at {grid_x}, {grid_y} but only has {player.inventory[player.block_equipped]} block{player.block_equipped}')
            if event.button == 1 and player.mining_mode:
                grid_x = player.position[0]+1
                grid_y = player.position[1]

                for block in world_blocks:
                    if block[1] == grid_x and block[2] == grid_y:
                        if random.randint(0, 6) == 1:
                            player.inventory[block[0]] += 2
                        else:
                            player.inventory[block[0]] += 1
                        print(f'Player now has {player.inventory[block[0]]} block({block[0]})')
                        block[0] = blocks['none']
                        break

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                player.block_equipped = blocks['stone']
            elif event.key == pygame.K_2:
                player.block_equipped = blocks['grass']
            elif event.key == pygame.K_3:
                player.block_equipped = blocks['wood_plank']
            elif event.key == pygame.K_4:
                player.block_equipped = blocks['coal']
            elif event.key == pygame.K_RALT:
                player.block_equipped = blocks[input('name > ')]
            elif event.key == pygame.K_0:
                player.mining_mode = not player.mining_mode
                print('mining:', player.mining_mode)
            elif event.key == pygame.K_g:
                give_nm = input('name > ')
                give_am = int(input('amount > '))
                player.inventory[blocks[give_nm]] = give_am
            elif event.key == pygame.K_c:
                player.in_cave = not player.in_cave
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
        player.position[1] = 24
    if player.position[1] > 22 and not player.in_cave: 
        player.position[1] = 22
    if player.in_cave and player.position[1] > 24:
        player.position[1] = 24

    for i in range(len(blockrects)):
        if not player.in_cave:
            pygame.draw.rect(screen, world.blocks[i][0], blockrects[i])
    for i in range(len(cave_blockrects)):
        if player.in_cave:
            pygame.draw.rect(screen, world.cave_blocks[i][0], cave_blockrects[i])
    
    update_player_rect()
    pygame.draw.rect(screen, (255, 255, 255), player_rect)

    hud.paint(screen)

    pygame.display.flip()