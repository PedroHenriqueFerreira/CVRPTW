from sys import argv

import pandas as pd

from src.data import Data
from run import main

n_runs = int(argv[1] if len(argv) > 1 else 10)

for group in ['solomon_25', 'solomon_50', 'solomon_100']:
    print(f' {group} '.center(80, '-'))
    
    df = pd.read_csv(f'instances/{group}.csv')

    columns = ['Instance']
    
    for i in range(1, n_runs + 1):
        columns += [f'KM+TO Time {i}', f'KM+TO+KN+Solver Time {i}', f'KM+TO Distance {i}', f'KN+Solver Distance {i}']

    new_df = pd.DataFrame(columns=columns)

    for line in df.itertuples():
        data = Data(f'instances/{group}/{line.Instance}.txt').load()
        
        km_to_times = []
        kn_solver_times = []
        km_costs = []
        to_costs = []
        solver_costs = []
        vehicle_counts = []
        
        for i in range(n_runs):
            km, to, kn, solver = main(data, 5)
            
            km_to_times.append(km[0] + to[0])
            kn_solver_times.append(kn[0] + solver[0])
            
            km_costs.append(sum(route.cost for route in km[1]))
            to_costs.append(sum(route.cost for route in to[1]))
            solver_costs.append(sum(route.cost for route in solver[1]))
            vehicle_counts.append(len(solver[1]))
    
        dic = { 'Instance': line.Instance }
        
        for i in range(n_runs):
            dic[f'KM+TO Time {i + 1}'] = round(km_to_times[i], 3)
            dic[f'KM+TO+KN+Solver Time {i + 1}'] = round(km_to_times[i] + kn_solver_times[i], 3)
            dic[f'KM+TO Distance {i + 1}'] = to_costs[i]
            dic[f'KN+Solver Distance {i + 1}'] = solver_costs[i]
            dic[f'Vehicles'] = vehicle_counts[i]
        
        print(f'Instance {line.Instance} processed')
                
    new_df.to_csv(f'{group}_results.csv', index=False)