import numpy as np
import matplotlib.pyplot as plt

import numpy as np

from time import time

def timer(func):
    ''' Decorator to measure the execution time of a function '''
    
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        
        if isinstance(result, tuple):
            return end - start, *result
        
        return end - start, result
    
    return wrapper

def distance(a: np.ndarray, b: np.ndarray) -> int:
    ''' Calculate the distance between two positions '''
    
    return np.linalg.norm(a - b)

def plot(instance, clusters):
    ''' Plot the instance and the clusters '''
    
    plt.figure(figsize=(12, 6))

    for i, cluster in enumerate(clusters):
        for j in range(len(cluster) - 1):
            c1, c2 = cluster[j], cluster[j + 1]
            
            plt.plot([c1.x, c2.x], [c1.y, c2.y], c='black', alpha=0.5, linestyle='--', linewidth=1)

        c1, c2 = cluster[0], cluster[-1]
        
        plt.plot([instance.depot.x, c1.x], [instance.depot.y, c1.y], c='gray', linestyle='--', linewidth=1)
        plt.plot([instance.depot.x, c2.x], [instance.depot.y, c2.y], c='gray', linestyle='--', linewidth=1)
        
        label = f'Route {i + 1} (Demand: {sum(c.demand for c in cluster)})'
        
        plt.scatter([c.x for c in cluster], [c.y for c in cluster], label=label, zorder=3)

    # PLOT DEPOT (MARKER)
    plt.scatter(instance.depot.x, instance.depot.y, c='black', s=100, marker='X', label='Depot', zorder=4)

    plt.legend()

    plt.title(f'{instance.name} (Cost: {sum(c.cost for c in clusters):.2f})')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()