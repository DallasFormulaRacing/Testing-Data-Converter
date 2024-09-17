from can import CSVReader
from data_deserializer import MessageData
import pandas as pd
from tqdm import tqdm

for i in range(759, 764):
    file = "./can-_ecu_" + str(i) + ".csv"

    df = pd.DataFrame()

    for msg in tqdm(CSVReader(file)):
        data = MessageData(msg)

        try:
            new_df = pd.DataFrame({"timestamp": msg.timestamp, **data.to_dict()}, index=[0])
        except:
            continue
        df = pd.concat([df, new_df])


    df.ffill(inplace=True)
    df.to_csv(f"./can_data/{file}", index=False)