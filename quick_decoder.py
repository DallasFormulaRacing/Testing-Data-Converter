from can.io import CSVReader
from channels_to_motec.data_deserializer import MessageData
import pandas as pd
from tqdm import tqdm

file = 'Data/chanhs-testing-data/can-_ecu_758.csv'

df = pd.DataFrame()

for msg in tqdm(CSVReader(file)):
    data = MessageData(msg)

    try:
        new_df = pd.DataFrame({"timestamp": msg.timestamp, **data.to_dict()}, index=[0])
    except:
        continue
    df = pd.concat([df, new_df])


df.to_csv(f"Data/Converted CanBUS Data/758.csv", index=False)