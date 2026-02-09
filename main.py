import numpy as np
import matplotlib.pyplot as plt

from src.instance import Instance
from src.k_means import KMeans
from src.route import Route

from sys import argv

if len(argv) < 3:
    print('Usage: python main.py <instance_file> <vehicle_number>')
    exit(1)

instance = Instance(argv[1])
instance.load()

total_demand = sum(customer.demand for customer in instance.customers)

k_means = KMeans(instance, n_clusters=int(argv[2]), random_state=None)
clusters = k_means.fit(instance.customers[1:])

plt.figure(figsize=(12, 6))

for cluster in clusters:
    x = [instance.customers[i].pos[0] for i in cluster]
    y = [instance.customers[i].pos[1] for i in cluster]
    
    plt.scatter(x, y, label=f'Cluster {clusters.index(cluster) + 1}')

    for i in cluster:
        customer = instance.customers[i]
        plt.text(customer.pos[0], customer.pos[1], str(customer.demand), fontsize=7, ha='center', va='center')
    
    cluster_demand = sum(instance.customers[i].demand for i in cluster)
    plt.text(cluster.pos[0], cluster.pos[1], f'{cluster_demand}', fontsize=12, ha='center', va='center', fontweight='bold', color='red')
    
    
    # PLOT EDGES OF CONSECUTIVE CUSTOMERS IN THE CLUSTER
    for i in range(len(cluster) - 1):
        c1 = instance.customers[cluster[i]]
        c2 = instance.customers[cluster[i + 1]]
        plt.plot([c1.pos[0], c2.pos[0]], [c1.pos[1], c2.pos[1]], c='gray', linestyle='--', linewidth=1)
        
        plt.arrow(
            c1.pos[0], c1.pos[1],
            (c2.pos[0] - c1.pos[0]) * 0.85,
            (c2.pos[1] - c1.pos[1]) * 0.85,
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
        
        c1 = instance.customers[cluster[0]]
        c2 = instance.customers[cluster[-1]]
        
        plt.plot([depot.pos[0], c1.pos[0]], [depot.pos[1],  c1.pos[1]], c='gray', linestyle='--', linewidth=1)
        plt.plot([depot.pos[0], c2.pos[0]], [depot.pos[1], c2.pos[1]], c='gray', linestyle='--', linewidth=1)

# PLOT TOTAL COST
total_cost = sum(route.cost for route in clusters)
plt.text(0.5, 0.95, f'Total Cost: {total_cost:.2f}', fontsize=12, ha='center', va='center', transform=plt.gca().transAxes)

plt.title(instance.name)
plt.xlabel('X')
plt.ylabel('Y')
plt.show()