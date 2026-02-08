import numpy as np

from src.customer import Customer

class Instance:
    ''' Class representing a CVRPTW instance.'''
    
    def __init__(self, file: str):
        self.file = file # Instance file
        
        self.name = '' # Instance name
        
        self.vehicle_number = 0 # Number of vehicles
        self.vehicle_capacity = 0 # Each vehicle capacity
        
        self.dimension = 0 # Number of customers
        self.edge_weight_type = '' # Edge weight type
        self.edge_weight_format = '' # Edge weight format
        
        self.customers: list[Customer] = [] # List of customers
        self.distances: np.ndarray = None # Distance matrix
    
    def load(self):
        ''' Load an instance from the file '''
        
        with open(self.file, 'r') as file:
            lines = file.readlines()
            
        self.name = lines[0].strip()
        self.vehicle_number, self.vehicle_capacity = map(int, lines[4].strip().split())
            
        for line in lines[9:-1]:
            self.customers.append(Customer(*map(int, line.strip().split())))
            
        self.distances = np.zeros((len(self.customers), len(self.customers)), dtype=int)
            
        for i in range(len(self.customers)):
            for j in range(i + 1, len(self.customers)):
                dx = (self.customers[i].x - self.customers[j].x) ** 2
                dy = (self.customers[i].y - self.customers[j].y) ** 2
                
                distance = np.sqrt(dx + dy)
                
                self.distances[i, j] = self.distances[j, i] = round(distance)
        
        return self