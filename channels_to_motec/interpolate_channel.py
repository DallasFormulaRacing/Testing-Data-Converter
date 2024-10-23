import numpy as np


# Interpolates data to create regular time intervals between data points
def make_data_regular_intervals(time_series, data_series):
    # Determine the smallest interval
    smallest_interval = min(np.diff(time_series))
    print(f'smallest_interval before rounding: {smallest_interval}')

    # Round the smallest interval so the hz is a whole number
    smallest_interval = round(smallest_interval / 10) * 10
    print(f'smallest_interval after rounding: {smallest_interval}')

    # Calculate the number of points needed to create regular intervals
    num_points = int((time_series.iloc[-1] - time_series.iloc[0]) / smallest_interval) + 1

    # Create new time values at regular intervals
    new_time_series = np.linspace(time_series.iloc[0], time_series.iloc[-1], num_points)

    # Interpolate the angle values for the new time values
    new_data_series = np.interp(new_time_series, time_series, data_series)

    hz = int(1000 / smallest_interval)

    return new_data_series, hz
