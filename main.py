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

km_cost = sum(route.cost / 10 for route in km_routes)
to_cost = sum(route.cost / 10 for route in to_routes)

print(f' KMeans ({km_time:.3f}s, {km_cost}) '.center(50, '-'))
for km_route in km_routes:
    print(km_route, km_route.cost / 10, km_route.time)

print(f' TwoOpt ({to_time:.3f}s, {to_cost}) '.center(50, '-'))
for to_route in to_routes:
    print(to_route, to_route.cost / 10, to_route.time)


print(f'{km_cost} -> {to_cost}')

solver_time, solver_routes = Solver(data, matrices).run()

solver_cost = sum(route.cost / 10 for route in solver_routes)

print(f'{to_cost} -> {solver_cost}', sum(route.time for route in solver_routes))

# plot(data, km_routes)
# plot(data, to_routes)
# plot(data, solver_routes)