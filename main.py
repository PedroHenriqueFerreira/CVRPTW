from src.data import Data
from src.k_means import KMeans
from src.two_opt import TwoOpt
from src.k_neighbors import KNeighbors
from src.solver import Solver

from src.utils import plot

from sys import argv

def main(*args):
    data = Data(args[0]).load()

    km = KMeans(data, random_state=0).run()
    to = TwoOpt(km[1]).run()

    kn = KNeighbors(data, int(args[1]), to[1]).run()
    solver = Solver(data, kn[1]).run()

    return km, to, kn, solver

if __name__ == '__main__':
    if len(argv) < 3:
        print('Usage: python main.py <instance_file> <k_neighbors>')
        exit(1)
    
    km, to, kn, solver = main(*argv[1:])
    
    print(f'K-Means + Two-Opt (Time): {km[0] + to[0]:.3f}')
    print(f'Solver (Time): {kn[0] + solver[0]:.3f}')