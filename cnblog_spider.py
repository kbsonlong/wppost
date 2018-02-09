#-*- coding:utf-8 -*-
#!/ust/bin/env python
##用于博客园新版爬取
from bs4 import BeautifulSoup
from wppost import *


headers = {'Content-Type':'application/json;charset=UTF-8'}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename='spider.log',level=logging.DEBUG,format='[%(asctime)s -%(name)s - %(levelname)s] %(message)s')



host='https://www.cnblogs.com'

import logging
import traceback





def get_links(url):
    soup = BeautifulSoup(get_info(url),'html.parser')
    hrefs =[]
    for h in soup.findAll('div',{'class':'entrylistItem'}):
        href = h.a.get('href')
        # if  href[:3] != "http":
        #     url = host + href
        # else:
        url = href
        hrefs.append(url)
    return hrefs[::-1]


def get_context(links,tags='',category=''):
    news = []
    for url in links:
        soup = BeautifulSoup(get_info(url), 'html.parser')
        try:
            title = soup.find('a',{'class':'postTitle2'}).get_text()
            # print title
            soup_context = soup.find('div', {
                'class': 'blogpost-body'})
            ###删除script标签，很多时候爬取内容中带有内嵌的广告script
            # [s.extract() for s in soup_context('script')]
            context = "%s \n 本文转载自 <a href='%s'> %s</a> " % (str(soup_context), str(url), str(title))
            # print context
            image_name = ''
            news.append(Contexts(title, tags, category, context, image_name))
        except Exception as e:
            logging.error(traceback.format_exc())
            print traceback.format_exc()

    return news

if __name__ == '__main__':
    ##批量爬取
    url='http://www.cnblogs.com/wangxiaoqiangs/category/973557.html'
    # print get_info(url)
    links = get_links(url)
    ##爬取某一文章
    # url =[ 'https://www.cnblogs.com/wangxiaoqiangs/p/6626076.html']
    news = get_context(links,category='大数据',tags='CDH')
    try:
        for new in news:
            user = {'website': 'http://www.along.party/xmlrpc.php', 'username': 'admin', 'password': 'kbsonlong@GMAIL.COM'}
            send_news(user,new)
    except Exception as e:
        print traceback.format_exc()