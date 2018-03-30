#-*- coding:utf-8 -*-
#!/ust/bin/env python
##用于www.centos.bz爬取
from bs4 import BeautifulSoup
from wppost import *


headers = {'Content-Type':'application/json;charset=UTF-8'}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename='spider.log',level=logging.DEBUG,format='[%(asctime)s -%(name)s - %(levelname)s] %(message)s')



host='https://www.centos.bz'

import logging
import traceback





def get_links(url):
    soup = BeautifulSoup(get_info(url),'html.parser')
    hrefs =[]
    for h in soup.findAll('article'):
        href = h.h2.a.get('href')
        # if  href[:3] != "http":
        #     url = host + href
        # else:
        url = href
        hrefs.append(url)

    # print hrefs
    return hrefs[::-1]


def get_context(links,tags='',category=''):
    news = []
    for url in links:
        soup = BeautifulSoup(get_info(url), 'html.parser')
        try:
            title = soup.find('header',{'class':'article-header'}).h1.get_text()
            # print title

            soup_context = soup.find('article',{'class':'article-content'})

            ###删除script标签，很多时候爬取内容中带有内嵌的广告script
            [s.extract() for s in soup_context('div',{'class':'content-index'})]
            [s.extract() for s in soup_context('blockquote')]
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

    # print get_info(url)
    # for page in range(7,0,-1):
    #     url = 'https://www.centos.bz/tag/kubernetes/page/%s/' % page
    #     links = get_links(url)
    # ##爬取某一文章
        links =[ 'https://www.centos.bz/2017/10/%E4%BD%BF%E7%94%A8docker%E5%92%8Ckubernetes%E6%9E%84%E5%BB%BA%E5%8F%AF%E4%BC%B8%E7%BC%A9%E7%9A%84%E5%BE%AE%E6%9C%8D%E5%8A%A1/']
        news = get_context(links,category='Kubernetes',tags='Kubernetes')
        # try:
        #     for new in news:
        #         user = {'website': 'http://www.along.party/xmlrpc.php', 'username': '', 'password': '@GMAIL.COM'}
        #         send_news(user,new)
        # except Exception as e:
        #     print traceback.format_exc()