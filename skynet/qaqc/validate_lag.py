#!/usr/bin/env python3
import pandas as pd
from datetime import timedelta


def parse_interval(interval:str)->timedelta:
    """Parses the interval string into a timedelta object."""
    number, unit = interval.split('-')
    number = int(number)
    if unit == 'hour':
        return timedelta(hours=number)
    elif unit == 'min':
        return timedelta(minutes=number)
    elif unit == 'sec':
        return timedelta(seconds=number)
    else:
        raise ValueError(f"Unsupported interval unit {unit}")

"""
Validating the lag of a realtime instrument's raw data is a crucial step in our QAQC process.

The lag of the realtime data refers to the time increment between data records.

In the final dataset, the lag should be consistent, e.g. the time difference between consecutive records is
1-min, 1-hour, etc.

Supported time units are: hour, min, sec.

To ensure consistency the 'date' column consisting of the datetimes of the records should be in UTC time in this format: YYYY-MM-DD HH:MM:SS
e.g. 2024-05-09 03:14:26.

* YYYY represents the year (2024)
* MM represents the month (05)
* DD represents the day (09)
* HH represents the hour in 24-hour format (03)
* MM represents the minutes (14)
* SS represents the seconds (26)

For the python datetime package use this formatting string: "%Y-%m-%d %H:%M:%S"
"""
def validate_lag(dataframe: pd.DataFrame, interval: str) -> bool:
    date_column_name = 'date'
    # Check if 'date' column exists
    if date_column_name not in dataframe.columns:
        raise ValueError(f"DataFrame must contain a {date_column_name} column")

    # Ensure the dataframe has at least two records to compare
    if len(dataframe) < 2:
        raise ValueError("DataFrame must contain at least 2 records")

    # Parse the interval string
    delta = parse_interval(interval)

    # Convert the 'timestamp' column to datetime if it's not already
    dataframe[date_column_name] = pd.to_datetime(dataframe[date_column_name])

    # Iterate through the dataframe and check the time difference
    for i in range(1, len(dataframe)):
        if dataframe[date_column_name].iloc[i] - dataframe[date_column_name].iloc[i - 1] != delta:
            return False

    return True