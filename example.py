import time
import pandas as pd
from channels_to_motec.mandrewLDWriter import File, Channel
import channels_to_motec.transform_channel as tc

# Load the data and process it to fit in MoTec
dataframe = pd.read_csv('Data/Converted CANbus Data/758.csv')

engine_RPM, engine_RPM_hz = tc.process_channel(dataframe['timestamp'], dataframe['RPM'])
driven_wheel_speed, driven_wheel_speed_hz = tc.process_channel(dataframe['timestamp'], dataframe['Driven Wheel Speed #1'])
oil_pressure, oil_pressure_hz = tc.process_channel(dataframe['timestamp'], dataframe['Analog Input #1'])
brakes_pressure_front, brakes_pressure_front_hz = tc.transform_brakes_pressure(dataframe['timestamp'], dataframe['Analog Input #6'])
brakes_pressure_rear, brakes_pressure_rear_hz = tc.transform_brakes_pressure(dataframe['timestamp'], dataframe['Analog Input #4'])
steered_angle, steered_angle_hz = tc.transform_steered_angle(dataframe['timestamp'], dataframe['Analog Input #2'])
throttle_position, throttle_position_hz = tc.process_channel(dataframe['timestamp'], dataframe['TPS'])
inlet_air_temp, inlet_air_temp_hz = tc.process_channel(dataframe['timestamp'], dataframe['Air Temp'])
inlet_manifold_pressure, inlet_manifold_pressure_hz = tc.process_channel(dataframe['timestamp'], dataframe['MAP'])
exhaust_lambda, exhaust_lambda_hz = tc.process_channel(dataframe['timestamp'], dataframe['Lambda'])
ignition_timing, ignition_timing_hz = tc.process_channel(dataframe['timestamp'], dataframe['Ignition Angle'])
ecu_battery_voltage, ecu_battery_voltage_hz = tc.process_channel(dataframe['timestamp'], dataframe['Battery Volt'])

# Here's some stuff I'm not sure if I should include because Reid didn't put these in his list:
fuel_open_time, fuel_open_time_hz = tc.process_channel(dataframe['timestamp'], dataframe['Fuel Open Time'])
coolant_temp, coolant_temp_hz = tc.process_channel(dataframe['timestamp'], dataframe['Coolant Temp'])
frequency_one, frequency_one_hz = tc.process_channel(dataframe['timestamp'], dataframe['Frequency 1'])
frequency_two, frequency_two_hz = tc.process_channel(dataframe['timestamp'], dataframe['Frequency 2'])
frequency_three, frequency_three_hz = tc.process_channel(dataframe['timestamp'], dataframe['Frequency 3'])
frequency_four, frequency_four_hz = tc.process_channel(dataframe['timestamp'], dataframe['Frequency 4'])
driven_avg_wheel_speed, average_driven_wheel_speed_hz = tc.process_channel(dataframe['timestamp'], dataframe['Driven Avg Wheel Speed'])
non_driven_avg_wheel_speed, average_non_driven_wheel_speed_hz = tc.process_channel(dataframe['timestamp'], dataframe['Non-Driven Avg Wheel Speed'])
ignition_compensation, ignition_compensation_hz = tc.process_channel(dataframe['timestamp'], dataframe['Ignition Compensation'])
ignition_cut, ignition_cut_hz = tc.process_channel(dataframe['timestamp'], dataframe['Ignition Cut Percentage'])
driven_wheel_speed_two, driven_wheel_speed_two_hz = tc.process_channel(dataframe['timestamp'], dataframe['Driven Wheel Speed #2'])
barometer, barometer_hz = tc.process_channel(dataframe['timestamp'], dataframe['Barometer'])
analog_input_one, analog_input_one_hz = tc.process_channel(dataframe['timestamp'], dataframe['Analog Input #1'])
analog_input_three, analog_input_three_hz = tc.process_channel(dataframe['timestamp'], dataframe['Analog Input #3'])
analog_input_five, analog_input_five_hz = tc.process_channel(dataframe['timestamp'], dataframe['Analog Input #5'])
analog_input_seven, analog_input_seven_hz = tc.process_channel(dataframe['timestamp'], dataframe['Analog Input #7'])
analog_input_eight, analog_input_eight_hz = tc.process_channel(dataframe['timestamp'], dataframe['Analog Input #8'])

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
engine_RPM_channel = Channel(
    frequency=engine_RPM_hz,
    name='Engine RPM',
    short_name='RPM',
    unit='rpm',
    data=engine_RPM
)

driven_wheel_speed_channel = Channel(
    frequency=driven_wheel_speed_hz,
    name='Wheel Speed',
    short_name='WS',
    unit='ft/s',
    data=driven_wheel_speed
)

oil_pressure_channel = Channel(
    frequency=oil_pressure_hz,
    name='Eng Oil Pres',
    short_name='OP',
    unit='V',
    data=oil_pressure
)

brakes_pressure_front_channel = Channel(
    frequency=brakes_pressure_front_hz,
    name='Front Brakes Pres',
    short_name='BPF',
    unit='psi',
    data=brakes_pressure_front
)

brakes_pressure_rear_channel = Channel(
    frequency=brakes_pressure_rear_hz,
    name='Rear Brakes Pres',
    short_name='BPR',
    unit='psi',
    data=brakes_pressure_rear
)

steered_angle_channel = Channel(
    frequency=steered_angle_hz,
    name='Steered Angle',
    short_name='SA',
    unit='deg',
    data=steered_angle
)

throttle_channel = Channel(
    frequency=throttle_position_hz,
    name='Throttle Pos',
    short_name='TP',
    unit='%',
    data=throttle_position
)

inlet_air_temp_channel = Channel(
    frequency=inlet_air_temp_hz,
    name='Inlet Air Temp',
    short_name='IAT',
    unit='C',
    data=inlet_air_temp
)

inlet_manifold_pressure_channel = Channel(
    frequency=inlet_manifold_pressure_hz,
    name='Inlet Manifold Pres',
    short_name='IMP',
    unit='kPa',
    data=inlet_manifold_pressure
)

exhaust_lambda_channel = Channel(
    frequency=exhaust_lambda_hz,
    name='Exhaust Lambda',
    short_name='EL',
    unit='LA',
    data=exhaust_lambda
)

ignition_timing_channel = Channel(
    frequency=ignition_timing_hz,
    name='Ignition Timing',
    short_name='IT',
    unit='deg',
    data=ignition_timing
)

ecu_battery_voltage_channel = Channel(
    frequency=ecu_battery_voltage_hz,
    name='ECU Battery Voltage',
    short_name='EBV',
    unit='V',
    data=ecu_battery_voltage
)


# Adding the channels that weren't in Reid's list

fuel_open_time_channel = Channel(
    frequency=fuel_open_time_hz,
    name='Fuel Open Time',
    short_name='FOT',
    unit='ms',
    data=fuel_open_time
)

coolant_temp_channel = Channel(
    frequency=coolant_temp_hz,
    name='Coolant Temp',
    short_name='CT',
    unit='C',
    data=coolant_temp
)

frequency_one_channel = Channel(
    frequency=frequency_one_hz,
    name='Frequency 1',
    short_name='F1',
    unit='Hz',
    data=frequency_one
)

frequency_two_channel = Channel(
    frequency=frequency_two_hz,
    name='Frequency 2',
    short_name='F2',
    unit='Hz',
    data=frequency_two
)

frequency_three_channel = Channel(
    frequency=frequency_three_hz,
    name='Frequency 3',
    short_name='F3',
    unit='Hz',
    data=frequency_three
)

frequency_four_channel = Channel(
    frequency=frequency_four_hz,
    name='Frequency 4',
    short_name='F4',
    unit='Hz',
    data=frequency_four
)

driven_avg_wheel_speed_channel = Channel(
    frequency=average_driven_wheel_speed_hz,
    name='Driven Avg Wheel Speed',
    short_name='DAWS',
    unit='ft/s',
    data=driven_avg_wheel_speed
)

non_driven_avg_wheel_speed_channel = Channel(
    frequency=average_non_driven_wheel_speed_hz,
    name='Non-Driven Avg Wheel Speed',
    short_name='NDAWS',
    unit='ft/s',
    data=non_driven_avg_wheel_speed
)

ignition_compensation_channel = Channel(
    frequency=ignition_compensation_hz,
    name='Ignition Compensation',
    short_name='IC',
    unit='deg',
    data=ignition_compensation
)

ignition_cut_channel = Channel(
    frequency=ignition_cut_hz,
    name='Ignition Cut Percentage',
    short_name='ICP',
    unit='%',
    data=ignition_cut
)

driven_wheel_speed_two_channel = Channel(
    frequency=driven_wheel_speed_two_hz,
    name='Driven Wheel Speed #2',
    short_name='DWS2',
    unit='ft/s',
    data=driven_wheel_speed_two
)

barometer_channel = Channel(
    frequency=barometer_hz,
    name='Barometer',
    short_name='BAR',
    unit='kPa',
    data=barometer
)

analog_input_one_channel = Channel(
    frequency=analog_input_one_hz,
    name='Analog Input #1',
    short_name='AI1',
    unit='V',
    data=analog_input_one
)

analog_input_three_channel = Channel(
    frequency=analog_input_three_hz,
    name='Analog Input #3',
    short_name='AI3',
    unit='V',
    data=analog_input_three
)

analog_input_five_channel = Channel(
    frequency=analog_input_five_hz,
    name='Analog Input #5',
    short_name='AI5',
    unit='V',
    data=analog_input_five
)

analog_input_seven_channel = Channel(
    frequency=analog_input_seven_hz,
    name='Analog Input #7',
    short_name='AI7',
    unit='V',
    data=analog_input_seven
)

analog_input_eight_channel = Channel(
    frequency=analog_input_eight_hz,
    name='Analog Input #8',
    short_name='AI8',
    unit='V',
    data=analog_input_eight
)


# Add channels to the file
channels = [
    engine_RPM_channel, driven_wheel_speed_channel, oil_pressure_channel, brakes_pressure_front_channel,
    brakes_pressure_rear_channel, steered_angle_channel, throttle_channel, inlet_air_temp_channel,
    inlet_manifold_pressure_channel, exhaust_lambda_channel, ignition_timing_channel, ecu_battery_voltage_channel
    # The channels that weren't in Reid's list:
    , fuel_open_time_channel, coolant_temp_channel, frequency_one_channel, frequency_two_channel,
    frequency_three_channel, frequency_four_channel, driven_avg_wheel_speed_channel, non_driven_avg_wheel_speed_channel,
    ignition_compensation_channel, ignition_cut_channel, driven_wheel_speed_two_channel, barometer_channel,
    analog_input_one_channel, analog_input_three_channel, analog_input_five_channel, analog_input_seven_channel,
    analog_input_eight_channel
]

for channel in channels:
    example_file.add_channels(channel)

# Write the file
example_file.write(open('output.ld', 'wb'))
