import time
import pandas as pd
from channels_to_motec.mandrewLDWriter import File, Channel
import channels_to_motec.transform_channel as tc


# Processes and transforms a series into the shape of a channel we want to write our MoTeC file
def process_channel(dataframe, time_series_name, data_series_name, transform_function=None):
    time_series = dataframe[time_series_name]
    data_series = dataframe[data_series_name]
    if transform_function:
        return transform_function(time_series, data_series)
    return tc.assimilate_channel(time_series, data_series)


# Creates a channel object with the given parameters
def create_channel(name, short_name, unit, data, frequency):
    return Channel(
        frequency=frequency,
        name=name,
        short_name=short_name,
        unit=unit,
        data=data
    )


if __name__ == "__main__":
    # Load the data from the CANbus CSV file
    can_dataframe = pd.read_csv('Data/Converted CANbus Data/758.csv')

    # Define the channels we want to write to the MoTeC file
    channels_info = [
        # (Name, Short Name, Unit, Data Series Name, Transform Function)
        ('Engine RPM', 'RPM', 'rpm', 'RPM', None),
        ('Wheel Speed', 'WS', 'ft/s', 'Driven Wheel Speed #1', None),
        ('Eng Oil Pres', 'OP', 'V', 'Analog Input #1', None),
        ('Front Brakes Pres', 'BPF', 'psi', 'Analog Input #6', tc.transform_brakes_pressure),
        ('Rear Brakes Pres', 'BPR', 'psi', 'Analog Input #4', tc.transform_brakes_pressure),
        ('Steered Angle', 'SA', 'deg', 'Analog Input #2', tc.transform_steered_angle),
        ('Throttle Pos', 'TP', '%', 'TPS', None),
        ('Inlet Air Temp', 'IAT', 'C', 'Air Temp', None),
        ('Inlet Manifold Pres', 'IMP', 'kPa', 'MAP', None),
        ('Exhaust Lambda', 'EL', 'LA', 'Lambda', None),
        ('Ignition Timing', 'IT', 'deg', 'Ignition Angle', None),
        ('ECU Battery Voltage', 'EBV', 'V', 'Battery Volt', None),
        # Here are the channels that weren't in Reid's original list
        ('Fuel Open Time', 'FOT', 'ms', 'Fuel Open Time', None),
        ('Coolant Temp', 'CT', 'C', 'Coolant Temp', None),
        ('Frequency 1', 'F1', 'Hz', 'Frequency 1', None),
        ('Frequency 2', 'F2', 'Hz', 'Frequency 2', None),
        ('Frequency 3', 'F3', 'Hz', 'Frequency 3', None),
        ('Frequency 4', 'F4', 'Hz', 'Frequency 4', None),
        ('Driven Avg Wheel Speed', 'DAWS', 'ft/s', 'Driven Avg Wheel Speed', None),
        ('Non-Driven Avg Wheel Speed', 'NDAWS', 'ft/s', 'Non-Driven Avg Wheel Speed', None),
        ('Ignition Compensation', 'IC', 'deg', 'Ignition Compensation', None),
        ('Ignition Cut Percentage', 'ICP', '%', 'Ignition Cut Percentage', None),
        ('Driven Wheel Speed #2', 'DWS2', 'ft/s', 'Driven Wheel Speed #2', None),
        ('Barometer', 'BAR', 'kPa', 'Barometer', None),
        ('Analog Input #1', 'AI1', 'V', 'Analog Input #1', None),
        ('Analog Input #3', 'AI3', 'V', 'Analog Input #3', None),
        ('Analog Input #5', 'AI5', 'V', 'Analog Input #5', None),
        ('Analog Input #7', 'AI7', 'V', 'Analog Input #7', None),
        ('Analog Input #8', 'AI8', 'V', 'Analog Input #8', None)
    ]

    # Create the MoTeC file object
    motec_file = File()
    motec_file.Time = time.localtime(can_dataframe['timestamp'][0])
    motec_file.Driver = 'Reid Minton'
    motec_file.Vehicle = 'Baller Mobile'
    motec_file.Venue = 'Pedestrian Promenade'
    motec_file.ShortComment = 'A brief ride through the pedestrian promenade'
    motec_file.EventName = 'Pedestrian Promenade Grand Prix'
    motec_file.EventSession = 'Qualifying'
    motec_file.EventComment = 'event comment here'
    motec_file.VehicleId = '1234'
    motec_file.VehicleWeight = 300  # I think this may be broken
    motec_file.VehicleType = 'Formula Car'
    motec_file.VehicleComment = 'Super fast Dallas Formula Racing car'

    # Loop through the channels, process them, and add them to the MoTeC file
    for name, short_name, unit, data_series_name, transform_function in channels_info:
        data, frequency = process_channel(can_dataframe, 'timestamp', data_series_name, transform_function)
        channel = create_channel(name, short_name, unit, data, frequency)
        motec_file.add_channels(channel)

    # Write the MoTeC file to the output.ld file
    motec_file.write(open('output.ld', 'wb'))
