# -*- coding:utf-8 -*-
class PopulationCrawler(object):

	def __init__(self, url, url_id, year_interval, month_interval):
		'''
		初始化
		:param url:網址連結
		:param url_id:網址的第一個參數url_id (含querystirng ?)
		:param year_interval: 抓取的年份，list紀錄開始與結束兩個值 ex: [86,102]
		:param month_interval: 抓取的月份，list紀錄開始與結束兩個值 ex: [1,12]
		'''
		self.year_start = year_interval[0]
		self.year_end = year_interval[1]
		self.month_start = month_interval[0]
		self.month_end = month_interval[1]
		self.url = url
		self.id = url_id

	def crawl_page(self):
		'''
		執行爬蟲，會從每年每月依序Parse，並且以各個年份製作成xlsx檔案
		'''
		pass