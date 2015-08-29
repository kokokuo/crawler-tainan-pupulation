# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import xlsxwriter
from .population import PopulationCrawler
'''
統計特定鄉里的每年每月人口統計，並製作成一份xlsx
'''
class VillagePopulationStatsicParser(PopulationCrawler):

	def __init__(self url, url_id, year_interval, month_interval):
		super(VillagePopulationStatsicParser, self).__init__( url, url_id, year_interval, month_interval)
		self.every_year_population = {}
		self.find_village = [
			u"光輝里",
			u"光華里",
			u"光榮里",
			u"光明里",
			u"營北里",
			u"營南里",
			u"內新里",
			u"內興里"
		]
		self.xlsx_village_column = {
			u"光輝里":1,
			u"光華里":2,
			u"光榮里":3,
			u"光明里":4,
			u"營北里":5,
			u"營南里":6,
			u"內新里":7,
			u"內興里":8,
		}
	def craw_page(self):
		# 初始化
		workbook = self.__init_xlsx()

		row_index = 1
		for y in range(self.year_start, self.year_end + 1):
			# 初始化當年的人口統計
			current_year_month_population = {}
			for village in self.find_village:
				current_year_month_population[village] = 0

			for m in range(self.month_start, self.month_end + 1):
				# 顯示資料
				# print u"第 %s 年 ,第 %s 月" % (y,m)
				# request 參數
				year_para = 'yy=' + '{:0>3d}'.format(y)
				month_para = 'mm=' + '{:0>2d}'.format(m)
				request_url = self.url + self.id + '&' + year_para + '&' + month_para

				# request頁面
				request_result = requests.get(request_url)
				# 創建指定的里結構，計算
				self.__craw_every_year_data(request_result,current_year_month_population)
				# 存入目前年份
				current_year_month = str(1911 + y) + '.' + '{:0>2d}'.format(m)
				# 寫入檔案
				self.__write2Xlsx(current_year_month_population, current_year_month, row_index, workbook)
				# 檔案索引
				row_index +=1
		workbook.close()	

	def __craw_every_year_data(self, request_result,current_year_month_population):
		soup = BeautifulSoup(request_result.content, "html.parser")
		population_table_tag = soup.find('table', attrs={'class': 'C-tableA0'})

		for tr in population_table_tag.select('tr'):
			for village in self.find_village:
				# 比對此row是否有包含欲尋找的里名稱
				if tr.find(string=village):
					# 取出 list td
					td_list = tr.find_all('td')
					# 顯示名稱與總人口數
					# print td_list[0].text, td_list[-1].text
					# 寫入list
					current_year_month_population[village] = int(td_list[-1].text.replace(',',''))


	def __init_xlsx(self):
		workbook = xlsxwriter.Workbook('台南市特定里人口統計.xlsx')
		worksheet = workbook.add_worksheet()
		# 設定Title
		for village in self.find_village:
			worksheet.write(
				0,
				self.xlsx_village_column[village],
				village)
		return workbook

	def __write2Xlsx(self,current_year_month_population, current_year_month, row_index, workbook):
		# 寫入年份月份
		worksheet = workbook.worksheets()[0]
		worksheet.write(row_index, 0 , current_year_month)
		for village in self.find_village:
			worksheet.write(
				row_index,
				self.xlsx_village_column[village],
				current_year_month_population[village]
			)
 