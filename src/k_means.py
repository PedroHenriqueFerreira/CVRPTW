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
        
    def fit(self, customers: list[Customer]):
        clusters: list[Route] = []
        
        for customer in sample(customers, self.n_clusters):
            clusters.append(Route(self.instance, [], customer.pos))
        
        # customers.sort(key=lambda c: c.demand, reverse=True)
        customers.sort(key=lambda c: c.due_date, reverse=False)
        
        pos = [cluster.pos for cluster in clusters]
        
        for it in range(self.max_iter):
            print(f'Iteration {it + 1}/{self.max_iter}')
            
            for i, cluster in enumerate(clusters):
                cluster.clear(pos[i])
            
            for c in customers:
                best = -1
                best_cost = float('inf')
                
                for i, cluster in enumerate(clusters):
                    if cluster.demand + c.demand > self.instance.vehicle_capacity:
                        continue
                    
                    if not cluster.value:
                        cost = distance(cluster.pos, c.pos)
                    else:
                        cost = distance(self.instance.customers[cluster.value[-1]].pos, c.pos)
                        
                        arrival = cluster.time + cost
                        
                        cost += max(0, arrival - c.due_date)
                        
                    if cost < best_cost:
                        best_cost = cost
                        best = i
                
                if best == -1:
                    raise ValueError('Increase the number of clusters')
                
                clusters[best].append(c.id)
                
            for i, cluster in enumerate(clusters):
                if cluster.value:
                    pos[i] = np.mean([self.instance.customers[j].pos for j in cluster], axis=0)
                else:
                    pos[i] = choice(self.instance.customers).pos
                
            if np.allclose(pos, [cluster.pos for cluster in clusters]):
                break
            
        
        return clusters