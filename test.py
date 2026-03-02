import pandas as pd

from main import main

for group in ['solomon_100']:
    df = pd.read_csv(f'instances/{group}.csv')

    for line in df.itertuples():
        main(f'instances/{group}/{line.Instance}.txt', line.Vehicles, -1)