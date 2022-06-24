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

#for i in range(0,1000):
#    creatures.append(generateCreature())

c_num = 535000
writeCreatures(creatures, f"gentest.json")

creatures = readCreatures("gen534.json")

for g in range(535, 1000):
    fits = []
    for c in creatures:
        fitness = 0
        c.reset()
        for t in range(0, 30*15):
            x_shift = c.fitness
            fitness = c.fitness / 10
            
            if np.isnan(fitness):
                fitness = -500
                c.fitness = -500
                break
            
            game_map.tick(x_shift)
            
            c.tick()
    
        if c_num % 100 == 0:
            print(c_num)
        c_num = c_num + 1
        fits.append(fitness)
        
    
    creatures.sort(key=sortFunc, reverse=True)
    for c in creatures:
        print(c.fitness)
    writeCreatures(creatures, f"gen{g}.json")
    creatures = creatures[:500]
    for c in creatures[:500]:
        creatures.append(reproduce(c))
