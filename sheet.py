import gspread_dataframe as gd
import gspread as gs
import csv
import pandas as pd

gc = gs.service_account(filename='test.json')

def export_to_sheets(df, mode='r'):
    sh = gc.open_by_key('1ku7kc4EVVSYRZVKLn7djICDjxHHcWqRVPFsocyc4Ktc').worksheet('main')
    if(mode == 'w'):
        sh.clear()
        gd.set_with_dataframe(worksheet=sh, dataframe=df, include_index=False,include_column_header=True,resize=True)
        return True
    elif(mode == 'a'):
        print("Append Mode")
        sh.add_rows(df.shape[0])
        gd.set_with_dataframe(worksheet=sh, dataframe=df, include_index=False, include_column_header=False, row=sh.row_count+1, resize=False)
        return True
    else:
        return gd.get_as_dataframe(worksheet=sh)