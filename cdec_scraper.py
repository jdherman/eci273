import numpy as np
import pandas as pd 

def cdec_build_url(station=None, sensor=None, duration=None, sd=None, ed=None):
  url = 'http://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?'
  url += 'Stations=%s' % station
  url += '&SensorNums=%d' % sensor
  url += '&dur_code=%s' % duration
  url += '&Start=%s' % sd
  url += '&End=%s' % ed
  return url

# takes df from one (station, sensor) request
# converts to a series indexed by datetime
def cdec_reformat_series(df):
  try:
    df.index.rename('datetime', inplace=True)
    # keep just the "VALUE" column and rename it
    name = '%s_%s_%s' % (df['STATION_ID'][0], df['SENSOR_TYPE'][0], df['UNITS'][0])
    df = df['VALUE'].rename(name).to_frame()
  except IndexError: #empty data frame causes indexerror
    raise IndexError('Requested data does not exist')
  return df

# gets data from a specific station and sensor type
def cdec_sensor_data(station=None, sensor=None, duration=None, sd=None, ed=None):
  url = cdec_build_url(station, sensor, duration, sd, ed)
  df = pd.read_csv(url, parse_dates=[4,5], index_col='DATE TIME', na_values='---')
  series = cdec_reformat_series(df)
  return series
