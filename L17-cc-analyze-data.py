import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set_style('whitegrid')
from scipy.stats import skew, norm

tafd_cfs = 1000 / 86400 * 43560
cfs_tafd = 2.29568411*10**-5 * 86400 / 1000

# load data (combine first three columns into a datetime)
df = pd.read_csv('data/streamflow_cmip5_ncar_day_GRAND.csv',
                  index_col='datetime', 
                  parse_dates={'datetime': [0,1,2]},
                  date_parser=lambda x: pd.datetime.strptime(x, '%Y %m %d'))

# filter columns by rcp
# df = df.filter(like='rcp26')

# annual rolling mean - method chaining
annual = ((df * cfs_tafd).resample('AS-OCT').sum()
           .rolling(window=50)
           .mean())

annual.plot(color='steelblue', legend=None)
plt.title('Colorado River @ Grand Canyon - NCAR CMIP5 Projections')
plt.ylabel('Annual Streamflow (TAF)')
plt.show()


###################################
# LP3 flood

def lp3(Q, ppf=0.99):
  # estimate flood with nonexceedance probability `ppf`
  Q = np.log(Q)
  m = Q.mean()
  s = Q.std()
  g = skew(Q)

  # Frequency factor Kp, HH 18.2.29
  Kp = (2/g)*(1 + g*norm.ppf(ppf)/6 - g**2/36)**3 - 2/g
  return np.exp(m + s*Kp)

# estimate 100-year flood with a rolling window - method chaining
Q100 = (df.resample('A')
          .max()
          .rolling(window=50)
          .apply(lp3, raw=True)) # raw=True passes numpy array to lp3 function

Q100.plot(color='steelblue', legend=None)
Q100.mean(axis=1).plot(color='k', linewidth=2)
plt.title('Colorado River @ Grand Canyon - NCAR CMIP5 Projections')
plt.ylabel('LP3 Estimate of 100-year flood (cfs)')
plt.show()
