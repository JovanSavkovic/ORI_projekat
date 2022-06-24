import pygame
import numpy
import sys

from map import *
from creature import *
from evolution import *
from database import *

pygame.init()

window_height = 900
window_width = 1600


screen = pygame.display.set_mode([window_width, window_height])

def sortFunc(creature):
    return creature.fitness

running = True
game_map = Map()
x_shift = 0
fitness = 0

gen_num = str(sys.argv[1])

print(gen_num)

creatures = readCreatures(f"gen{gen_num}.json")
creatures.sort(key=sortFunc, reverse = True)


creature = creatures[0]
creature.fitness = 0
clock = pygame.time.Clock()
for t in range(0, 30*60):
    clock.tick_busy_loop(30)
    screen.fill((0,204,255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not running:
        break
    
    x_shift = creature.fitness + 200
    fitness = (creature.fitness)
    
    if np.isnan(fitness):
        fitness = 0
    
    game_map.tick(x_shift)
    game_map.render(screen)
    
    creature.tick()
    creature.render(screen, x_shift)
    
    output = 'Fitness: ' + str(round(fitness,2))
    textFitness = pygame.font.Font('font/GothicA1-Black.ttf', 34).render(output, True, (0, 0, 0), (255,255,255))
    textFitnessRect = textFitness.get_rect()
    textFitnessRect.center = (500, 100)

    screen.blit(textFitness, textFitnessRect)
    pygame.display.update()
print(creature.fitness)
pygame.quit()
