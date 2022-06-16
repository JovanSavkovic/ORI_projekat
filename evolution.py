import pygame
import numpy as np

from creature import *

min_node_friction = 0
max_node_friction = 1

min_node_mass = 5
max_node_mass = 50

first_node_pos = np.array([350, 500])

min_muscle_strength = 0.1
max_muscle_strength = 5

min_muscle_length = 50
max_muscle_length = 150

min_muscle_flexibility = 5
max_muscle_flexibility = 50

min_switch_time = 0
max_switch_time = 120

min_nodes = 2
max_nodes = 10

def randomFloat(min_val, max_val):
    return (max_val - min_val)*np.random.sample() + min_val


def generateNode(pos):
    friction = randomFloat(min_node_friction, max_node_friction)
    mass = randomFloat(min_node_mass, max_node_mass)
    node = Node(pos, friction, mass)
    return node

def musclePosition(muscle_len):
    theta = np.deg2rad(np.random.randint(0, 360))
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    muscle = np.dot(rot, np.array([muscle_len,0]))
    return muscle

def muscleAlike(muscle, muscles):
    for m in muscles:
        if muscle.node1 == m.node1 and muscle.node2 == m.node2:
            return True
        if muscle.node1 == m.node2 and muscle.node2 == m.node2:
            return True
        return False

def generateMuscle(nodes, muscles):
    muscle_len = randomFloat(min_muscle_length, max_muscle_length)
    muscle_strength = randomFloat(min_muscle_strength, max_muscle_strength)
    muscle_flexibility = randomFloat(min_muscle_flexibility, max_muscle_flexibility)
    
    muscle_switch_times = []
    
    for i in range(np.random.randint(1,3)):
        muscle_switch_times.append(np.random.randint(max_switch_time))
    
    if len(nodes) < 1:
        node1 = generateNode(first_node_pos)
        nodes.append(node1)
        node_index1 = 0
        node2 = generateNode(node1.pos + musclePosition(muscle_len))
        nodes.append(node2)
        node_index2 = 1
    elif len(nodes) < 2:
        node_index1 = 0
        node2 = generateNode(node1.pos + musclePosition(muscle_len))
        nodes.append(node2)
        node_index2 = 1
    else:
        node_index1 = np.random.randint(len(nodes))
        if np.random.randint(max_nodes) > len(nodes):
            node2 = generateNode(nodes[node_index1].pos + musclePosition(muscle_len))
            node_index2 = len(nodes)
            nodes.append(node2)
        else:
            node_index2 = np.random.randint(len(nodes))
    
    muscle = Muscle(nodes, node_index1, node_index2, muscle_strength, muscle_len, muscle_flexibility, muscle_switch_times)
    if muscleAlike(muscle, muscles):
        return
    else:
        muscles.append(muscle)
   
def generateCreature():
    nodes = []
    muscles = []
    for i in range(2, 5):
        generateMuscle(nodes, muscles)
        
    creature = Creature(muscles, nodes)
    return creature

def mutateNode(node):
    new_friction = max(min_node_friction, min(node.friction_coefficient + randomFloat(-0.2, 0.2), max_node_friction))
    new_mass = max(min_node_mass, min(node.mass + randomFloat(-5, 5), max_node_mass))
    new_node = Node(node.pos, new_friction, new_mass)
    return new_node

def mutateMuscle(muscle, nodes):
    new_strength = max(min_muscle_strength, min(muscle.strength + randomFloat(-0.5, 0.5), max_muscle_strength))
    new_length = max(min_muscle_length, min(muscle.relax_length + randomFloat(-10, 10), max_muscle_length))
    new_flexibility = max(min_muscle_flexibility, min(muscle.flexibility + randomFloat(-5, 5), max_muscle_flexibility))
    new_times = []
    for t in muscle.switch_times:
        new_times.append(max(0, min(t + (np.random.randint(10) - 5), max_switch_time)))
    return Muscle(nodes, muscle.node_index1, muscle.node_index2, new_strength, new_length, new_flexibility, new_times)
    
def reproduce(parent):
    nodes = []
    muscles = []
    for n in parent.nodes:
        nodes.append(mutateNode(n))
    for m in parent.muscles:
        muscles.append(mutateMuscle(m, nodes))
        
    if np.random.randint(100) < 1:
        generateMuscle(nodes, muscles)
        
    return Creature(muscles, nodes)
