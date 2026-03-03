import pandas as pd

from main import main

for group in ['solomon_25', 'solomon_50', 'solomon_100']:
    print(f' {group} '.center(80, '-'))
    
    for line in pd.read_csv(f'instances/{group}.csv').itertuples():
        km, to, kn, solver = main(f'instances/{group}/{line.Instance}.txt', 5)
        
        km_cost = sum(route.cost for route in km[1])
        to_cost = sum(route.cost for route in to[1])
        solver_cost = sum(route.cost for route in solver[1])
        
        print(f'{line.Instance}: {km_cost} -> {to_cost} -> {solver_cost}')