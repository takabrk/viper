#!/usr/bin/env python
#-*- coding:utf8 -*-

from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'https://www.mizuhobank.co.jp/retail/takarakuji/check/numbers/numbers3/index.html?year=2021&month=5'

op = Options()
op.add_argument("--headless")
op.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')
op.add_argument('--lang=ja-JP')

def backnumber_latest_link_to_lists():
    url = 'https://www.mizuhobank.co.jp/retail/takarakuji/check/numbers/backnumber/index.html'

    driver = webdriver.Chrome('/Users/user/driver/chromedriver',options=op)
    driver.get(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    
    lists = []
    links = driver.find_elements_by_partial_link_text('ナンバーズ3')
    for link in links:
        lists.append(link.get_attribute('href'))
    
    return lists


backnumber_latest = backnumber_latest_link_to_lists()

# A表から回別、抽選日、抽選数字をDataFrameに変換　
backnumbers = []
for link in backnumber_latest:
    url = link

    driver = webdriver.Chrome('/Users/user/driver/chromedriver',options=op)
    driver.get(url)
    no = driver.find_elements_by_class_name('bgf7f7f7')
    date = driver.find_elements_by_class_name('js-lottery-date-pc')
    number = driver.find_elements_by_class_name('js-lottery-number-pc')


    for i in range(0,len(no)):
        backnumber = {}
        backnumber['回別'] = no[i].text
        backnumber['抽せん日'] = date[i].text
        backnumber['ナンバーズ3抽せん数字'] = number[i].text

        backnumbers.append(backnumber)
backnumber_df = pd.DataFrame(backnumbers)

driver.implicitly_wait(10)
backnumber_links = driver.find_elements_by_css_selector('.typeTK.js-backnumber-b tbody tr td a')
links = []
for item in backnumber_links:
    links.append(item.get_attribute('href'))
all_df = pd.DataFrame()

for i in len(links):
    url2 = links[i]
    driver.get(url2)
    df = pd.read_html(driver.page_sourvce)[0]
    all_df = all_df.append(df,ignore_index=True)
all_df = all_df.drop(all_df.cloumns[[3]],axis=1)

df = pd.DataFrame()
df = df.append(all_df,ignore_index=True)
df = df.append(backnumber_df,ignore_index=True)
df = df.dropna(how='all')