import pygame
import numpy

from map import *
from creature import *
from evolution import *
from database import *

def sortFunc(creature):
    return creature.fitness

game_map = Map()
x_shift = 0
fitness = 0

creatures = []

for i in range(0,1000):
    creatures.append(generateCreature())

c_num = 0
writeCreatures(creatures, f"gentest.json")

for g in range(0, 10):
    fits = []
    for c in creatures:
        fitness = 0
        for t in range(0, 30*15):
            x_shift = c.fitness
            fitness = c.fitness / 10
            
            if np.isnan(fitness):
                fitness = -500
            
            game_map.tick(x_shift)
            
            c.tick()
    
        print(c_num)
        c_num = c_num + 1
        fits.append(fitness)
    
    fits.sort()
    writeCreatures(creatures, f"gen{g}.json")
    print(fits)
    
    creatures.sort(key=sortFunc)
    creatures = creatures[:500]
    for c in creatures[:500]:
        creatures.append(reproduce(c))
