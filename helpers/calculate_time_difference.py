from datetime import datetime


def calculate_time_difference(base_time):
    current_time = datetime.now()
    time_difference = (current_time - base_time).total_seconds()
    return time_difference
