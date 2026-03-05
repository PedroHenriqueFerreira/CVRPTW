from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from src.data import Data

class Customer:
    ''' Class representing a customer in the CVRPTW problem.'''
    
    def __init__(
        self, 
        data: 'Data',
        id: int,
        x: int, 
        y: int, 
        demand: int, 
        ready_time: int, 
        due_date: int, 
        service_time: int
    ):
        self.data = data
        self.id = id
        self.pos = np.array([x, y])
        self.demand = demand
        self.ready_time = 10 ** self.data.precision * ready_time
        self.due_date = 10 ** self.data.precision * due_date
        self.service_time = 10 ** self.data.precision * service_time
        
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