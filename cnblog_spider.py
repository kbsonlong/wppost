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
    soup = BeautifulSoup(get_info(url),'html.parser', from_encoding='utf-8')
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
        soup = BeautifulSoup(get_info(url), 'html5lib', from_encoding='utf-8')
        try:
            title = soup.find('a',{'class':'postTitle2'}).get_text()
            soup_context = soup.find('div', {
                'class': 'blogpost-body'})
            ###删除script标签，很多时候爬取内容中带有内嵌的广告script
            # [s.extract() for s in soup_context('script')]
            # print context
            images_name =[]
            # 查找图片
            # a_tag = soup.findAll('img')
            # for tag in a_tag:
            #     if tag != None and tag.attrs['src'] != '':
            #         image_url = tag.attrs['src']
            #         image_name = os.path.basename(image_url).split('!')[0]
            #         # 下载图片
            #         get_image(image_url, image_name)
            #         # 删除标签
            #         tag.extract()
            #         images_name.append(image_name)
            #     else:
            #         images_name =[]
            context = "%s \n 本文转载自 <a href='%s' target='_blank'> %s</a> " % (str(soup_context), str(url), str(title))
            news.append(Contexts(title, tags, category, context, images_name))
        except Exception as e:
            logging.error(traceback.format_exc())
            print traceback.format_exc()
    return news


def _get_new_data(page_url):
    response = urllib2.urlopen(page_url)
    html_cont=response.read()
    soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
    print soup
    res_data = {}
    res_data['url'] = page_url

    #<a id="cb_post_title_url" class="postTitle2" href="http://www.cnblogs.com/zhuyuliang/p/5218635.html">Android开发代码规范</a>
    title_node = soup.find('a',class_='postTitle2')
    res_data['title'] = title_node['text']

    #div id='topics'
    summary_node = soup.find('div',class_="post")
    res_data['summary'] = summary_node

    new_tag = soup.new_tag("body")
    new_tag.string = summary_node.encode('utf-8')
    soup.body.replace_with(new_tag)
    res_data['template'] = soup
    print res_data['template']

    return res_data

if __name__ == '__main__':
    ##批量爬取
    url='http://www.cnblogs.com/clsn/category/1131345.html'
    # print get_info(url)
    # links = get_links(url)
    ##爬取某一文章
    links =[ 'https://www.cnblogs.com/huangpeng1990/p/4364341.html','https://www.cnblogs.com/kaynet/p/5861926.html']
    # _get_new_data('http://www.cnblogs.com/clsn/p/8022625.html')
    news = get_context(links,category='ELK',tags=u'elasticsearch,性能调优')
    try:
        for new in news:
            user = {'website': 'https://www.along.party/xmlrpc.php', 'username': '', 'password': '.COM'}
            send_news(user,new)
    except Exception as e:
        print traceback.format_exc()
