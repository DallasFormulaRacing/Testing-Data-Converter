# Takes a dataframe column and scales it to fit within the bounds [-10,10]


def process_steered_angle(series):  # dataframe column
    angle_series = series.astype(float)

    # apply data transformation from Arjun's Grafana dashboard
    angle_series = angle_series.apply(lambda x: ((x - 2) * 0.75))
    # Scale the data to fit within the bounds [-10,10] like MoTec steered angle
    angle_series = angle_series.apply(lambda x: x * 8.888 if x > 0 else x * 6.7114094 if x < 10 else x)
    angle_series = angle_series.apply(lambda x: 10 if x > 10 else -10 if x < -10 else x)
    # Convert to MoTec's degrees range. It's weirdly automatically between -572.9578 and 572.9578
    angle_series = angle_series.apply(lambda x: x * 57.29578)
    return angle_series
