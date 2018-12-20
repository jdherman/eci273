import pandas as pd 
import time
import urllib2
from bs4 import BeautifulSoup

# stations with monthly storage data
ids = pd.read_csv('all-reservoirs.csv').ID.values
d_save = {}

# **some of these don't download, not sure why
# some entries in the json file are empty

for k in ids:
  url = 'http://cdec.water.ca.gov/cgi-progs/profile?s=%s&type=dam' % k

  keep_reading = True
  while keep_reading:
    try:
      page = urllib2.urlopen(url).read()
      keep_reading = False
    except:
      print('failed, trying again')
      continue

  soup = BeautifulSoup(page, 'lxml')

  d = {}
  for tr in soup.find_all('tr')[1:]:
    tds = tr.find_all('td')
    z = zip([t.text for t in tds[0::2]], [t.text for t in tds[1::2]])
    d.update(dict(z))
    
  d_save[k] = d

  print(k)
  # if k > 'PNF':
  # print('Now downloading %s' % k)

  # # download data - returns nested dicts of pandas series
  # dat = cd.get_data(station_ids=[k], sensor_ids=[15], resolutions=['monthly'], start=None, end=None) # 74 is evap
  # df = pd.DataFrame()
  # df['storage'] = dat[k]['RESERVOIR STORAGE monthly']['value']
  # df.storage /= 1000 # TAF

  # df[df < 0] = 0.0
  # df.fillna(method='ffill', inplace=True)

  # df.to_csv('monthly/%s.csv' % k)

  # time.sleep(1)

import json
with open('reservoir_characteristics.json', 'w') as fp:
    json.dump(d_save, fp, sort_keys=True, indent=2)
