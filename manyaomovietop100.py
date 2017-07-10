import re
from multiprocessing import Pool
import requests
from requests.exceptions import RequestException

def get_one_page(url):
	try:
		response = requests.get(url)
		if response.status_code ==200:
			return response.text
		return None
	except RequestException:
		return None

def parse_one_page(html):
	pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name"><a.*?">(.*?)</a>.*?star">(.*?)</p>'
						 +'.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
	items = re.findall(pattern, html)
	for item in items:
		yield {
			'排名' : item[0],
			'电影名': item[2].strip(),
			'主演': item[3].strip()[3:],
			'上映时间': item[4].strip()[5:],
			'评分': item[5] + item[6],
			#'封面' : item[1]
		}

def write_to_file(content):
	file_path = 'E:/movie-top100.txt'
	with open(file_path, 'a', encoding='utf-8') as f:
		f.write(content + '\n')
		f.close()

def main(offset):
	url = 'http://maoyan.com/board/4?offset=' + str(offset)
	html = get_one_page(url)
	for item in parse_one_page(html):
		line = item['排名'] + ' '+ item['电影名'] + ' 评分' + item['评分'] + ' 主演:' + item['主演']
		print(line)
		write_to_file(line)

if __name__ == '__main__':
	for i in range(10):
		main(i*10)
	#pool = Pool()
	#pool.map(main, [i*10 for i in range(10)])
