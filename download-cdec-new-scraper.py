import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

# create URL from input info
# assumes only one station and sensor per request
def build_url(station, sensor, duration='D', sd='', ed=''):
  url = 'http://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet?'
  url += 'Stations=%s' % station
  url += '&SensorNums=%d' % sensor
  url += '&dur_code=%s' % duration
  url += '&Start=%s' % sd
  url += '&End=%s' % ed
  return url

# takes df from one (station, sensor) request
# converts to a series indexed by datetime
def reformat_series(df):
  # reindex by datetime
  df['DATE TIME'] = pd.to_datetime(df['DATE TIME'])
  df.set_index('DATE TIME', inplace=True)
  df.index.rename('datetime', inplace=True)

  # keep just the "VALUE" column and rename it
  name = '%s_%s_%s' % (df['STATION_ID'][0], df['SENSOR_TYPE'][0], df['UNITS'][0])
  df = df['VALUE']
  df.rename(name, inplace=True)
  return df

url = build_url('SHA', 15)
df = pd.read_csv(url)
series = reformat_series(df)
print(series) # the series name is SHA_STORAGE_AF

# then after this I guess a bunch of different series
# would need to be cobbled together into a new dataframe
