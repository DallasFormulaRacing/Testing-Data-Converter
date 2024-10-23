import channels_to_motec.interpolate_channel as interpolate_channel


# Takes a dataframe series and transforms the data to fit in MoTec as a Steered Angle
def process_steered_angle(time_series, angle_series):  # dataframe series
    processed_angle_series = angle_series.astype(float)

    # apply data transformation from Arjun's Grafana dashboard
    processed_angle_series = processed_angle_series.apply(lambda x: ((x - 2) * 0.75))
    # Scale the data to fit within the bounds [-10,10] like MoTec (m) default range
    processed_angle_series = processed_angle_series.apply(lambda x: x * 8.888 if x > 0 else x * 6.7114094 if x < 10 else x)
    processed_angle_series = processed_angle_series.apply(lambda x: 10 if x > 10 else -10 if x < -10 else x)
    # Convert to MoTec's degrees range. It's weirdly automatically between -572.9578 and 572.9578
    processed_angle_series = processed_angle_series.apply(lambda x: x * 57.29578)

    # Interpolate the data to create regular time intervals
    processed_angle_series, hz = interpolate_channel.make_data_regular_intervals(time_series, processed_angle_series)

    return processed_angle_series, hz


# Takes a dataframe series and transforms the data to fit in MoTec as a Throttle Position
def process_throttle_position(time_series, throttle_series):
    processed_throttle_series = throttle_series.astype(float)
    processed_throttle_series, hz = interpolate_channel.make_data_regular_intervals(time_series, processed_throttle_series)
    return processed_throttle_series, hz
