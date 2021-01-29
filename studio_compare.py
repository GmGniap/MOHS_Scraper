import pandas as pd

## for Data Studio , I've to generate another csv because Data Studio works with only Lat/Long.
## So, generate csv then join Lat/Long columns into one with comma separated.
cols_to_keep = ['Town_Name_MMR','Tsp_Pcode','Longitude', 'Latitude']
df2 = pd.read_excel('./pcode_9_2.xlsx', sheet_name='04_Town', engine='openpyxl')
df2 = df2[cols_to_keep]
print(df2.shape)
## drop duplicated Tsp_pcode rows 
df2 = df2.drop_duplicates(subset = ['Tsp_Pcode'])

df2['combined'] = df2[['Latitude','Longitude']].apply(lambda x: ",".join(x.values.astype(str)), axis=1)
df2 = df2.dropna()
#print(df2.shape)
#df2.to_csv(r'.\df2.csv')
#print(df2.head())


## previous data reading 
df3 = pd.read_csv("edit_pcode.csv", encoding='utf-8')

## Remove (South)/(East),etc extra word from First_sr column 
df3['First_sr'] = df3['First_sr'].replace(regex=[r'\(\w+\)'], value='').str.strip()
print(pd.unique(df3['First_sr']))
#print(df3.shape)
#print(df3.head())

merged = pd.merge(df3, df2, on='Tsp_Pcode', how='inner')
print(merged.shape)
#print(merged.columns)
#merged.to_csv(r'.\pcode_studio.csv')
