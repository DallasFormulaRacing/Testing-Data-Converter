# Takes a dataframe column and scales it to fit within the bounds [-10,10]


def process_steered_angle(series):  # dataframe column
    angle_series = series.astype(float)

    # Define the lowest/highest possible values in sensor data
    # I don't know what these are right now, so we'll use the lowest/highest in the series FOR NOW
    can_min = angle_series.min()
    can_max = angle_series.max()

    # Scale data to fit between -10 and 10, like .ld Steered Angle does (I think)
    angle_series = angle_series.apply(lambda x: ((x - can_min) / (can_max - can_min) * 20 - 10))
    return angle_series
