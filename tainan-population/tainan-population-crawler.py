# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from crawler.all_population import AllPopulationParser

def main():
    # 台南市政府 人口統計 url
    url = 'http://nthr.nantou.gov.tw/CustomerSet/032_population/u_population_v.asp'
    url_id = "?id={8C3E3E30-CA6D-4819-87D7-CC6C52B1EA67}"
    # 取得最新的年份
    newest_year = get_newest_year(url, url_id)
    print 'newest_year', newest_year

    # 爬蟲物件
    population_parser = AllPopulationParser(url, url_id, [86, newest_year], [1, 12])
    population_parser.crawl_page()


def get_newest_year(url, id):
    '''
    取得最新的年份，傳入台南市政府的統計網址與id
    '''

    res = requests.get(url + id)
    soup = BeautifulSoup(res.content, "html.parser")
    # get sub tree for id = yy and the first child option tag name
    first_option = soup.find(id='yy').find('option')
    # get option value by xpath
    return int(first_option["value"])


if __name__ == '__main__':
    main()