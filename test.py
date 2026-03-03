import pandas as pd

from main import main

for group in ['solomon_25']:
    for line in pd.read_csv(f'instances/{group}.csv').itertuples():
        main(f'instances/{group}/{line.Instance}.txt', 4)