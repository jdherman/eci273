import pandas as pd 
import urllib
import numpy as np
from io import StringIO

dates = pd.date_range(start='4/20/2010', end='12/29/2020')
dates = dates.strftime('%Y%m%d')

hours = pd.date_range(start='4/20/2010', end='12/29/2020', freq='H')
cols = ['geothermal', 'biomass', 'biogas', 'small hydro', 'wind total', 'solar',
        'renewables', 'nuclear', 'thermal', 'imports', 'hydro']

# this will be the dataframe we fill in
total_gen = pd.DataFrame(index=hours, columns=cols)

for d in dates:

  # these days have junk data
  if d in ['20150308', '20160313', '20170312']: 
    continue

  print(d)
  url = 'http://content.caiso.com/green/renewrpt/%s_DailyRenewablesWatch.txt' % d
  
  try:
    page = urllib.request.urlopen(url).read()
  except:
    print('Day %s failed, continuing...' % d)

  soup = BeautifulSoup(page, 'lxml')
  t = str(soup.find('p').text).replace('\t\t', ',').replace('\t',',')

  # grab the two tables and combine them into one
  df1 = pd.read_csv(StringIO(t), header=1, nrows=24)
  df2 = pd.read_csv(StringIO(t), header=29, nrows=24)
  df = pd.concat([df1, df2.drop('Hour', axis=1)], axis=1)
  df.set_index('Hour', inplace=True)
  df = df[df.columns[~df.columns.str.contains('Unnamed:')]]
  df.columns = [c.lower() for c in df.columns] # uppercase

  # starting in July 2012, they separate solar pv and solar thermal
  # add them back together and fix missing values
  if df.values.shape[1] > 11:

    if df['solar thermal'].dtype == np.object_: # string
      ix = df['solar thermal'].str.contains('No Good Data')
      df['solar thermal'][ix] = np.nan
      df['solar thermal'] = pd.to_numeric(df['solar thermal'])
    
    df['solar'] = df['solar pv'] + df['solar thermal']
    df = df[list(total_gen.columns)] # re-order and only keep cols in output
  
  total_gen[d] = df.values

total_gen.to_csv('CAISO-all-hourly.csv')

# even after this, beware of bad data values like #NAME, #REF, #VALUE etc
# I did some manual cleaning in the final CSV files
