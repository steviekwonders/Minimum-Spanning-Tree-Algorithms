#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 22:30:57 2021

@author: student
"""

import json
import pandas as pd
import time

### ______________________________________________________________________________________________________________________________________________________________________________________________________
### Graph Class for creating graph object which include Kruskals method for obtaining a minimum spanning tree 

class Graph():
    
    def __init__(self, V, E, W):
        # Instantiate list of vertices, edges and edge weights
        self.V = V
        self.E = E
        self.W = W
        
    def sort_ascending(self, E, W):
        # Create a dataframe for the edges and weights, each row being respective edge, weight pair
        edges_df = pd.DataFrame({'edges': E, 'weights': W})
        # Sort the dataframe in ascending order, by weights
        sorted_edges_df = edges_df.sort_values(by=['weights'])  
        
        # Assign the 'edges' and 'weights' columns of dataframe as lists
        sorted_edges = list(sorted_edges_df['edges'])
        sorted_weights = list(sorted_edges_df['weights'])
        
        # Return the list of sorted edges and weights
        return sorted_edges, sorted_weights
    
    def find(self, parent, i):
        # Function shows the parent of a vertex
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])
 
    def union(self, parent, rank, v1, v2):
        # Find the parents of two vertices of an edge
        xroot = self.find(parent, v1)
        yroot = self.find(parent, v2)
     
        # Update the parents based on conditions
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot         
        else:
            parent[yroot] = xroot
            rank[xroot] += 1
    
    def solve_Kruskal(self):
        ## PARAMETERS ________________________________________________________________________________________________________________________
        
        # Obtain list of sorted edges and weights. Corresponding edge and weight will share same index in respective sorted list
        sorted_E, sorted_W = self.sort_ascending(self.E, self.W)
        
        # Instantiate some data needed for main loop of Kruskals
        edges_of_MST = []     # The list to which we will append least cost edges
        N = len(self.V)       # N represents the number of vertices
        
        # Instantiate the parent and rank lists for the vertices
        parent = []           # parent list of each vertex
        rank = []             # rank list of each vertex
        
        for node in range(N):
            parent.append(node)   # parent of each node initially will be itself
            rank.append(0)        # rank of each node will initally all be zero
        
        # Other parameters
        i = 0 
        cost = 0                # Will eventually become sum of edges weights in MST
        
        ## KRUSKALS ALGORITHM ________________________________________________________________________________________________________________________
        # Main Loop that represents Kruskals Algorithm. Will add least cost edges that do not create a cycle
        # until the number of edges is one less that the number of vertices.
        
        begin = time.time()
        
        while len(edges_of_MST) < N - 1:
            
            # Obtain current edge in list of sorted edges, and find parents of the vertices connecting that edge
            e = sorted_E[i]
            x = self.find(parent, self.V.index(e[0]))  
            y = self.find(parent, self.V.index(e[1]))
             
            # Will add the edge as part of MST if it does not create a cycle i.e. if the parents of nodes do not equal
            if x != y:
                edges_of_MST.append(e)
                cost = cost + sorted_W[i]    
                self.union(parent, rank, x, y)
            
            i = i + 1
        
        end = time.time()
        # Output to the user
        print('Order of edges selected by Kruskals Algorithm: ')

        for e in edges_of_MST:
            print('Edge', e[0], '---', e[1], 'with cost', sorted_W[sorted_E.index(e)])   
            
        print('Minimum cost of our MST is ',cost)
        print('Total run time of Kruskals to find MST was', end-begin)

### ______________________________________________________________________________________________________________________________________________________________________________________________________
### Main Program: Will load data from a json file, instantiate graph object with that data, and find the 
### minimum spanning tree using the Graph object's solve_Kruskal method.
       
if __name__ == "__main__":
    
    # Opening JSON file
    f = open('GraphSize100.json',)
     
    # load the json file: graph
    graph = json.load(f)
    
    # Append the vertices from the json and append each to the list vertices 
    vertices = graph['vertices']   
    edges = graph['edges']
    weights = graph['weights']
     
    # Closing file
    f.close()
    
    # Instantiate Graph object and solve MST using Kruskals
    graph = Graph(vertices, edges, weights)
    graph.solve_Kruskal()    

  



