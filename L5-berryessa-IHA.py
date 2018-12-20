import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

# some IHA examples 
# note the API for "resample" changed in recent pandas versions
# only matters if you installed it a while ago

df = pd.read_csv('data/putah-winters.csv', index_col=0, parse_dates=True)
# df.plot()
# plt.show()

###########
# first: how much does the reservoir alter the 3-day peak flow?
# max3day = df.rolling(3).mean().resample('AS-OCT').max()
# max3day.plot()
# plt.title('Annual maximum 3-day flow average (cfs)')
# plt.show()

# predam_avg = max3day[:'1957'].mean()
# postdam_avg = max3day['1957':].mean()
# print('Pre-Dam 3-day peak flow: %0.2f cfs, Post-dam: %0.2f cfs' % (predam_avg, postdam_avg))

# ###########
# # next: how much does the reservoir alter the 30-day minimum flow?
# min30day = (df.rolling(30).mean()
#               .resample('AS-OCT').min())
# min30day.plot()
# plt.title('Annual minimum 30-day flow average (cfs)')
# plt.show()

# predam_avg = min30day[:'1957'].mean()
# postdam_avg = min30day['1957':].mean()
# print('Pre-Dam 30-day min flow: %0.2f cfs, Post-dam: %0.2f cfs' % (predam_avg, postdam_avg))

###########
# last: alteration to peak flow timing
# this is a trickier one, but still clean
def water_day(d):
  return d - 274 if d >= 274 else d + 91

dowy = (df.resample('AS-OCT')
          .apply(pd.DataFrame.idxmax) # each year, find the date of max flow
          .flow_cfs.dt.dayofyear # convert that date to day of year
          .apply(water_day)) # apply custom function above to get DOWY

print(dowy)
dowy.plot()
plt.ylabel('Day of Water Year (Oct 1 = 0)')
plt.show()

# predam_avg = dowy[:'1957'].mean()
# postdam_avg = dowy['1957':].mean()
# print('Pre-Dam DOWY peak flow: %d, Post-dam: %d' % (predam_avg, postdam_avg))

