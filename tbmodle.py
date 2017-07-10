import re
from multiprocessing import Pool
from urllib.parse import urlencode
import urllib.request
import requests
from requests.exceptions import RequestException
import json
import os

GirlName = []
GirlCity = []
GirlId   = []
GirlUrl  = []
GirlHeight = []
GirlWeight = []
GirlPhoUrl = []
OutputDir = 'E:/tbmodlephoto/'
url = 'https://mm.taobao.com/self/aiShow.htm?spm=719.7763510.1998643336.1.dLKjVy&userId='

def get_page_index(index):
	data = {
		'q': '',
		'viewFlag': 'A',
		'sortType': 'default',
		'searchStyle': '',
		'searchRegion': 'city',
		'searchFansNum': '',
		'currentPage': index,
		'pageSize': '100'
	}
	url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8' + urlencode(data)
	try:
		res = requests.get(url)
		if res.status_code == 200:
			return res.text
		return None
	except RequestException:
		print('请求索引页出错')
		return None

def parse_page_url(html):
	data = json.loads(html)
	if data and 'data' in data.keys():
		data_item =  data.get('data')
		for item in data_item.get('searchDOList'):
			GirlName.append(item.get('realName'))
			GirlCity.append(item.get('city'))
			GirlId.append(str(item.get('userId')))
			GirlHeight.append(item.get('height'))
			GirlWeight.append(item.get('weight'))

def mkdir(path):
	isExists = os.path.exists(path)
	if not isExists:
		os.makedirs(path)
		print('创建文件夹' + path + '成功')
		return True
	else:
		return False

def download(path, url):
	for i, img in zip(range(len(url)), url):
		html = urllib.request.urlopen('https:' + img.strip() + '.jpg')
		file_name = '{}/{}.jpg'.format(path, i + 1)
		if os.path.exists(file_name):
			print('已经存在', img)
		else:
			with open(file_name, 'wb') as f:
				print('正在下载',img)
				f.write(html.read())
				f.close()

def get_page_detail(url):
	try:
		res = requests.get(url)
		if res.status_code == 200:
			return res.text
		return None
	except RequestException:
		print('请求详情页出错')
		return None

def main(index):
	html = get_page_index(index)
	parse_page_url(html)
	GirlUrl = [(url + i) for i in GirlId]
	for Name, City, Url in zip(GirlName, GirlCity, GirlUrl):
		path = OutputDir + Name + ' ' + City
		mkdir(path)
		html = get_page_detail(Url)
		img_pattern = re.compile('img.*?src="(.*?).jpg"', re.S)
		imgs = re.findall(img_pattern, html)
		download(path, imgs)

GROUP_START = 1
GROUP_END   = 1

if __name__ == '__main__':
	# group = [x for x in range(GROUP_START, GROUP_END + 1)]
	# pool = Pool()
	# pool.map(main, group)
	main(1)