from sqlalchemy import create_engine
import pandas as pd
import re

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
print(pd.unique(ts_read['sr']))
print(len(pd.unique(ts_read['sr'])))