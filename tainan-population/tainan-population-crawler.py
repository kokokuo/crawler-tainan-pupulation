# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import xlsxwriter


class PopulationCrawler(object):

	def __init__(self, year_interval, month_interval, url, id):
		self.year_start = year_interval[0]
		self.year_end = year_interval[1]
		self.month_start = month_interval[0]
		self.month_end = month_interval[1]
		self.url = url
		self.id = id

	def craw_data(self):
		'''
		執行爬蟲，會從每年每月依序Parse，並且以各個年份製作成xlsx檔案
		'''
		print 'start crawling'
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
				self.__crawl_population(res, y, m, workbook)

			# 保存文件
			workbook.close()
			# 完成此年份
			print 'finished ' + filename + '.'

		print 'all done...'

	def __crawl_population(self, res_result, year, month, workbook):
		'''
		傳入beautifulSoup物件，開始做爬蟲，並存成檔案

		res_result:requests物件
		year:目前年份(int)
		month:目前月份(int)
		workbook:要寫入Excel的workbook物件
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
		爬蟲table內的td or th標籤

		keyword:
		tr:tr tag
		find_tag:要傳入尋找的標籤字串
		worksheet:worksheet物件
		row_index:傳入此前要寫入worksheet的row索引
		'''
		list = tr.find_all(find_tag)
		j = 0
		for table_content in list:
			worksheet.write(row_index, j, table_content.text)
			# print column[:-1]
			j += 1
def main():
	# 台南市政府 人口統計 url
	url = 'http://nthr.nantou.gov.tw/CustomerSet/032_population/u_population_v.asp'
	id = "?id={8C3E3E30-CA6D-4819-87D7-CC6C52B1EA67}"
	# 取得最新的年份
	newest_year = get_newest_year(url, id)
	print 'newest_year', newest_year

	# 爬蟲物件
	crawler = PopulationCrawler([86, newest_year], [1, 12], url, id)
	crawler.craw_data()


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