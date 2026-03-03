import numpy as np
from math import ceil

from src.customer import Customer
from src.utils import distance

class Data:
    ''' Class representing a CVRPTW instance.'''
    
    def __init__(self, file: str):
        self.file = file # Instance file
        
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
            self.customers.append(Customer(*map(int, line.strip().split())))
        
        self.min_vehicle_number = ceil(sum(customer.demand for customer in self.customers) / self.vehicle_capacity)
        
        self.depot = self.customers[0]

        self.distances = np.zeros((len(self.customers), len(self.customers)), dtype=int)            
        for i in range(len(self.customers)):
            for j in range(i + 1, len(self.customers)):
                self.distances[i][j] = self.distances[j][i] = round(10 * distance(self.customers[i].pos, self.customers[j].pos))
                
        return self