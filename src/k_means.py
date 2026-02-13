import numpy as np
from random import sample, choice, seed
from math import ceil

from src.data import Data
from src.customer import Customer
from src.route import Route

from src.utils import timer, distance

class KMeans:
    def __init__(
        self, 
        data: Data,
        n_clusters: int | None = None,
        max_iter = 100, 
        random_state: int | None = None
    ):
        self.data = data
        self.n_clusters = n_clusters
        self.max_iter = max_iter

        if random_state is not None:
            seed(random_state)
    
    def fit(self, customers: list[Customer]):
        ''' Fit the model to the instance '''
        
        clusters: list[Route] = []
        pos: list[np.ndarray] = []
        
        for customer in sample(customers, self.n_clusters):
            clusters.append(Route(self.data, [], customer.pos))
            pos.append(customer.pos)
        
        for it in range(self.max_iter):
            print(f'Iteration {it + 1}/{self.max_iter}')
            
            for i, cluster in enumerate(clusters):
                cluster.clear(pos[i])
            
            for customer in customers:
                best: Route | None = None
                
                for cluster in clusters:
                    if cluster.demand + customer.demand > self.data.vehicle_capacity:
                        continue
                    
                    if len(cluster):
                        cost = distance(cluster[-1].pos, customer.pos)
                        
                        time = cluster.time + cost
                    
                        if time > customer.due_date:
                            continue
                        
                        time = max(time, customer.ready_time) + customer.service_time
                        
                        if time + self.data.distances[customer.id, 0] > self.data.depot.due_date:
                            continue
                        
                    else:
                        cost = distance(cluster.pos, customer.pos)
                        
                        # Dont need to check constraints for a single customer (only depot -> customer -> depot)
                        
                    if best is None or cost < best.cost:
                        best = cluster
                
                if best is None:
                    raise ValueError('Increase the number of clusters')
                
                best.append(customer)
                
            for i, cluster in enumerate(clusters):
                if len(cluster):
                    pos[i] = np.mean([customer.pos for customer in cluster], axis=0)
                else:
                    pos[i] = choice(customers).pos
                
            if np.allclose(pos, [cluster.pos for cluster in clusters]):
                break
            
        return clusters
    
    @timer
    def run(self) -> tuple[float, list[Route]]:
        ''' Returns a list of clusters (routes) and the time taken to compute them.'''
        
        customers = sorted(self.data.customers[1:], key=lambda c: c.due_date)
    
        if self.n_clusters is None:
            self.n_clusters = self.data.min_vehicle_number
        else:
            return self.fit(customers)
        
        while self.n_clusters <= self.data.max_vehicle_number:
            try:
                return self.fit(customers)
            except Exception:
                self.n_clusters += 1
                
        raise ValueError('Could not find a solution with the given number of clusters')