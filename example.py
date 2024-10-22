from mandrewLDWriter import File, Channel
import pandas as pd
import process_steered_angle
import interpolate_data
import time

# Load CSV file into a dataframe
steered_angle_dataframe = interpolate_data.csv_to_dataframe('Data/random_steering_data_from_grafana_10-13-2024.csv')

# Interpolate the data to create regular time intervals, so we can use HZ in the MoTec converter I like
interpolated_angle_series = process_steered_angle.process_steered_angle(steered_angle_dataframe['Steered Angle'])
ranged_steered_angle_dataframe = pd.DataFrame({'Time': steered_angle_dataframe['Time'], 'Steered Angle': interpolated_angle_series})

# for val in ranged_steered_angle_dataframe['Steered Angle']:
#     print(f'{val},', end='')


# Create a File instance
example_file = File()
example_file.Time = time.localtime()
example_file.Driver = 'Reid Minton'
example_file.Vehicle = 'Baller Mobile'
example_file.Venue = 'Pedestrian Promenade'
example_file.ShortComment = 'A brief ride through the pedestrian promenade'
example_file.EventName = 'Pedestrian Promenade Grand Prix'
example_file.EventSession = 'Qualifying'
example_file.EventComment = 'event comment here'
example_file.VehicleId = '1234'
example_file.VehicleWeight = 300
example_file.VehicleType = 'Formula Car'
example_file.VehicleComment = 'Super fast Dallas Formula Racing car'

# Create channels
channel1 = Channel(
    frequency=98,
    name='Steered Angle',
    short_name='SA',
    unit='deg',
    data=ranged_steered_angle_dataframe['Steered Angle']
)

# channel2 = Channel(
#     frequency=100,
#     name='Speed',
#     short_name='SPD',
#     unit='km/h',
#     data=[0.0, 50.0, 100.0, 150.0]
# )

# Add channels to the file
example_file.add_channels(channel1)

# Write the file
example_file.write(open('output.ld', 'wb'))
