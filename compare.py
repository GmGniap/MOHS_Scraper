from sqlalchemy import create_engine
import pandas as pd
import re
import datetime

engine = create_engine('mysql+pymysql://root:paing@localhost:3306/mohs')
ts_read = pd.read_sql('SELECT * FROM township',con=engine)
#print(ts_read.head())

## Check total volumne of cumulative_no
#print(ts_read['cumulative_no'].sum())

## Check null value on township column
#print(ts_read[ts_read.townships.isnull()])



## Apply Regex for SR clean names 
#ts_read['sr'].apply(lambda x: re.sub(r'*', '', x))
#ts_read['sr'] = ts_read['sr'].str.replace(r'Naypyitaw\*', 'NPT')

ts_read = ts_read.replace({'sr': r'\*'}, {'sr': ''}, regex=True)
ts_read.to_csv(r'.\township.csv')
#print(ts_read.columns)
#sample_ts = ts_read.iloc[:50, 3:5]
sample_ts = ts_read[:50]
#print(pd.unique(ts_read['sr']))
#print(len(pd.unique(ts_read['sr'])))

#print(sample_ts.isnull().sum())
#g = ts_read.groupby('sr')['cumulative_no']
#print(g.sum())

## Date/Time Groupby 
'''
ts_read['trouble_day'] = ts_read['upload_date'].map(lambda x: x.strftime('%D'))
group_test = ts_read.groupby('trouble_day').size()
print(group_test)
''' 
## To filter date , used datetime.date funtion 
sep_date = ts_read[ts_read['upload_date'] == datetime.date(2021,1,16)]

## Take datframe Yangon Region only & Date-Jan16 
#ygn = ts_read[(ts_read['sr']=='Yangon Region') & (ts_read['upload_date'] == datetime.date(2021,1,16))]
#print(ygn)
#print(sep_date.shape)
#print(ygn.shape)


jan_16 = sep_date.groupby('sr')['cumulative_no']
print(jan_16.sum())
#print(g.transform(lambda x: x.rank(ascending=False)))