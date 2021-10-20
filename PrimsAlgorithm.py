#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 15:53:54 2021

@author: student
"""

import json
import pandas as pd
import random
import time


### ______________________________________________________________________________________________________________________________________________________________________________________________________
### Graph Class for creating graph object which include Prims method for obtaining a minimum spanning tree 

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
    
    def solve_Prims(self):
        ## PARAMETERS ________________________________________________________________________________________________________________________
        
        # Obtain list of sorted edges and weights. Corresponding edge and weight will share same index in respective sorted list
        sorted_E, sorted_W = self.sort_ascending(self.E, self.W)
        
        # Instantiate some data needed for main loop of Kruskals
        edges_of_MST = []               # The list to which we will append least cost edges
        N = len(self.V)                 # N represents the number of vertices
        
        # Instantiate the parent and rank lists for the vertices
        parent = []                  # parent list of each vertex
        rank = []             # rank list of each vertex
    
        for node in range(N):
            parent.append(node)           # parent of each node initially will be itself
            rank.append(0)                # rank of each node will initally all be zero
        
        cost = 0        # Will eventually become sum of edges weights in MST
        
        # Select a random starting vertex and add to list called vertex_set
        starting_vert = random.choice(self.V)
        vertex_set = [starting_vert]           # We will add vertices to this list as new edges added to MST
        print('Starting vertex set:', vertex_set)
        
        begin = time.time()
        
        ## PRIMS ALGORITHM ________________________________________________________________________________________________________________________
        # MAIN LOOP that represents Prims Algorithm. We start with one random vertex and add to a vertex set. We will look for a least 
        # cost edge where one of the endpoints is our random vertex. Add the other endpoint to vertex set. Then continue by looking for 
        # least cost edge where one of the endpoints is in our vertex set. Continue until our MST list has N-1 edges.
        
        while len(edges_of_MST) < N - 1:
            # Reset index to 0 each time, as we will remove edges
            i = 0
            e = sorted_E[i]  # grab first least cost edge
            
            # Iterate through least cost edge list until we find an edge connected to a vertex in our vertex_set
            while set(vertex_set).intersection(set(e)) == set():
                i = i + 1
                e = sorted_E[i]
            
            # Find parents of the vertices of the edge
            x = self.find(parent, self.V.index(e[0]))
            y = self.find(parent, self.V.index(e[1]))
             
            # Will add the edge as part of MST if it does not create a cycle i.e. if the parents of nodes do not equal
            if x != y:
                edges_of_MST.append(e)
                self.union(parent, rank, x, y)
                cost = cost + sorted_W[i]
                if e[0] in vertex_set:
                    vertex_set.append(e[1])
                else:
                    vertex_set.append(e[0])
            
            # Print to user the updated vertex_set
            print('Current vertex set:', vertex_set)
            
            # Remove the edge. It has been added to MST if it did not create a cycle. Still remove if the edge creates cycle.
            sorted_E.remove(e)
            sorted_W.pop(i)     # Remove the associated edge weight of removed edge.
        
        end = time.time()
        
        # Output to user regarding the order of edges added to MST    
        print('\n')
        print('Order of edges selected by PRIMs Algorithm: ')
            
        for e in edges_of_MST:
            print('Edge', e[0], '---', e[1])   
                
        print('Minimum cost of our MST is ',cost)
        print('Total run time of PRIMs to find MST was', end-begin)
### ______________________________________________________________________________________________________________________________________________________________________________________________________
### Main Program: Will load data from a json file, instantiate graph object with that data, and find the 
### minimum spanning tree using the Graph object's solve_Prims method. 

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
    graph.solve_Prims()    

