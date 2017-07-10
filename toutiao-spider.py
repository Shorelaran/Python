import json
import os
import re
from _md5 import md5
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from multiprocessing import Pool

def get_page_index(offset, keyword):
	data = {
		'offset': offset,
		'format': 'json',
		'keyword': keyword,
		'autoload': 'true',
		'count': '20',
		'cur_tab': '3'
	}
	url = 'http://www.toutiao.com/search_content/?' + urlencode(data)
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
		for item in data.get('data'):
			yield item.get('article_url')

def get_page_detail(url):
	try:
		res = requests.get(url)
		if res.status_code == 200:
			return res.text
		return None
	except RequestException:
		print('请求详情页出错')
		return None

def parse_page_detail(html,url):
	soup = BeautifulSoup(html, 'html.parser')
	title = soup.select('title')[0].get_text()
	image_pattern = re.compile('var gallery = (.*?);', re.S)
	result = re.search(image_pattern,html)
	if result:
		data = json.loads(result.group(1))
		if data and 'sub_images' in data.keys():
			sub_images = data.get('sub_images')
			images = [item.get('url') for item in sub_images]
			for image in images : download_image(image)
			return {
				'title': title,
				'url': url,
				'images': images
			}

def download_image(url):
	print('正在下载:',url)
	try:
		res = requests.get(url)
		if res.status_code == 200:
			save_image(res.content)
		return None
	except RequestException:
		print('请求详情页出错')
		return None

def save_image(content):
	file_path = '{0}/{1}.{2}'.format('E:/a', md5(content).hexdigest(), 'jpg')
	if not os.path.exists(file_path):
		with open(file_path, 'wb') as f:
			f.write(content)
			f.close()

def main(offset):
	html = get_page_index(offset, '街拍')
	for url in parse_page_url(html):
		html = get_page_detail(url)
		if html:
			result = parse_page_detail(html, url)
			if result:
				print(result)

GROUP_START = 1
GROUP_END = 20

if __name__ == '__main__':
	groups = [x * 20 for x in range(GROUP_START,GROUP_END + 1)]
	pool = Pool()
	pool.map(main, groups)