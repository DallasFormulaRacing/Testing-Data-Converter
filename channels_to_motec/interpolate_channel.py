import numpy as np


# Interpolates data to create regular time intervals between data points
def make_data_regular_intervals(time_series, data_series):
    # Determine the smallest interval in time between data points
    smallest_interval = min(np.diff(time_series))

    # Round the smallest interval so the hz is a whole number, while keeping the interval close to what it was.
    smallest_interval = 1 / round((1 / smallest_interval))

    # Calculate the number of points needed to create regular intervals
    num_points = int((time_series.iloc[-1] - time_series.iloc[0]) / smallest_interval) + 1

    # Create new time values at regular intervals
    new_time_series = np.linspace(time_series.iloc[0], time_series.iloc[-1], num_points)

    # Interpolate the angle values for the new time values
    new_data_series = np.interp(new_time_series, time_series, data_series)

    hz = int(1 / smallest_interval)

    return new_data_series, hz
