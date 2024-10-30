import pandas as pd
import channels_to_motec.interpolate_channel as interpolate_channel


# Removes rows with NaN values from the data series and time series
# and filters out data points that are recorded within 10ms of each other
def prune_channels(time_series, data_series):
    # Remove rows with NaN values
    mask = data_series.notna()
    time_series, data_series = time_series[mask], data_series[mask]

    # Filter out data points with a difference of less than 0.01 seconds
    reduced_time_series = []
    reduced_data_series = []

    last_time = time_series.iloc[0]
    reduced_time_series.append(last_time)
    reduced_data_series.append(data_series.iloc[0])

    for i in range(1, len(time_series)):
        current_time = time_series.iloc[i]
        if current_time - last_time >= .01:
            reduced_time_series.append(current_time)
            reduced_data_series.append(data_series.iloc[i])
            last_time = current_time

    return pd.Series(reduced_time_series), pd.Series(reduced_data_series)


# Takes a dataframe series that is the right shape, and prunes it and interpolates it, so it conforms to MoTec
def assimilate_channel(time_series, data_series):
    time_series, data_series = prune_channels(time_series, data_series)
    processed_data_series = data_series.astype(float)
    processed_data_series, hz = interpolate_channel.make_data_regular_intervals(time_series, processed_data_series)
    return processed_data_series, hz


# Takes a time series and steered angle series and transforms the data to fit in MoTec as a Steered Angle
def transform_steered_angle(time_series, angle_series):
    #  Prune the data
    time_series, angle_series = prune_channels(time_series, angle_series)
    processed_angle_series = angle_series.astype(float)

    # Apply data transformation from Arjun's Grafana dashboard
    processed_angle_series = processed_angle_series.apply(lambda x: ((x - 2) * 0.75))
    # Scale the data to fit within the bounds [-10,10] so we can adjust it easily
    processed_angle_series = processed_angle_series.apply(
        lambda x: x * 8.888 if x > 0 else x * 6.7114094 if x < 10 else x)
    processed_angle_series = processed_angle_series.apply(lambda x: 10 if x > 10 else -10 if x < -10 else x)
    # Convert to our wheel's range of motion, [-105,105].
    processed_angle_series = processed_angle_series.apply(lambda x: x * 10.5)

    # Interpolate the data to create regular time intervals
    processed_angle_series, hz = interpolate_channel.make_data_regular_intervals(time_series, processed_angle_series)

    return processed_angle_series, hz


def transform_brakes_pressure(time_series, brakes_pressure_series):
    #  Prune the data
    time_series, brakes_pressure_series = prune_channels(time_series, brakes_pressure_series)
    processed_brakes_pressure_series = brakes_pressure_series.astype(float)

    # Apply data transformation from Arjun
    processed_brakes_pressure_series = processed_brakes_pressure_series.apply(lambda x: 500 * (x - 0.5))

    # Interpolate the data to create regular time intervals
    processed_brakes_pressure_series, hz = interpolate_channel.make_data_regular_intervals(time_series,
                                                                                           processed_brakes_pressure_series)

    return processed_brakes_pressure_series, hz
