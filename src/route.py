import numpy as np

from src.instance import Instance
from src.customer import Customer

class Route:
    ''' Class for the route '''
    
    def __init__(
        self, 
        instance: Instance, 
        value: list[int],
        pos: np.ndarray | None = None,
        cost: float = -1,
        demand: int = -1,
        time: int = -1,
    ):
        self.instance = instance # CVRPTW instance
        self.value = value # Route list
        
        self.pos = pos # Route position (for clustering)
        
        self._cost = cost # Route cost
        self._demand = demand # Route demand
        self._time = time # Route time (for clustering)
        
    def __repr__(self):
        ''' Return the string representation of the route '''
        
        return f'Route{self.value}'
        
    def __len__(self):
        ''' Get the length of the route '''
        
        return len(self.value)
        
    def __iter__(self):
        ''' Iterate over the route '''
        
        return iter(self.instance.customers[item] for item in self.value)
        
    def __getitem__(self, idx: int) -> Customer:
        ''' Get the customer at the index '''
        
        return self.instance.customers[self.value[idx]]

    def append(self, customer: Customer):
        ''' Append a customer to the end of the route '''
        
        self.value.append((idx := customer.id))
        
        if self._demand >= 0:
            self._demand += customer.demand
            
        if self._cost >= 0:
            if len(self.value) == 1:
                self._cost = self.instance.distances[0, idx] + self.instance.distances[idx, 0]
            else:
                self._cost += self.instance.distances[self.value[-2], idx] 
                self._cost += self.instance.distances[idx, 0]
                self._cost -= self.instance.distances[self.value[-2], 0]
                
        if self._time >= 0:
            if len(self.value) == 1:
                self._time = self.instance.distances[0, idx]
            else:
                self._time += self.instance.distances[self.value[-2], idx]
                
            if self._time > customer.due_date:
                self._time = float('inf')
            else:
                self._time = max(self._time, customer.ready_time) 
                self._time += customer.service_time
    
    def clear(self, pos: np.ndarray | None = None):
        ''' Clear the route '''
        
        self.value.clear()
        
        self.pos = pos
        
        self._cost = 0
        self._demand = 0
        self._time = 0
    
    def reversed(self, i = None, j = None):
        ''' Returns a reversed route on the given indexes '''
        
        value = self.value[:]
        
        value[i:j] = value[i:j][::-1]
        
        # TODO: CHECK
        cost = self._cost
        if self._cost >= 0:
            if i > 0:
                cost -= self.instance.distances[self.value[i - 1], self.value[i]]
                cost += self.instance.distances[self.value[i - 1], self.value[j - 1]]
            
            if j < len(self.value):
                cost -= self.instance.distances[self.value[j - 1], self.value[j]]
                cost += self.instance.distances[self.value[i], self.value[j]]
                
        return Route(self.instance, value, self.pos, cost, self.demand)

    @property
    def x(self):
        ''' Get the x coordinate of the route '''
        
        return self.pos[0]
    
    @property
    def y(self):
        ''' Get the y coordinate of the route '''
        
        return self.pos[1]

    @property
    def cost(self):
        ''' Get the route cost '''
        
        if self._cost < 0:
            self._cost = self.calculate_cost()
        
        return self._cost
    
    @property
    def demand(self):
        ''' Get the route demand '''
        
        if self._demand < 0:
            self._demand = self.calculate_demand()
        
        return self._demand
        
    @property
    def time(self):
        ''' Get the route time '''
        
        if self._time is None:
            self._time = self.calculate_time()
        
        return self._time
        
    def calculate_cost(self):
        ''' Calculate the cost for the route '''
        
        if not self.value:
            return 0
        
        cost = self.instance.distances[0, self.value[0]] + self.instance.distances[self.value[-1], 0]
        
        for i in range(len(self.value) - 1):
            cost += self.instance.distances[self.value[i], self.value[i + 1]]
        
        return cost
    
    def calculate_demand(self):
        ''' Calculate the demand for the route '''
        
        return sum(self.instance.customers[c].demand for c in self.value)
    
    def calculate_time(self):
        ''' Calculate the time for the route '''
        
        time = 0
        prev = 0
        
        for i in range(len(self.value)):
            time += self.instance.distances[prev, self.value[i]]
            
            customer = self.instance.customers[self.value[i]]
            
            if time > customer.due_date:
                return float('inf')
            
            time = max(time, customer.ready_time) + customer.service_time
            
            prev = self.value[i]
        
        return time
