#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 02:37:28 2021

@author: student
"""

from itertools import combinations
import random 
import json

class RandomGraph():
    
    def __init__(self, num_V, json_title):
        self.num_V = num_V
        self.json_title = json_title
        
    def generate(self):

        V = [i+1 for i in range(self.num_V)]
        E = list(combinations(V, 2))
        W = random.choices(list(range(5,45)), k=len(E))

        graph = {
            'vertices' : V,
                
            'edges' : E,
            
            'weights' : W       
                
            }

        file = json.dumps(graph)
        with open(self.json_title, 'w') as f:
            f.write(file)
            f.close()
            
        print('Your random graph of size', self.num_V, 'with all possible edges has been generated.')
        

if __name__ == "__main__":
    
    random_graph = RandomGraph(100, 'GraphSize100.json')
    random_graph.generate()