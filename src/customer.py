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
        
    @property
    def x(self):
        ''' Get the x coordinate of the customer '''
        
        return self.pos[0]
    
    @property
    def y(self):
        ''' Get the y coordinate of the customer '''
        
        return self.pos[1]
        
    def __repr__(self):
        ''' Return the string representation of the customer '''
        
        return f'Customer({self.id})'