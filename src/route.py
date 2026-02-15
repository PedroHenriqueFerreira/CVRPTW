import numpy as np

from src.data import Data
from src.customer import Customer

class Route:
    ''' Class for the route '''
    
    def __init__(
        self, 
        data: Data, 
        value: list[int],
        pos: np.ndarray | None = None,
        cost: float = -1,
        demand: int = -1,
        time: int = -1,
    ):
        self.data = data # CVRPTW instance
        self.value = value # Route list
        
        self.pos = pos # Route position (for clustering)
        
        self._cost = cost # Route cost
        self._demand = demand # Route demand
        self._time = time # Route time (for clustering)
        
    def __repr__(self):
        ''' Return the string representation of the route '''
        
        return f'Route{self.value}'
        
    def __eq__(self, other: 'Route'):
        ''' Check if two routes are equal '''
        
        return self.value == other.value
        
    def __len__(self):
        ''' Get the length of the route '''
        
        return len(self.value)
        
    def __iter__(self):
        ''' Iterate over the route '''
        
        return iter(self.data.customers[item] for item in self.value)
        
    def __getitem__(self, idx: int) -> Customer:
        ''' Get the customer at the index '''
        
        return self.data.customers[self.value[idx]]

    def append(self, customer: Customer):
        ''' Append a customer to the end of the route '''
        
        self.value.append(customer.id)
        
        if self._demand >= 0:
            self._demand += customer.demand
            
        if self._cost >= 0:
            if len(self.value) == 1:
                self._cost = 2 * self.data.distances[0, customer.id]
            else:
                self._cost += self.data.distances[self.value[-2], customer.id] 
                self._cost += self.data.distances[customer.id, 0]
                self._cost -= self.data.distances[self.value[-2], 0]
                
        if self._time >= 0:
            if len(self.value) == 1:
                self._time = self.data.distances[0, customer.id]
            else:
                self._time += self.data.distances[self.value[-2], customer.id]
                
            if self._time > customer.due_date:
                self._time = float('inf')
            else:
                self._time = max(self._time, customer.ready_time) + customer.service_time
                
            if self._time + self.data.distances[customer.id, 0] > self.data.depot.due_date:
                self._time = float('inf')
    
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
        
        cost = self._cost
        if cost >= 0:
            if i > 0:
                cost -= self.data.distances[value[i - 1], value[i]]
                cost += self.data.distances[value[i - 1], value[j - 1]]
            else:
                cost -= self.data.distances[0, value[i]]
                cost += self.data.distances[0, value[j - 1]]
                
            if j < len(value):
                cost -= self.data.distances[value[j - 1], value[j]]
                cost += self.data.distances[value[i], value[j]]
            else:
                cost -= self.data.distances[value[j - 1], 0]
                cost += self.data.distances[value[i], 0]
            
            # TODO: FIX
            cost = -1
        
        return Route(self.data, value, self.pos, cost, self.demand)

    def best_reversed(self):
        ''' Returns the best reversed route '''
        
        best = self
        
        for i in range(len(self.value) - 1):
            for j in range(i + 1, len(self.value)):
                route = self.reversed(i, j + 1)
                
                if route.feasible and route.cost < best.cost:
                    best = route
        
        return best

    def insertion(self, index: int, customer: Customer):
        ''' Insert a customer at the index '''
        
        value = self.value[:]
        
        value.insert(index, customer.id)

        demand = self._demand
        if demand >= 0:
            demand += customer.demand
            
        cost = self._cost
        if cost >= 0:
            if len(value) == 1:
                cost = 2 * self.data.distances[0, customer.id]
            else:
                if index == 0:
                    cost += self.data.distances[0, customer.id] 
                    cost += self.data.distances[customer.id, value[1]]
                    cost -= self.data.distances[0, value[1]]
                elif index == len(value) - 1:
                    cost += self.data.distances[value[-2], customer.id] 
                    cost += self.data.distances[customer.id, 0]
                    cost -= self.data.distances[value[-2], 0]
                else:
                    cost += self.data.distances[value[index - 1], customer.id] 
                    cost += self.data.distances[customer.id, value[index + 1]]
                    cost -= self.data.distances[value[index - 1], value[index + 1]]

        return Route(self.data, value, self.pos, cost, demand)                    

    def best_insertion(self, customer: Customer):
        ''' Insert a customer at the best position '''
        
        if self.demand + customer.demand > self.data.vehicle_capacity:
            return None
        
        best = None
        
        for idx in range(len(self.value) + 1):
            new = self.insertion(idx, customer)
            
            if best is None or (new.cost < best.cost and new.feasible):
                best = new
        
        return best

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
        
        if self._time < 0:
            self._time = self.calculate_time()
        
        return self._time
        
    def calculate_cost(self):
        ''' Calculate the cost for the route '''
        
        if not self.value:
            return 0
        
        cost = self.data.distances[0, self.value[0]] + self.data.distances[self.value[-1], 0]
        
        for i in range(len(self.value) - 1):
            cost += self.data.distances[self.value[i], self.value[i + 1]]
        
        return cost
    
    def calculate_demand(self):
        ''' Calculate the demand for the route '''
        
        return sum(self.data.customers[c].demand for c in self.value)
    
    def calculate_time(self):
        ''' Calculate the time for the route '''
        
        time = 0
        
        prev = self.data.depot
        for customer in self:
            time += self.data.distances[prev.id, customer.id]
            
            if time > customer.due_date:
                return float('inf')
            
            time = max(time, customer.ready_time) + customer.service_time
            
            prev = customer
        
        time += self.data.distances[prev.id, self.data.depot.id]
        
        if time > self.data.depot.due_date:
            return float('inf')
        
        return time

    @property
    def feasible(self) -> bool:
        ''' Check if the route is feasible '''
        
        return self.demand <= self.data.vehicle_capacity and self.time <= self.data.depot.due_date
    