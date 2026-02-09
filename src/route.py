import numpy as np

from src.instance import Instance

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
        
        return iter(self.value)
        
    def __getitem__(self, idx: int | slice):
        ''' Get the customer at the index '''
        
        return self.value[idx]
        
    def __contains__(self, customer: int):
        ''' Check if a customer is in the route '''
        
        return customer in self.value
        
    def __eq__(self, other: 'Route'):
        ''' Check if two routes are equal '''
        
        return self.value == other.value
    
    def __add__(self, other: 'Route'):
        ''' Add a customer to the route '''
        
        demand = -1  
        if self._demand >= 0 and other._demand >= 0:
            demand = self._demand + other._demand
        
        cost = -1
        if self._cost >= 0 and other._cost >= 0:
            cost = self._cost + other._cost

            cost -= self.instance.distances[self.value[-1], 0]
            cost -= self.instance.distances[0, other.value[0]]
            cost += self.instance.distances[self.value[-1], other.value[0]]

        time = -1
        
        return Route(
            self.instance, 
            self.value + other.value, 
            self.pos, cost, demand, time
        )
    
    def insert(self, idx: int, customer: int):
        ''' Insert a customer in the route at the index '''
        
        self.value.insert(idx, customer)
        
        if self._demand >= 0:
            self._demand += self.instance.customers[customer].demand
        
        if self._cost >= 0:
            if idx == 0:
                if len(self.value) == 1:
                    self._cost = self.instance.distances[0, customer] * 2
                else:
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
                
        if self._time >= 0:
            if idx == len(self.value) - 1:
                self._time += self.instance.distances[self.value[-1], customer]
                
                if self._time > self.instance.customers[customer].due_date:
                    self._time = float('inf')
                else:
                    self._time = max(self._time, self.instance.customers[customer].ready_time) 
                    self._time += self.instance.customers[customer].service_time
                    
            else:
                self._time = -1     
    
    def append(self, customer: int):
        ''' Append a customer to the end of the route '''
        
        self.insert(len(self.value), customer)
    
    def remove(self, customer: int):
        ''' Remove a customer from the route '''
        
        self.value.pop((idx := self.value.index(customer)))
        
        if self._demand >= 0:
            self._demand -= self.instance.customers[customer].demand
        
        if self._cost >= 0:
            if idx == 0:
                if len(self.value) == 0:
                    self._cost = 0
                else:
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
    
        if self._time >= 0:
            self._time = -1
    
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
                
        time = self._time
        if self._time >= 0:
            time = -1
                
        return Route(self.instance, value, self.pos, cost, self.demand, time)

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
    
    def feasible(self):
        ''' Check if the route is feasible '''
        
        return self.demand <= self.instance.vehicle_capacity and self.time <= self.instance.customers[0].due_date