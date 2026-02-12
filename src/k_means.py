import numpy as np
from random import sample, choice, seed

from src.instance import Instance
from src.customer import Customer
from src.route import Route
from src.utils import timer, distance

class KMeans:
    def __init__(
        self, 
        instance: Instance, 
        n_clusters: int, 
        max_iter = 100, 
        random_state: int | None = None
    ):
        self.instance = instance
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        
        if random_state is not None:
            seed(random_state)
    
    @timer
    def run(self, customers: list[Customer]) -> tuple[float, list[Route]]:
        clusters: list[Route] = []
        
        for customer in sample(customers, self.n_clusters):
            clusters.append(Route(self.instance, [], customer.pos))
        
        customers.sort(key=lambda c: c.due_date, reverse=False)
        
        pos = [cluster.pos for cluster in clusters]
        
        for it in range(self.max_iter):
            print(f'Iteration {it + 1}/{self.max_iter}')
            
            for i, cluster in enumerate(clusters):
                cluster.clear(pos[i])
            
            for customer in customers:
                best: Route | None = None
                best_cost = float('inf')
                
                for cluster in clusters:
                    if cluster.demand + customer.demand > self.instance.vehicle_capacity:
                        continue
                    
                    if len(cluster):
                        cost = distance(cluster[-1].pos, customer.pos)
                        
                        if cluster.time + cost > customer.due_date:
                            continue
                    else:
                        cost = distance(cluster.pos, customer.pos)
                        
                    if cost < best_cost:
                        best_cost = cost
                        best = cluster
                
                if best is None:
                    raise ValueError('Increase the number of clusters')
                
                best.append(customer)
                
            for i, cluster in enumerate(clusters):
                if len(cluster):
                    pos[i] = np.mean([customer.pos for customer in cluster], axis=0)
                else:
                    pos[i] = choice(self.instance.customers).pos
                
            if np.allclose(pos, [cluster.pos for cluster in clusters]):
                break
            
        
        return clusters