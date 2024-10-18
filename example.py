import pandas as pd
import process_steered_angle
import interpolate_data
import ldparser
import plotly.express as px

# Load CSV file into a dataframe
steered_angle_dataframe = interpolate_data.csv_to_dataframe('Data/random_steering_data_from_grafana_10-13-2024.csv')

# Interpolate the data to create regular time intervals, so we can use HZ in the MoTec converter I like
interpolated_angle_series = process_steered_angle.process_steered_angle(steered_angle_dataframe['Steered Angle'])
ranged_steered_angle_dataframe = pd.DataFrame({'Time': steered_angle_dataframe['Time'], 'Steered Angle': interpolated_angle_series})

# for val in ranged_steered_angle_dataframe['Steered Angle']:
#     print(f'{val},', end='')

ld_data = ldparser.ldData.frompd(ranged_steered_angle_dataframe)
ld_data.write('output.ld')

fig = px.line(ranged_steered_angle_dataframe, x='Time', y='Steered Angle')
fig.show()