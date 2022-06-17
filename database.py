import numpy
import json

from creature import *

def writeCreatures(creatures, fileName):
    w_list = []
    for c in creatures:
        w_nodes = []
        for node in c.nodes:
            w_nodes.append({"start_pos" : (float(node.start_pos[0]), float(node.start_pos[1])), "friction_coefficient" : node.friction_coefficient, "mass" : node.mass})
        w_muscles = []
        for muscle in c.muscles:
            w_muscles.append({"node_index1" : muscle.node_index1, "node_index2" : muscle.node_index2, "strength" : muscle.strength, "relax_length" : muscle.relax_length, "flexibility" : muscle.flexibility, "switch_times" : int(muscle.switch_times)})
        w_list.append({"nodes" : w_nodes, "muscles" : w_muscles, "fitness" : c.fitness})
   
    text = json.dumps(w_list)
    f = open(fileName, "w")
    f.write(text)
    f.close()

def readCreatures(fileName):
    creatures = []
    f = open(fileName, "r")
    text = f.read()
    f.close()
    
    l = json.loads(text)

    for c in l:
        nodes = []
        for n in c["nodes"]:
            nodes.append(Node(np.array([float(n["start_pos"][0]),float(n["start_pos"][1])]), n["friction_coefficient"], n["mass"]))
        muscles = []
        for m in c["muscles"]:
            muscles.append(Muscle(nodes, m["node_index1"], m["node_index2"], m["strength"], m["relax_length"], m["flexibility"], m["switch_times"]))
            
        new_c = Creature(muscles, nodes)
        new_c.fitness = c["fitness"]
        creatures.append(new_c)
    
    return creatures
