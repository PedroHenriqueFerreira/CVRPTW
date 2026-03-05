import numpy as np
from random import sample, choice, seed
from math import ceil

from src.data import Data
from src.customer import Customer
from src.route import Route

from src.utils import timer

class KMeans:
    def __init__(
        self, 
        data: Data,
        max_iter = 300, 
        random_state: int | None = None
    ):
        self.data = data
        self.max_iter = max_iter

        if random_state is not None:
            seed(random_state)
    
    @timer
    def run(self) -> tuple[float, list[Route]]:
        ''' Returns a list of clusters (routes) and the time taken to compute them.'''
        
        customers = sorted(self.data.customers[1:], key=lambda c: (c.due_date, c.ready_time))
    
        clusters: list[Route] = []
        pos: list[np.ndarray] = []
        
        for customer in sample(customers, self.data.min_vehicle_number):
            clusters.append(Route(self.data, [], customer.pos))
            pos.append(customer.pos)
        
        for it in range(self.max_iter):
            # print(f'Iteration {it + 1}/{self.max_iter}')
            
            for i, cluster in enumerate(clusters):
                cluster.clear(pos[i])

            remaining: list[Customer] = []
            
            for customer in customers:
                best = None
                best_cost = float('inf')
                
                for i, cluster in enumerate(clusters):
                    if cluster.demand + customer.demand > self.data.vehicle_capacity:
                        continue
                    
                    if len(cluster):
                        cost = self.data.distance(cluster[-1].pos, customer.pos)
                        
                        time = cluster.time + cost

                        if time > customer.due_date:
                            continue
                        
                        time = max(time, customer.ready_time) + customer.service_time
                        
                        if time + self.data.distances[customer.id, 0] > self.data.depot.due_date:
                            continue
                        
                    else:   
                        cost = self.data.distance(cluster.pos, customer.pos)
                        
                        # Dont need to check constraints for a single customer (only depot -> customer -> depot)
                        
                    if cost < best_cost:
                        best = cluster
                        best_cost = cost
                        
                if best is None:
                    remaining.append(customer)
                    # raise ValueError('Increase the number of clusters')
                else:
                    best.append(customer)
            
            for customer in remaining:
                clusters = sorted(clusters, key=lambda cluster: self.data.distance(cluster.pos, customer.pos))
                
                inserted = False
                
                for i, cluster in enumerate(clusters):
                    best_insertion = cluster.best_insertion(customer)
                    
                    if best_insertion is not None:
                        clusters[i] = best_insertion
                        inserted = True
                        
                        break
            
                if not inserted:
                    # INCREASE THE NUMBER OF CLUSTERS
                    if len(clusters) < self.data.max_vehicle_number:
                        clusters.append(Route(self.data, [], customer.pos))
                        pos.append(customer.pos)
                        
                        break
                    else:
                        raise ValueError('Increase the number of clusters')

            for i, cluster in enumerate(clusters):
                if len(cluster):
                    pos[i] = np.mean([customer.pos for customer in cluster], axis=0)
                else:
                    pos[i] = choice(customers).pos
            
            if np.allclose(pos, [cluster.pos for cluster in clusters]):
                break
        
        return clusters