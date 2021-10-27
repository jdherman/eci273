import matplotlib.pyplot as plt
import pandas as pd

# read CSV data into a dataframe - pandas can parse dates
# this will be familiar to R users (not so much matlab users)
df = pd.read_csv('data/SHA.csv', 
                 index_col=0, 
                 parse_dates=True)

# dataframes have column names and an index
# print(df.columns)
# print(df.index)

# let's only use the inflow and outflow columns, and rename them
df = df[['SHA_INFLOW_CFS', 'SHA_OUTFLOW_CFS']]
df.rename(columns={'SHA_INFLOW_CFS': 'inflow', 
                   'SHA_OUTFLOW_CFS': 'outflow'}, inplace=True)

# accessing columns and rows
# print(df.inflow) # or df['inflow']. One column is called a Series.
# print(df.loc['2006-02-01']) 
# print(df.loc['2006-02-01'].inflow)

# because the dataframe is indexed by date, we can slice with dates!
# df = df['2005-10-01':'2008-09-30']

# it knows the column names from the file
# also notice the plot x-axis keeps the dates, even if you zoom in
# df.plot()
# plt.show()

# you can always go back and forth to numpy matrices
# matrix = df.values # removes index and header
# print(type(matrix))
# print(matrix)

# to create a dataframe from a matrix, need to provide index and col names
# index = pd.date_range('2005-10-01', '2008-09-30', freq='D')
# df = pd.DataFrame(matrix, index=index, columns=['inflow','outflow'])
# print(df) # this should match the original that we took "matrix" from

##############
# plot the cumulative distributions (exceedance)
# note this is also how you add Series to an existing DataFrame
# for Q in ['inflow', 'outflow']:
#   df[Q+'_exc'] = df[Q].rank(ascending=False, pct=True)
#   df = df.sort_values(by=Q+'_exc')
#   plt.plot(df[Q+'_exc'], df[Q])

# plt.legend(['Inflow', 'Outflow'])
# plt.ylabel('Streamflow')
# plt.xlabel('Exceedance')
# plt.show()

#############
# we need to learn two important functions: "resample" and "rolling"
# resample(frequency) where frequency is 'A', 'M', 'W'...
# rolling(window) every day uses the trailing (window) days to calculate

# example: take the 14-day trailing moving average of flows
# df.inflow.plot()
# df.inflow.rolling(14).mean().plot(color='k', linewidth=2)
# plt.show()

# example: aggregate daily to monthly
# watch out for units here
# df = df.resample('M').sum()
# print(df)
# df.plot(linewidth=2)
# plt.show()

# go back down?
# df = df.resample('D').mean()
# print(df)

# resampling to water year frequency (useful)
# df = df.resample('AS-OCT').sum()
# print(df)

# a full list of frequency strings is here:
# https://stackoverflow.com/questions/17001389/pandas-resample-documentation

