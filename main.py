import pandas as pd

from src.data import Data
from run import main

for group in ['solomon_25', 'solomon_50', 'solomon_100']:
    print(f' {group} '.center(80, '-'))
    
    df = pd.read_csv(f'instances/{group}.csv')

    new_df = pd.DataFrame(columns=[
        'Instance', 'KM+TO Time', 'KM+TO+KN+Solver Time', 'KM+TO Distance', 'KN+Solver Distance', 'Vehicles'
    ])

    for line in df.itertuples():
        data = Data(f'instances/{group}/{line.Instance}.txt').load()
        
        km_to_time = kn_solver_time = 0

        km_cost = to_cost = solver_cost = n_vehicles = 0
        
        for i in range(3):
            km, to, kn, solver = main(data, 5)
            
            km_to_time += km[0] + to[0]
            kn_solver_time += kn[0] + solver[0]
            
            if i == 0:
                km_cost = sum(route.cost for route in km[1])
                to_cost = sum(route.cost for route in to[1])
                solver_cost = sum(route.cost for route in solver[1])
                n_vehicles = len(solver[1])
        
        km_to_time /= 3
        kn_solver_time /= 3
        
        new_df.loc[len(new_df)] = {
            'Instance': line.Instance,
            'KM+TO Time': round(km_to_time, 3),
            'KM+TO+KN+Solver Time': round(km_to_time + kn_solver_time, 3),
            'KM+TO Distance': to_cost,
            'KN+Solver Distance': solver_cost,
            'Vehicles': n_vehicles
        }
        
        print(f'Instance {line.Instance} processed ({km_to_time + kn_solver_time:.2f} seconds)')
                
    new_df.to_csv(f'{group}_results.csv', index=False)