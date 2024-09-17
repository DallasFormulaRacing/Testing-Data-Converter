import pandas as pd
from modules.ldparser import ldData
import numpy as np
from can import CSVReader
from modules.data_deserializer import MessageData
from tqdm import tqdm
from io import StringIO
import csv

i = 758

file = "./can_data/can-_ecu_" + str(i) + "_small.csv" # using _small here because otherwise it takes a little while to process the data, and there's no point in that for quick development.

df = pd.DataFrame().set_flags(
    allows_duplicate_labels=False
)

for msg in tqdm(CSVReader(file)):
    data = MessageData(msg)

    try:
        new_df = pd.DataFrame({"timestamp": msg.timestamp, **data.to_dict()}, index=[0])
    except:
        continue
    df = pd.concat([df, new_df])


df.ffill(inplace=True)

# This is the most god awful thing i've ever made, but without it pandas will error about duplicate indexes,
# and no matter what I tried, this was the easiest way to "deal with that." 
# I encourage anyone to find a better solution to this, because it is BAD.
buffer = StringIO()
df.to_csv(buffer)
buffer.seek(0)
df = pd.read_csv(buffer)
# End of terrible code

# Rearranging dataframe so motec will accept data
dfColumns=['Engine Speed','Engine Speed Limit','Gear','Brake State',
           'ECU Acceleration X','ECU Acceleration Y','ECU Acceleration Z',
           'Corr Speed','Throttle Servo Bank 1 Aim',
           'Throttle Servo Bank 1 Position','Throttle Pedal','Brake Bias Setting',
           'Fuel Injector Primary Duty Cycle','Throttle Position','Throttle Aim',
           'Steering Angle','Brake Pressure Front','Brake Pressure Rear',
           'Engine Oil Pressure','Brake Temp FL','Brake Temp FR','Brake Temp RL',
           'Brake Temp RR','Inlet Air Temperature','Coolant Temperature',
           'Engine Oil Temperature','Differential Temperature','Transmission Temperature',
           'Tyre Temp FL','Tyre Temp FR','Tyre Temp RL','Tyre Temp RR','Fuel Mixture Aim',
           'Exhaust Lambda Bank 1','Exhaust Lambda Bank 2','Exhaust Lambda',
           'Inlet Manifold Pressure','Fuel Pressure','Ignition Timing',
           'Ignition Timing Main','ECU Battery Voltage','Beacon']

output_df = pd.DataFrame(np.zeros((len(df.index), len(dfColumns))), columns = dfColumns)

# This is long, don't know how else to format

output_df[['Engine Speed','Throttle Position', 'Inlet Air Temperature', 'Coolant Temperature', 'Exhaust Lambda', 'Inlet Manifold Pressure', 'ECU Battery Voltage']] = df[['RPM', 'TPS', 'Air Temp', 'Coolant Temp', 'Lambda', 'MAP', 'Battery Volt']].copy()

# create an lddata object from the dataframe
l = ldData.frompd(output_df)

# write an .ld file
l.write("test.ld")