# Code by TPM - Jan 11,2021 

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup
from sheet import export_to_sheets

from selenium.webdriver.chrome.options import Options
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import pandas as pd 
import os
import re

import sys
import time

#url = 'https://doph.maps.arcgis.com/apps/opsdashboard/index.html#/f8fb4ccc3d2d42c7ab0590dbb3fc26b8'
#driver = webdriver.Chrome()
#driver.get(url)

# Date info for filename
today = date.today()
# YYYYMMDD
today_str = today.strftime("%m_%d")
today_format = today.strftime("%d-%m-%Y")

def get_source_mohs():
    driver = webdriver.Chrome()
    # Wait 30 seconds for page to load and extract the element after it loads
    driver.get(
    "https://doph.maps.arcgis.com/apps/opsdashboard/index.html#/f8fb4ccc3d2d42c7ab0590dbb3fc26b8")
    timeout = 30
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='ember28']/div[2]/nav")))
    except TimeoutException:
        print('Timed out waiting for page to load')
        driver.quit()
        return False

    
    Html_file = open("arg_"+today_str+".html", "w" ,encoding='utf-8')
    Html_file.write(driver.page_source)
    Html_file.close()
    driver.close()
    return True


    
def get_data(open_file):
    read_file = open(open_file, "r", encoding='utf-8')
    soup = BeautifulSoup(read_file, 'html.parser')
    
    
    summary = []
    tds = []

    # Scraping Abbreviation Table
    table_info = soup.find_all("table")[0]
    for row in table_info.find_all('td'):
        #print(row)
        first_txt = row.get_text().replace("-", "").strip()
        out = first_txt.splitlines()
        out_convert = []
        
        #print(out)
        #print(type(out))
        for i in out:
            #print(i.strip())
            #print("----x----")
            out_convert.append(i.strip())
        tds.append("::".join(out_convert))
    # print(tds)

    ## Scraping Summery Total Numbers (Top bar)
    all_main_info = soup.find_all("text")
    for item in all_main_info:
        summary.append(float(item.text.replace(",", "")))
    
    #print(summary)

    # Combine above two list into Dictionary
    result_dict = {}
    for key in tds:
        for value in summary:
            result_dict[key]=value
            summary.remove(value)
            break

    summary_df = pd.DataFrame.from_dict(result_dict, orient='index',columns=['Total_No'] )
    #print(summary_df)
    ts = [] 
    sr = [] 
    no = []
    
    pattern = re.compile(r'Total:\s\d+')
    pattern2 = re.compile(r'^[A-Z].*Township,.*,')
    pattern2_test = re.compile(r'[[A-Z].*Township,.*,|.*\(Seikkan\),.*|Laboratory\sConfirmed,.*|.*Yangon\sRegion\*,|.*Naypyitaw\*,|]')
    feature_list = soup.find_all('nav', class_='feature-list')

    header = ['townships','sr','cumulative_no']
    ts_sr_dict = dict.fromkeys(header)
    count = 0
    #print(ts_sr_dict)
    for feature in feature_list:
        for p in feature.find_all('p'):
            
            strong = p.find_all('strong', text = pattern)
            span = p.find_all('span', text = pattern2_test)

            
            for strong_tag in strong:
                
                #print(len(strong_tag))
                no.append(strong_tag.text.replace("Total:","").strip())
            
            for span_tag in span:
                count += 1
                test = span_tag.text.strip().split(',')
                #print(type(test))
                ts.append(test[0].strip())
                sr.append(test[1].strip())

    # Assign ts,sr,no values into dictionary 
    ts_sr_dict['townships'] = ts
    ts_sr_dict['sr'] = sr
    ts_sr_dict['cumulative_no'] = no

    ## Checking Length of scraped data list
    #print(len(ts),len(sr),len(no))
    #print(count)
    #print(no)
    #print(ts_sr_dict)
    
    # transform dictionary into dataframe 
    ts_sr_df = pd.DataFrame.from_dict(ts_sr_dict, orient='columns')
    #print(ts_sr_df.head())

    return summary_df, ts_sr_df

if __name__ == "__main__":
    html_file = "arg_"+today_str+".html"
    if os.path.isfile(html_file) is False:
        print("Scraping for..."+today_str)
        get_source_mohs()
        
    summary,ts_data = get_data(html_file)
    #print(ts_data.tail(10))
    print(summary.dtypes)
    '''
    
    print(test_df.shape)
    print(test_df.columns)
    '''
