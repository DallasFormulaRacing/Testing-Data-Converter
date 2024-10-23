import time
import pandas as pd
from channels_to_motec.mandrewLDWriter import File, Channel
import channels_to_motec.transform_channel as tc

# # Load CSV files into dataframes
# steered_angle_dataframe = pd.read_csv('Data/Steered Angle Data/random_steering_data_from_grafana_10-13-2024.csv')
# throttle_position_dataframe = pd.read_csv('Data/Throttle Position Data/random_throttle_position_data_from_grafana_2024-10-22.csv')
#
#
# # Interpolate the channel to create regular time intervals, so we can use HZ in the MoTec converter I like
# processed_angle_series, angle_hz = tc.process_steered_angle(steered_angle_dataframe['Time'], steered_angle_dataframe['data Analog Input #2'])
# processed_throttle_series, throttle_hz = tc.process_throttle_position(throttle_position_dataframe['Time'], throttle_position_dataframe['data TPS'])


dataframe = pd.read_csv('Data/Converted CANbus Data/758.csv')
processed_angle_series, angle_hz = tc.process_steered_angle(dataframe['timestamp'], dataframe['Analog Input #2'])
processed_throttle_series, throttle_hz = tc.process_throttle_position(dataframe['timestamp'], dataframe['TPS'])

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
    frequency=angle_hz,
    name='Steered Angle',
    short_name='SA',
    unit='deg',
    data=processed_angle_series
)

channel2 = Channel(
    frequency=throttle_hz,
    name='Throttle Pos',
    short_name='TP',
    unit='%',
    data=processed_throttle_series
)

# Add channels to the file
example_file.add_channels(channel1, channel2)

# Write the file
example_file.write(open('output.ld', 'wb'))
