# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import xlsxwriter
from .population import PopulationCrawler

'''
此類別取得全部，所有每一年的各個里的細節人口資料，並依照每年製作成各個xlsx檔案
'''
class AllPopulationParser(PopulationCrawler):

    def __init__(self, url, url_id, year_interval, month_interval):
        super(AllPopulationParser, self).__init__(url, url_id, year_interval, month_interval)

    def crawl_page(self):
        '''
        執行爬蟲，會從每年每月依序Parse，並且以各個年份製作成xlsx檔案
        '''
        print 'start crawling...'

        self.__parse_every_year_month()

        print 'all done...'

    def __parse_every_year_month(self):
        '''
        Parse 每年每月的個里人口資料
        '''
        # print 'url is =>' + self.url + self.id
        # 尋訪每年
        for y in range(self.year_start, self.year_end + 1):
            # left padding zero three digit ex:098 ,103
            year = "yy=" + '{:0>3d}'.format(y)
            # create xlsx Workbook
            filename = '台南市人口統計-' + str(y) + '.xlsx'
            workbook = xlsxwriter.Workbook(filename)

            # 尋訪每個月
            for m in range(self.month_start, self.month_end + 1):
                month = "mm=" + '{:0>2d}'.format(m)
                # print 'current year: ' + year + 'current month: ' + month
                # print 'url = ' + self.url + self.id + '&' + year + '&' + month
                res = requests.get(self.url + self.id + '&' + year + '&' + month)

                # 取得目前年份每月的人口統計資料，並存入excel
                self.__crawl_population_table(res, y, m, workbook)

            # 保存文件
            workbook.close()
            # 完成此年份
            print 'finished ' + filename + '.'

    def __crawl_population_table(self, res_result, year, month, workbook):
        '''
        傳入每年每月的個里URL beautifulSoup物件，開始做目前年份目前月的個里人口資料Parse，並存成檔案

        :param res_result: requests物件
        :param year: 目前年份(int)
        :param month: 目前月份(int)
        :param workbook: 要寫入Excel的workbook物件
        '''
        worksheet = workbook.add_worksheet(str(month) + u"月")
        # print type(res_result.content)
        # 需傳入content才會正確產生格式
        soup = BeautifulSoup(res_result.content, "html.parser")
        # utf-8
        # print type(soup.original_encoding)

        # 印出內容
        # print soup.contents
        table = soup.find('table', attrs={'class': 'C-tableA0'})
        i = 1
        for tr in table.select('tr'):
            # 標題
            self.__parse_table_conetnt(tr, 'th', worksheet, i)
            # 內容
            self.__parse_table_conetnt(tr, 'td', worksheet, i)
            i += 1

    def __parse_table_conetnt(self, tr, find_tag, worksheet, row_index):
        '''
        Parse table內的td or th標籤

        :param tr: beautifulsoup tag, tr標籤
        :param find_tag: 要傳入尋找的標籤字串 ex: 'td'
        :param worksheet: worksheet物件
        :param row_index: 傳入此前要寫入worksheet的row索引
        '''
        list = tr.find_all(find_tag)
        j = 0
        for table_content in list:
            worksheet.write(row_index, j, table_content.text)
            # print column[:-1]
            j += 1
