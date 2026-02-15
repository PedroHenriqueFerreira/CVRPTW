import numpy as np

from networkx import Graph, minimum_spanning_tree

from src.data import Data
from src.route import Route
from src.utils import timer

class KNeighbors:
    ''' Class for the k-nearest neighbors heuristic '''
    
    def __init__(self, data: Data, k: int, routes: list[Route]):  
        self.data = data # CVRPTW instance
        self.k = k # Number of neighbors
        self.routes = routes # Routes list
        
        self.mst: Graph = None # Minimum spanning tree
        
    def load_mst(self):
        ''' Load the minimum spanning tree '''  
        
        graph = Graph()
        for i in range(len(self.data.customers)):
            for j in range(len(self.data.customers)):
                graph.add_edge(i, j, weight=self.data.distances[i, j])
    
        self.mst = minimum_spanning_tree(graph)
        
    def nearest_neighbors_mst(self, customer: int) -> list[int]:
        ''' Get the nearest neighbors from the minimum spanning tree '''
    
        neighbors = list(self.mst.neighbors(customer))
        weights = [self.mst.get_edge_data(customer, i)['weight'] for i in neighbors]
        
        sorted_neighbors = [item for _, item in sorted(zip(weights, neighbors))]
        
        return sorted_neighbors[:self.k]
        
    def nearest_neighbors_mat(self, customer: int):
        ''' Get the nearest neighbors from the distance matrix '''
        
        neighbors = list(range(len(self.data.customers)))
        weights = list(self.data.distances[customer])
        
        sorted_neighbors = [item for _, item in sorted(zip(weights, neighbors)) if item != customer]
        
        return sorted_neighbors[:self.k]
        
    def nearest_neighbors(self, customer: int):
        ''' Get the nearest neighbors '''
        
        neighbors = self.nearest_neighbors_mst(customer)
        
        if len(neighbors) < self.k:
            for neighbor in self.nearest_neighbors_mat(customer):
                if neighbor not in neighbors:
                    neighbors.append(neighbor)
                    
                if len(neighbors) == self.k:
                    break
        
        if len(neighbors) < self.k:
            raise Exception('Cannot find all neighbors')
        
        return neighbors
    
    @timer
    def run(self) -> tuple[float, list[np.ndarray]]:
        ''' Run the k-nearest neighbors heuristic '''
        
        self.load_mst()
        
        matrices: list[np.ndarray] = []
        
        for route in self.routes:
            matrix = np.full((len(self.data.customers), len(self.data.customers)), -1, dtype=int)
            
            for i in range(len(self.data.customers)):
                matrix[i, i] = 0
            
            matrix[0, route[0].id] = matrix[route[0].id, 0] = round(self.data.distances[0, route[0].id])
            matrix[0, route[-1].id] = matrix[route[-1].id, 0] = round(self.data.distances[0, route[-1].id])
            
            for i in range(len(route) - 1):
                distance = round(self.data.distances[route[i].id, route[i + 1].id])
                
                matrix[route[i].id, route[i + 1].id] = matrix[route[i + 1].id, route[i].id] = distance
                
            for customer in route:
                for neighbor in self.nearest_neighbors(customer.id):
                    distance = round(self.data.distances[customer.id, neighbor])
                    matrix[customer.id, neighbor] = matrix[neighbor, customer.id] = distance
            
            matrices.append(matrix)
            
        return matrices