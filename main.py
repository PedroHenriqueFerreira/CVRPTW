from src.data import Data
from src.k_means import KMeans
from src.two_opt import TwoOpt
from src.k_neighbors import KNeighbors
from src.solver import Solver

from src.utils import plot

from sys import argv

if len(argv) < 4:
    print('Usage: python main.py <instance_file> <vehicle_number> <k_neighbors>')
    exit(1)

data = Data(argv[1]).load()

km_time, km_routes = KMeans(data, int(argv[2]), random_state=0).run()
to_time, to_routes = TwoOpt(km_routes).run()
kn_time, matrices = KNeighbors(data, int(argv[3]), to_routes).run()
solver_time, solver_routes = Solver(data, matrices).run()

km_cost = sum(route.cost for route in km_routes)
to_cost = sum(route.cost for route in to_routes)
solver_cost = sum(route.cost for route in solver_routes)

print(f'{km_cost} -> {to_cost} -> {solver_cost}')

plot(data, km_routes)
plot(data, to_routes)
plot(data, solver_routes)