import pytest
from datetime import timedelta
import pandas as pd
from skynet.qaqc.validate_lag import validate_lag


"""
Test the validate_lag function
"""
def test_validate_lag():
  data = {
      'date': ['2024-05-09 03:14:26', '2024-05-09 04:14:26', '2024-05-09 05:14:26']
  }
  df = pd.DataFrame(data)
  assert validate_lag(df, '1-hour') == True
  assert validate_lag(df, '1-min') == False

  # Test that an error gets thrown if there is no date column
  # In this example the dataframe has a 'datetime' column instead of a date column
  data = {
      'datetime': ['2024-05-09 03:14:26', '2024-05-09 04:14:26', '2024-05-09 05:14:26']
  }
  df = pd.DataFrame(data)
  with pytest.raises(ValueError, match=f"DataFrame must contain a date column"):
    validate_lag(df, '1-hour')

  # Test that an error gets thrown if the dataframe only less than two records
  # In this example the dataframe has the correct 'date' column name
  # but only contains one record, so vlaidating the lag is not possible
  data = {
      'date': ['2024-05-09 03:14:26']
  }
  df = pd.DataFrame(data)
  with pytest.raises(ValueError, match="DataFrame must contain at least 2 records"):
    validate_lag(df, '1-hour')