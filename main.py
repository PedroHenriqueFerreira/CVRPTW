from src.data import Data
from src.k_means import KMeans
from src.two_opt import TwoOpt

from src.utils import plot

from sys import argv

if len(argv) < 2:
    print('Usage: python main.py <instance_file> [<vehicle_number>]')
    exit(1)

data = Data(argv[1]).load()

km_time, clusters = KMeans(data, int(argv[2]) if len(argv) > 2 else None, random_state=0).run()
prev_total_cost = sum(cluster.cost for cluster in clusters)

to_time, new_clusters = TwoOpt().run(clusters)
curr_total_cost = sum(cluster.cost for cluster in new_clusters)

print(f'{prev_total_cost} -> {curr_total_cost}', curr_total_cost - prev_total_cost)

plot(data, clusters)
plot(data, new_clusters)

