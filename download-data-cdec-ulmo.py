import pandas as pd 
from ulmo.cdec import historical as cd
import matplotlib.pyplot as plt 
import seaborn as sns

# returns a pandas dataframe indexed on site id
# stations = cd.get_stations()

# returns a pandas dataframe with codes mapped to site information
# sensors = cd.get_sensors()
# print sensors

# returns a python dict with site codes as keys 
# with values containing pandas dataframes of available sensor numbers and metadata.
# available_sensors = cd.get_station_sensors(['FOL'], None, ['daily'])
# print available_sensors['FOL']

# k = 'FLD'
# dat = cd.get_data(station_ids=[k], sensor_ids=[4], resolutions=['event'], start='2005-01-01', end='2008-12-31')
# B = pd.DataFrame()
# B['Tair'] = dat[k]['TEMPERATURE, AIR event']['value']
# B = B.resample('D').mean()
# B.to_csv('FLD-Tair.csv')
# B.Tair.plot()
# plt.show()

k = 'FOL'
dat = cd.get_data(station_ids=[k], 
  sensor_ids=[15,6,23,76,74], resolutions=['daily'], 
  start='2015-10-01', end='2017-01-27')
B = pd.DataFrame()

B['storage'] = dat[k]['RESERVOIR STORAGE daily']['value']
# B['elevation'] = dat[k]['RESERVOIR ELEVATION daily']['value']
B['outflow'] = dat[k]['RESERVOIR OUTFLOW daily']['value']
B['inflow'] = dat[k]['RESERVOIR INFLOW daily']['value']
# # # B['precip'] = dat[k]['PRECIPITATION, INCREMENTAL daily']['value']
B['evap'] = dat[k]['EVAPORATION, LAKE COMPUTED CFS daily']['value']
# # # B['tocs'] = dat[k]['RESERVOIR, TOP CONSERV STORAGE daily']['value']

# B = pd.read_csv('data/FOL-daily-2005-08.csv', index_col=0, parse_dates=True)#['2005-01-01':'2008-12-31']
# B = B[['storage','elevation','outflow','inflow','evap']]
# df2 = pd.read_csv('data/FLD-Tair.csv', index_col=0, parse_dates=True)
# B['Tair'] = pd.Series(df2.Tair.values, index=B.index)


# storage in acre-feet. outflow/evap in CFS.
# convert to TAF and TAF/day
B.storage /= 1000 # TAF
B.outflow *= 2.29568411*10**-5 * 86400 / 1000 # TAF/day
B.inflow *= 2.29568411*10**-5 * 86400 / 1000 # TAF/day
B.evap *= 2.29568411*10**-5 * 86400 / 1000 # TAF/day
# B['evap'] = -1*(B.storage.diff() - B.inflow + B.outflow) # TAF/day IF NOT AVAILABLE TO DOWNLOAD
# precip in inches. elevation in feet.

B.inflow[B.inflow < 0] = 0.0

# B[['inflow','outflow','storage','evap']].to_csv('FOL-daily-WY2016.csv')
# B.FNF_AF.plot()
# plt.show()
# # B.to_pickle('%s.pkl' % k)
# # B = pd.read_pickle('BER.pkl')
# # B = B['20001001':'20150630']
# # B.storage.plot()
# def cfs_to_taf(Q):
#   return Q * 2.29568411*10**-5 * 86400 / 1000

B.dSdt = B.inflow - B.outflow - B.evap
B.storage.plot()
(B.storage.iloc[0] + B.dSdt.cumsum()).plot()
plt.show()