import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

# some IHA examples 

df = pd.read_csv('data/putah-winters.csv', 
  index_col=0, parse_dates=True)
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
# this is a trickier one. we can write a custom function to apply.

# this custom function will be applied to each water year
def day_of_peak(x):
  d = x.idxmax().dayofyear # get the date of the peak flow
  return (d - 274 if d >= 274 else d + 91) # convert calendar day to water-year day

# apply the function to get a new series of just the integer days each year
day_of_peak = df.resample('AS-OCT').apply(day_of_peak) 

day_of_peak.plot()
plt.ylabel('Day of Water Year (Oct 1 = 0)')
plt.show()

predam_avg = day_of_peak[:'1957'].mean()
postdam_avg = day_of_peak['1957':].mean()
print('Pre-Dam DOWY peak flow: %d, Post-dam: %d' % (predam_avg, postdam_avg))
