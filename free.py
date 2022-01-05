import requests
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
import time
class judicial():
	def __init__(self):
		self.url = 'https://aomp109.judicial.gov.tw/judbp/wkw/WHD1A02/QUERY.htm'
		a = 1
		self.post_data ={
			'crtnm': '全部',
			'proptype': 'C52',
			'saletype': '1',
			'sorted_column': 'A.CRMYY, A.CRMID, A.CRMNO, A.SALENO, A.ROWID',
			'sorted_type': 'ASC',
			'_ORDER_BY': '',
			'pageNum': 1,
			'pageSize': 9999 #一頁顯示多少筆資料
			}

	def requests(self):
		headers = {'User-Agent': 'your_UA',  #<<<貼上你的 User Agent
		'Referer' : 'https://aomp109.judicial.gov.tw/judbp/wkw/WHD1A02/V2.htm?',
		}

		session = requests.session()
		session.get('https://aomp109.judicial.gov.tw/judbp/wkw/WHD1A02.htm',headers = headers)
		r = session.post(self.url, data = self.post_data)
		datas = json.loads(r.text)['data']

		for data in datas:
			crt_name = data['crtnm']
			case_num = data['crm']+data['dptstr']
			saledate = data['saledate']
			cities = data['hsimun']+data['ctmd']
			address = data['budadd']+data['area3str']+data['saleamtstr']
			price = data['summinprcstr']
			checkyn = data['checkynstr']
			emptyyn = data['emptyynstr']
			batchno = data['batchno']
			remark = data['rmkexcel']
			commyn = data['commynstr']
			yield crt_name, case_num, saledate, cities, address, price, checkyn, emptyyn, batchno, remark, commyn


	def to_xlsx(self,save_path):
		datas = self.requests()
		df = pd.DataFrame(datas)
		df.columns=['法院名稱', '案號股別','拍賣日期拍賣次數','縣市','房屋地址樓層面積','總拍賣底價(元)','點交','空屋','標別','備註','採通訊投標']
		df.to_xlsx(save_path+str(time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()))+'.xlsx')

if __name__ == '__main__':
	judicial = judicial()
	judicial.to_xlsx('your_path')#<<<貼上你儲存路徑


	

		