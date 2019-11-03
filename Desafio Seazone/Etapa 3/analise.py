import pandas as pd 

vivareal = 'vivareal 2019-11-03'
airbnb = 'airbnb 2019-11-03'

df = pd.read_csv(f'leituras/{vivareal}.csv','\t')
df2 = pd.read_csv(f'leituras/{airbnb}.csv','\t')