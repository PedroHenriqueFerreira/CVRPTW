from src.data import Data
from src.k_means import KMeans
from src.two_opt import TwoOpt
from src.k_neighbors import KNeighbors
from src.solver import Solver

from src.utils import plot

from sys import argv

def main(*args):
    data = Data(args[0]).load()

    km_time, km_routes = KMeans(data, int(args[1]), random_state=0).run()
    to_time, to_routes = TwoOpt(km_routes).run()

    km_cost = sum(route.cost / 10 for route in km_routes)
    to_cost = sum(route.cost / 10 for route in to_routes)

    km_test = sum(route.time for route in km_routes)
    to_test = sum(route.time for route in to_routes)

    # print(f' KMeans (spent={km_time:.3f}s, cost={km_cost}, time={km_test}s) '.center(80, '-'))
    # for km_route in km_routes:
    #     print(km_route, km_route.cost / 10, km_route.time)

    # print(f' TwoOpt (spent={to_time:.3f}s, cost={to_cost}, time={to_test}s) '.center(80, '-'))
    # for to_route in to_routes:
    #     print(to_route, to_route.cost / 10, to_route.time)

    print(args[0].split('/')[-1].split('.')[0], end=' -> ')

    print(f'{km_cost:.3f} ({km_test}) -> {to_cost:.3f} ({to_test}) -> ', end='')

    if int(args[2]) >= 0:
        kn_time, matrices = KNeighbors(data, int(args[2]), to_routes).run()
        solver_time, solver_routes = Solver(data, matrices).run()

        solver_cost = sum(route.cost / 10 for route in solver_routes)
        solver_test = sum(route.time for route in solver_routes)

        print(f'{solver_cost:.3f} ({solver_test})')
    else:
        print('No solver')

    if len(args) > 3 and args[3] == 'plot':
        plot(data, km_routes)
        plot(data, to_routes)
        
        if int(args[2]) >= 0:
            plot(data, solver_routes)

if __name__ == '__main__':
    if len(argv) < 4:
        print('Usage: python main.py <instance_file> <vehicle_number> <k_neighbors>')
        exit(1)
    
    main(*argv[1:])