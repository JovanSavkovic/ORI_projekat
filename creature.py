import pygame
import numpy as np

from map import *

gravity = np.array([0, 4])

class Node:
    def __init__(self, start_pos : np.array, friction_coefficient : float, mass : float):
        self.start_pos = start_pos
        self.pos = start_pos
        self.render_pos = start_pos
        self.friction_coefficient = friction_coefficient
        self.mass = mass
        self.map_x = start_pos[0]
        self.velocity = np.array([0,0])
        
        self.muscle_force = np.array([0,0])
        
        self.net_force = np.array([0,0])
        
        self.acc = np.array([0,0])
        
    def onGround(self):
        if self.pos[1] >= ground_y-self.mass-2:
            return True
        else:
            return False
        
    def apply_forces(self):
        if self.onGround():
            friction_force = np.array([-self.friction_coefficient*self.velocity[0], 0])
        else:
            friction_force = np.array([0,0])
        drag_force = -0.1*self.velocity
        
        self.net_force = gravity + friction_force + drag_force + self.muscle_force
        self.muscle_force = 0
        
        
    def move(self):
        self.apply_forces()
        self.accelerate(self.net_force/self.mass)
        self.pos = self.pos + self.velocity
        if self.pos[0] < self.mass:
            self.pos[0] = self.mass
        if self.pos[1]+self.mass > ground_y:
            self.pos[1] = ground_y - self.mass
            
        
    def accelerate(self, acc):
        self.velocity = self.velocity + acc
        
    def tick(self):
        self.move()
    
    def render(self, screen, x_shift):
        if np.isnan(self.pos).any():
            return
        if np.isnan(x_shift):
            return
        self.render_pos[0] = self.pos[0] - x_shift + 800
        self.render_pos[1] = self.pos[1]
        color = self.friction_coefficient*255
        pygame.draw.circle(screen, (color,color,color), self.render_pos, self.mass)
        
class Muscle:
    def __init__(self, nodes, node_index1, node_index2, strength : float, relax_length : float, flexibility : float, switch_times):
        self.node1 = nodes[node_index1]
        self.node_index1 = node_index1
        self.node2 = nodes[node_index2]
        self.node_index2 = node_index2
        self.strength = strength
        self.relax_length = relax_length
        self.flexibility = flexibility
        self.switch_times = switch_times
        
        self.max_length = relax_length + flexibility
        self.min_length = relax_length - flexibility
        
        self.pull = True
        self.push = False
        
        self.time = 0
        
    def tick(self):
        if self.time in self.switch_times :
            if self.pull:
                self.pull = False
                self.push = True
            elif self.push:
                self.pull = True
                self.push = False
        self.time = (self.time + 1)%120

        distance_vector = self.node1.pos - self.node2.pos
        distance = np.sqrt(distance_vector.dot(distance_vector))
        if distance == 0:
            distane = 0.01
        
        target_length = self.relax_length
        if self.pull:
            target_length = self.relax_length - self.flexibility
        if self.push:
            target_length = self.relax_length + self.flexibility 
        
        force = (target_length - distance)*self.strength
        
        
        self.node1.muscle_force = self.node1.muscle_force + force*(distance_vector/distance)
        self.node2.muscle_force = self.node2.muscle_force - force*(distance_vector/distance)
        
        
    def render(self, screen):
        pygame.draw.aaline(screen, (0,0,0), self.node1.render_pos, self.node2.render_pos)
       
       
class Creature:
    def __init__(self, muscles, nodes):
        self.muscles = muscles
        self.nodes = nodes
        self.fitness = 0
        
    def set_fitness(self):
        f = 0.0
        for n in self.nodes:
            f = f + n.pos[0]
        self.fitness = f / len(self.nodes) - 300
    
    def tick(self):
        for m in self.muscles:
            m.tick()
        for n in self.nodes:
            n.tick()
        self.set_fitness()
    
    def render(self, screen, x_shift):
        for m in self.muscles:
            m.render(screen)
        for n in self.nodes:
            n.render(screen, x_shift)
