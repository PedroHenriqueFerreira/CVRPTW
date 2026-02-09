import numpy as np

class Customer:
    ''' Class representing a customer in the CVRPTW problem.'''
    
    def __init__(
        self, 
        id: int,
        x: int, 
        y: int, 
        demand: int, 
        ready_time: int, 
        due_date: int, 
        service_time: int
    ):
        self.id = id
        self.pos = np.array([x, y])
        self.demand = demand
        self.ready_time = ready_time
        self.due_date = due_date
        self.service_time = service_time
        
    def __repr__(self):
        ''' Return the string representation of the customer '''
        
        return f'Customer({self.id})'