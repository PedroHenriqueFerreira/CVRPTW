from typing import Union   

from src.instance import Instance

class Route:
    ''' Class for the route '''
    
    def __init__(
        self, 
        instance: Instance, 
        value: list[int], 
        cost: float = -1,
        demand: int = -1 
    ):
        self.instance = instance # CVRPTW instance
        self.value = value # Route list
        
        self._cost: float = cost # Route cost
        self._demand: int = demand # Route demand
        
    def __repr__(self):
        ''' Return the string representation of the route '''
        
        return f'Route{self.value}'
        
    def __len__(self):
        ''' Get the length of the route '''
        
        return len(self.value)
        
    def __iter__(self):
        ''' Iterate over the route '''
        
        return iter(self.value)
        
    def __eq__(self, other: 'Route'):
        ''' Check if two routes are equal '''
        
        return self.value == other.value
        
    def __contains__(self, customer: int):
        ''' Check if a customer is in the route '''
        
        return customer in self.value
    
    def __getitem__(self, idx: int | slice):
        ''' Get the customer at the index '''
        
        return self.value[idx]
    
    def __add__(self, other: 'Route'):
        ''' Add a customer to the route '''
        
        demand = -1  
        if self.demand >= 0 and other.demand >= 0:
            demand = self.demand + other.demand
        
        cost = -1
        if self.cost >= 0 and other.cost >= 0:
            cost = self.cost + other.cost
            
            cost -= self.instance.distances[self.value[-1], 0]
            cost -= self.instance.distances[0, other.value[0]]
            cost += self.instance.distances[self.value[-1], other.value[0]]
        
        return Route(self.instance, self.value + other.value, cost, demand)
    
    def insert(self, idx: int, customer: int):
        ''' Insert a customer in the route at the index '''
        
        self.value.insert(idx, customer)
        
        if self._demand >= 0:
            self._demand += self.instance.customers[customer].demand
        
        if self._cost >= 0:
            if idx == 0:
                self._cost += self.instance.distances[0, customer] 
                self._cost += self.instance.distances[customer, self.value[1]]
                self._cost -= self.instance.distances[0, self.value[1]]
            elif idx == len(self.value) - 1:
                self._cost += self.instance.distances[self.value[-2], customer] 
                self._cost += self.instance.distances[customer, 0]
                self._cost -= self.instance.distances[self.value[-2], 0]
            else:
                self._cost += self.instance.distances[self.value[idx - 1], customer] 
                self._cost += self.instance.distances[customer, self.value[idx + 1]]
                self._cost -= self.instance.distances[self.value[idx - 1], self.value[idx + 1]]
    
    def remove(self, customer: int):
        ''' Remove a customer from the route '''
        
        self.value.pop((idx := self.value.index(customer)))
        
        if self._demand >= 0:
            self._demand -= self.instance.customers[customer].demand
        
        if self._cost >= 0:
            if idx == 0:
                self._cost -= self.instance.distances[0, customer] 
                self._cost -= self.instance.distances[customer, self.value[0]]
                self._cost += self.instance.distances[0, self.value[0]]
            elif idx == len(self.value):
                self._cost -= self.instance.distances[self.value[-1], customer] 
                self._cost -= self.instance.distances[customer, 0]
                self._cost += self.instance.distances[self.value[-1], 0]
            else:
                self._cost -= self.instance.distances[self.value[idx - 1], customer] 
                self._cost -= self.instance.distances[customer, self.value[idx]]
                self._cost += self.instance.distances[self.value[idx - 1], self.value[idx]]    
    
    def reversed(self, i = None, j = None):
        ''' Returns a reversed route on the given indexes '''
        
        route = self.value[:]
        
        route[i:j] = route[i:j][::-1]
        
        return Route(self.instance, route, self.cost, self.demand)

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
        
    def calculate_cost(self):
        ''' Calculate the cost for the route '''
        
        cost = self.instance.distances[0, self.value[0]] + self.instance.distances[self.value[-1], 0]
        
        for i in range(len(self.value) - 1):
            cost += self.instance.distances[self.value[i], self.value[i + 1]]
        
        return cost
    
    def calculate_demand(self):
        ''' Calculate the demand for the route '''
        
        return sum(self.instance.customers[c].demand for c in self.value)