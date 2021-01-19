from sqlalchemy import create_engine
import pandas as pd
import re
import datetime
import numpy as np 

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
#ts_read.to_csv(r'.\township.csv')
#print(ts_read.columns)
#sample_ts = ts_read.iloc[:50, 3:5]

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
sep_date = ts_read[ts_read['upload_date'] == datetime.date(2021,1,18)]
sample_ts = sep_date[['townships','sr']].copy()
## Take datframe Yangon Region only & Date-Jan16 
#ygn = ts_read[(ts_read['sr']=='Yangon Region') & (ts_read['upload_date'] == datetime.date(2021,1,16))]
#print(ygn)
#print(sep_date.shape)
#print(ygn.shape)


jan_16 = sep_date.groupby('sr')['cumulative_no']
#print(jan_16.sum())
#print(g.transform(lambda x: x.rank(ascending=False)))

## Read Pcode excel file 
#xls = pd.ExcelFile("pcode_9_2.xlsx")
#df1 = pd.read_excel(xls, '03_Township', engine='openpyxl')
cols_to_keep = ['Township_Name_Eng','Tsp_Pcode','SR_Pcode','SR_Name_Eng','Township_Name_MMR']
df1 = pd.read_excel('./pcode_9_2.xlsx', sheet_name='03_Township', engine='openpyxl')
df1 = df1[cols_to_keep]
#print(df1.head())
#print(df1.columns)

## take only first value of the words - example: Botahtaung Township >> Botahtaung , YGN Region >> YGN 
remove_pat = re.compile(r'Township')
sr_pat = re.compile(r'Region|State')
#sample_ts['First_ts'] = sample_ts['townships'].str.rsplit(' ', expand=False)
sample_ts['First_ts'] = sample_ts.loc[:,'townships'].str.replace(remove_pat, '').str.strip()
sample_ts['First_sr'] = sample_ts.loc[:,'sr'].str.replace(sr_pat, '').str.strip()
#sample_ts[:,'First_sr'].str.strip()
#print(sample_ts.shape)

## Remove row that contain unnecessary values 
sample_ts = sample_ts[~sample_ts.First_sr.str.contains("New Case")]
#print(sample_ts.shape)
sample_ts['First_sr'].replace({
    "Naypyitaw":"Nay Pyi Taw",
    "Shan  (South)":"Shan (South)",
    "Shan  (East)":"Shan (East)",
    "Shan  (North)":"Shan (North)"
}, inplace=True)
#print(pd.unique(sample_ts['First_sr']))
#print(pd.unique(df1['SR_Name_Eng']))


## Merge two df based on township & region columns 
merged = pd.merge(sample_ts, df1, how='left', left_on=['First_ts','First_sr'], right_on=['Township_Name_Eng', 'SR_Name_Eng'])
#print(merged.head())
#print(merged.columns)
#print(merged.isnull().sum())

filter1 = df1["SR_Name_Eng"] == "Yangon"
filter2 = df1["SR_Name_Eng"] == "Bago (West)"
trouble = merged[merged.Tsp_Pcode.isnull()]
#print(trouble.shape)
trouble = trouble.dropna(axis='columns', how='all')
#print(trouble.shape)
#print(trouble)

## Taking Bago data for East & West 
bago_ts = df1[(df1["SR_Name_Eng"] == "Bago (East)") | (df1["SR_Name_Eng"] == "Bago (West)")]
#print(bago_ts.shape)
#bago_ts['check'] = np.where(bago_ts['Township_Name_Eng']==trouble['First_ts'], 'True', 'False')
#print(bago_ts)

bago_merged = pd.merge(trouble,bago_ts, how='inner', left_on=['First_ts'], right_on = ['Township_Name_Eng'])
#print(bago_merged.shape)
#print(merged.shape)
merged = merged[merged['Tsp_Pcode'].notna()]
final = pd.concat([merged, bago_merged], ignore_index=True)
final.to_csv(r'.\pcode.csv', encoding='utf-8')
print(final.shape)
#print(final.tail(10))