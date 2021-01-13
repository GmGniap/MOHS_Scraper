# Code by TPM , Jan 13
import pymysql
import time
from datetime import date
from sqlalchemy import create_engine

from mohs_data import get_data

# Start connection 
conn = pymysql.connect(host= 'localhost', user='root', password='paing', db='mohs')

#Initialise sql engine 
engine = create_engine('mysql+pymysql://root:paing@localhost:3306/mohs')

# Date info for filename
today = date.today()
# YYYYMMDD
today_str = today.strftime("%m_%d")
# html_file 
html_file = "arg_"+today_str+".html"

# Data Update 
summary,ts_data = get_data(html_file)

# need to covert previous String type into Integer 
# but comma separated (like 1,500) is being error while coverting into int 
# so need to use split,join function as a trick 
ts_data['cumulative_no'] = ts_data['cumulative_no'].str.split(',').str.join('').astype(int)
#print(ts_data.dtypes)
#print(ts_data['cumulative_no'].head(10))

# change the data type into Float to match with SQL type
summary['Total_No'] = summary['Total_No'].astype(float)

# change the index name to align with SQL column name
#summary.DataFrame.rename('index_name', inplace=True)
summary.rename_axis('index_name',inplace=True)
print(summary.dtypes)
print(summary)

#print(ts_data[ts_data['SR'].isnull()])
summary.to_sql('overall', con= engine, if_exists= 'append')

# need to be careful if used 'replace' instead of 'append',it'll replace the whole table
#ts_data.to_sql('township', con= engine, if_exists= 'append', index=False)
print("Successful!")
'''
# Execute SQL to retrieve from a table
with engine.connect() as conn, conn.begin():
    data = pd.read_sql('select * from morningstar_key_financials_aud;', conn)
'''
