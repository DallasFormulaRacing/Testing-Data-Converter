import pandas as pd
import numpy as np


# you know exactly what this does
def csv_to_dataframe(filepath):
    csv_file = pd.read_csv(filepath)
    first_column = csv_file.iloc[:, 0]
    second_column = csv_file.iloc[:, 1]
    csv_dataframe = pd.DataFrame({'Time': first_column, 'Steered Angle': second_column})
    return csv_dataframe


# interpolates data to create regular time intervals between data points
def make_data_regular_intervals(data):
    # Extract time and angle values
    times = data['Time']
    angles = data['Steered Angle']

    # Determine the smallest interval
    smallest_interval = min(np.diff(times))

    # Create new time values at regular intervals
    new_times = np.arange(times[0], times[-1] + smallest_interval, smallest_interval)

    # Interpolate the angle values for the new time values
    new_angles = np.interp(new_times, times, angles)

    # Combine the new time and angle values into a list of pairs
    new_data = pd.DataFrame({"Time": new_times, "Steered Angle": new_angles})

    return new_data
