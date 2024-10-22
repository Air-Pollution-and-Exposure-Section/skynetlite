import pytest
from datetime import timedelta
from skynet.qaqc.validate_lag import parse_interval


"""
Test the parse_interval function
"""
def test_parse_interval():
  assert parse_interval('1-hour') == timedelta(hours=1)
  assert parse_interval('1-min') == timedelta(minutes=1)
  assert parse_interval('1-sec') == timedelta(seconds=1)
