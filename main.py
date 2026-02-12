import numpy as np
import matplotlib.pyplot as plt

from src.instance import Instance
from src.route import Route
from src.k_means import KMeans
from src.two_opt import TwoOpt

from sys import argv

if len(argv) < 3:
    print('Usage: python main.py <instance_file> <vehicle_number>')
    exit(1)

instance = Instance(argv[1]).load()

km_time, clusters = KMeans(instance, n_clusters=int(argv[2]), random_state=0).run(instance.customers[1:])

print('TIME', sum(cluster.time for cluster in clusters), sum(cluster.calculate_time() for cluster in clusters))
print('DEMAND', sum(cluster.demand for cluster in clusters), sum(cluster.calculate_demand() for cluster in clusters))
print('COST', sum(cluster.cost for cluster in clusters), sum(cluster.calculate_cost() for cluster in clusters))

to_time, clusters = TwoOpt().run(clusters)

print('TIME', sum(cluster.time for cluster in clusters), sum(cluster.calculate_time() for cluster in clusters))
print('DEMAND', sum(cluster.demand for cluster in clusters), sum(cluster.calculate_demand() for cluster in clusters))
print('COST', sum(cluster.cost for cluster in clusters), sum(cluster.calculate_cost() for cluster in clusters))

plt.figure(figsize=(12, 6))

for cluster in clusters:
    x = [customer.x for customer in cluster]
    y = [customer.y for customer in cluster]
    
    plt.scatter(x, y, label=f'Cluster {clusters.index(cluster) + 1}')

    for customer in cluster:
        plt.text(customer.x, customer.y, str(customer.demand), fontsize=7, ha='center', va='center')
    
    cluster_demand = sum(customer.demand for customer in cluster)
    plt.text(cluster.x, cluster.y, f'{cluster_demand}', fontsize=12, ha='center', va='center', fontweight='bold', color='red')
    
    
    # PLOT EDGES OF CONSECUTIVE CUSTOMERS IN THE CLUSTER
    for i in range(len(cluster) - 1):
        c1 = cluster[i]
        c2 = cluster[i + 1]
        plt.plot([c1.x, c2.x], [c1.y, c2.y], c='gray', linestyle='--', linewidth=1)
        
        plt.arrow(
            c1.x, c1.y,
            (c2.x - c1.x) * 0.85,
            (c2.y - c1.y) * 0.85,
            head_width=0.1,
            head_length=0.2,
            fc='gray',
            ec='gray',
            linestyle='--',
            linewidth=1
        )

    # PLOT EDGES BETWEEN FIRST AND LAST CUSTOMER TO THE DEPOT
    if cluster:
        depot = instance.customers[0]
        
        c1 = cluster[0]
        c2 = cluster[-1]
        
        plt.plot([depot.x, c1.x], [depot.y,  c1.y], c='gray', linestyle='--', linewidth=1)
        plt.plot([depot.x, c2.x], [depot.y, c2.y], c='gray', linestyle='--', linewidth=1)

total_cost = sum(route.cost for route in clusters)
plt.text(0.5, 0.95, f'Total Cost: {total_cost:.2f}', fontsize=12, ha='center', va='center', transform=plt.gca().transAxes)

plt.title(instance.name)
plt.xlabel('X')
plt.ylabel('Y')
plt.show()