# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

# 計算此網頁的全國大專院校學生總數
url = requests.get('http://ricelohas.blogspot.tw/2014/01/102.html')

total_college = 0
soup =  BeautifulSoup(url.content, "html.parser")
# 資料在table下tr td:nth-child(4)中的child span span
tr_list = soup.find('table').find_all('tr')
# 掠過第一筆（因為是標題）
for tr in tr_list[1:]:
    # 取得各5筆的td
    td_list = tr.find_all('td')[4::5]
    for td in td_list:
        for span in td.select('span span'):
            total_college += int(span.text.replace(',',''))

print '全國，所有大專院校學生： %d' % total_college