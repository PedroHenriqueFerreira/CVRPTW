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
        self.vehicle_capacity = 0 # Each vehicle capacity
        self.customers: list[Customer] = [] # List of customers
        
        self.depot: Customer = None # Depot customer
        
        self.min_vehicle_number = 0 # Minimum number of vehicles
        
        self.distances: np.ndarray = None # Distance matrix
    
    def load(self):
        ''' Load an instance from the file '''
        
        with open(self.file, 'r') as file:
            lines = file.readlines()
            
        self.name = lines[0].strip()
        self.max_vehicle_number, self.vehicle_capacity = map(int, lines[4].strip().split())
            
        for line in lines[9:-1]:
            self.customers.append(Customer(*map(int, line.strip().split())))
        
        self.depot = self.customers[0]
        
        self.min_vehicle_number = ceil(sum(c.demand for c in self.customers) / self.vehicle_capacity)
            
        self.distances = np.zeros((len(self.customers), len(self.customers)))
            
        for i, i_customer in enumerate(self.customers):
            for j, j_customer in enumerate(self.customers[i + 1:], start=i + 1):
                self.distances[i, j] = self.distances[j, i] = distance(i_customer.pos, j_customer.pos)
        
        return self