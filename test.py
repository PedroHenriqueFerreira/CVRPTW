import pandas as pd

for group in ['solomon_25', 'solomon_50', 'solomon_100']:
    print(f' {group} '.center(80, '-'))
    
    df = pd.read_csv(f'{group}_results.csv')
    
    print('KM+TO Time Average:', round(df['KM+TO Time'].mean(), 3), 'seconds')
    print('KM+TO+KN+Solver Time Average:', round(df['KM+TO+KN+Solver Time'].mean(), 3), 'seconds')
    
    for category in ['C1', 'R1', 'RC1', 'C2', 'R2', 'RC2']:
        print(f'{category} KM+TO', df[df['Instance'].str.startswith(category)]['KM+TO Distance'].mean())
        print(f'{category} KN+Solver', df[df['Instance'].str.startswith(category)]['KN+Solver Distance'].mean())
        print()

    # print(df)