from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup
from sheet import export_to_sheets

import pandas as pd 


import sys
import time



url = 'https://doph.maps.arcgis.com/apps/opsdashboard/index.html#/f8fb4ccc3d2d42c7ab0590dbb3fc26b8'
#url = 'https://covid19.moh.gov.sa/'
driver = webdriver.Chrome()
driver.get(url)


for i in range(0, 20):
    time.sleep(1) # Waiting for the page to fully load
    sys.stdout.write('\r{}%'.format(i*10 + 10))
    sys.stdout.flush()
sys.stdout.write("\n")

with open("A.html", "w", encoding='utf-8') as f:
    f.write(driver.page_source)


#soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()


# Opening saved MOHS dashboard page
all_stat = []
with open("A.html", encoding='utf-8') as f:
    soup = BeautifulSoup(f, "html.parser")

    feature_list = soup.find_all('nav', class_='feature-list')
    

    for feature in feature_list:
        stat = {}
        for p in feature.find_all('p'):
            strong = p.find_all('strong')
            #print(strong)
            for strong_tag in strong:
                all_stat.append(strong_tag.text.strip())
                #print(strong_tag.text)
        '''
        s = strong[0].text.split(' ')
        s[0] = s[0].strip().replace(',', '')
        stat[s[1].strip('\u200e')] = int(s[0])
        ''' 
    #print(all_stat)

df = pd.DataFrame.from_dict(all_stat)
print(df.head(20))
export_to_sheets(df, 'w')
print("Success")

'''
driver.get("https://food.ndtv.com/recipes")

def get_link_by_text(text):
    element = driver.find_element_by_link_text(text.strip())
    return element.get_attribute("href")

def get_list_by_class_name(class_name = "main_image"):
    element_list = []
    
    all_elements = driver.find_elements_by_class_name(class_name)
    element_list = [x.text for x in all_elements if len(x.text)>0]
    print(element_list)


get_list_by_class_name()
category_list = {x: get_link_by_text(x) for x in get_list_by_class_name('recipe-tab-heading')
                }
print(category_list)
'''