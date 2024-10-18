import pandas as pd
import process_steered_angle
import interpolate_data
import plotly.express as px

# Load CSV file into a dataframe
steered_angle_dataframe = interpolate_data.csv_to_dataframe('Data/Steering Angle-data-2024-10-18 01_26_50.csv')

# Interpolate the data to create regular time intervals, so we can use HZ in the MoTec converter I like
interpolated_angle_series = process_steered_angle.process_steered_angle(steered_angle_dataframe['Steered Angle'])
ranged_steered_angle_dataframe = pd.DataFrame({'Time': steered_angle_dataframe['Time'], 'Steered Angle': interpolated_angle_series})

fig = px.line(ranged_steered_angle_dataframe, x='Time', y='Steered Angle')
fig.show()
