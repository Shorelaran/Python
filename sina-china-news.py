import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

commentURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&\
channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&\
page_size=20'

result = {}

def get_news_url(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    for news in soup.select('.news-item'):
        if len(news.select('h2')) > 0:
            news_url = news.select('a')[0]['href']
            yield news_url
            
def get_comment_count(newsurl):
    m = re.search('doc-i(.*).shtml',newsurl)
    newsid = m.group(1)
    comments = requests.get(commentURL.format(newsid))
    jd = json.loads(comments.text.strip('var data='))
    return jd['result']['count']['total']
    

def get_news_detail(newsurl):   
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    result['title'] = soup.select('#artibodyTitle')[0].text
    timesource = soup.select('.time-source')[0].contents[0].strip()
    result['dt'] = datetime.strptime(timesource,'%Y年%m月%d日%H:%M')
    result['newssource'] = soup.select('.time-source span a')[0].text
    result['article'] = ' '.join([p.text.strip() for p in soup.select('#artibody p')[:-2]])
    result['editor'] = soup.select('.article-editor')[0].text
    result['comments'] = '评论数：' + str(get_comment_count(newsurl))

    return result

def main():
    url = 'http://news.sina.com.cn/china/'
    for url in get_news_url(url):
        result = get_news_detail(url)
        for key in result.keys():
            print(result[key])
        print('\n')
        
if __name__ == '__main__':
    main()
    


