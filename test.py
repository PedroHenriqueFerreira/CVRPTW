import pandas as pd

from main import main

for group in ['solomon_25', 'solomon_50', 'solomon_100']:
    print(f' {group} '.center(80, '-'))
    
    for line in pd.read_csv(f'instances/{group}.csv').itertuples():
        main(f'instances/{group}/{line.Instance}.txt', 0)