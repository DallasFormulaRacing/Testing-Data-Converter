import pandas as pd

from processSteeredAngle import process_steered_angle

d = {'col1': [1.16, 3.42, 5.60, 7.213123, 9.1], 'col2': [3.3, 4.123, 6.9966, 1.230, 9.1]}
df = pd.DataFrame(d)
print(df['col1'])
print(process_steered_angle(df['col1']))
