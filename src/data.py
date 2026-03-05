import numpy as np
from math import ceil

from src.customer import Customer

class Data:
    ''' Class representing a CVRPTW instance.'''
    
    def __init__(self, file: str, precision: int = 0):
        self.file = file # Instance file
        self.precision = precision # Distance precision
        
        self.name = '' # Instance name
        self.max_vehicle_number = 0 # Maximum number of vehicles
        self.max_vehicle_number = 0 # Maximum number of vehicles
        self.vehicle_capacity = 0 # Each vehicle capacity
        self.customers: list[Customer] = [] # List of customers
        
        self.depot: Customer = None # Depot customer
        
        self.distances: np.ndarray = None # Distance matrix
    
    def load(self):
        ''' Load an instance from the file '''
        
        with open(self.file, 'r') as file:
            lines = file.readlines()
            
        self.name = lines[0].strip()
        self.max_vehicle_number, self.vehicle_capacity = map(int, lines[4].strip().split())
        
        for i, line in enumerate(lines[9:-1]):
            self.customers.append(Customer(self, *map(int, line.strip().split())))
        
        self.min_vehicle_number = ceil(sum(customer.demand for customer in self.customers) / self.vehicle_capacity)
        
        self.depot = self.customers[0]

        self.distances = np.zeros((len(self.customers), len(self.customers)), dtype=int)            
        for i in range(len(self.customers)):
            for j in range(i + 1, len(self.customers)):
                d = self.distance(self.customers[i].pos, self.customers[j].pos)
                
                self.distances[i][j] = self.distances[j][i] = d
                
        return self

    def distance(self, a: np.ndarray, b: np.ndarray) -> int:
        ''' Calculate the distance between two positions '''
    
        return round(10 ** self.precision * np.linalg.norm(a - b))