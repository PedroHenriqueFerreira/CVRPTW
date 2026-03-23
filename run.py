from src.data import Data
from src.k_means import KMeans
from src.two_opt import TwoOpt
from src.k_neighbors import KNeighbors
from src.solver import Solver

from src.utils import plot

from sys import argv

def main(data: Data, neighbors: int):
    km = KMeans(data).run()
    to = TwoOpt(km[1]).run()

    kn = KNeighbors(data, neighbors, to[1]).run()
    solver = Solver(data, kn[1]).run()

    return km, to, kn, solver

if __name__ == '__main__':
    if len(argv) < 3:
        print('Usage: python main.py <instance_file> <k_neighbors>')
        exit(1)
    
    data = Data(argv[1]).load()
    km, to, kn, solver = main(data, int(argv[2]))
    
    plot(data, to[1])
    plot(data, solver[1])