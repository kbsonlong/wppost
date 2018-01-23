import requests
from bs4 import BeautifulSoup
from wppost import *

def get_url(url,classname,n=50):
    bsObj = requests.session()
    bsObj = BeautifulSoup(get_info(url),'html.parser')
    links = []
    for link in bsObj.find('main').findAll('a')[0:n]:
        if 'href' in link.attrs:
            href = link.attrs['href']
            if href.startswith('//'):
                href = 'http:' + href
            elif href.startswith('/'):
                href = url + href
            elif href.startswith('?'):
                href=''
            href=href.split('#')[0]
            links.append(href)
    return links

def get_context(url,classname,n=1,tags='',category='转载'):
    links = list(set(get_url(url, classname)))
    news =[]
    for link in links:
        if link:
            # print link
            bsObj = requests.session()
            bsObj = BeautifulSoup(get_info(link), 'html.parser')
            conObj =bsObj.find('main', {'class': 'site-main'})
            try:
                title = conObj.h1.get_text()
                soup = conObj.find('div',{'class':'single-content'})

                ###删除script标签，很多时候爬取内容中带有内嵌的广告script
                [s.extract() for s in soup('script')]
                context = "%s \n 本文转载自 <a href='%s'> %s</a> " % (str(soup),str(link),str(title))
                image_name=''
                # # 查找图片
                # a_tag = conObj.find('img')
                # if a_tag != None and a_tag.attrs['src'] != '':
                #     image_url = a_tag.attrs['src']
                #     image_name = os.path.basename(image_url).split('!')[0]
                #     # 下载图片
                #     get_image(image_url, image_name)
                #     # 删除标签
                #     a_tag.extract()
                # else:
                #     image_name = ''
                news.append(Contexts(title, tags, category, context, image_name))
            except Exception as e:
                print traceback.format_exc()
    return news




if __name__ == '__main__':
    url = 'http://www.ttlsa.com/fbs/page/1/'
    classname='content-area'
    news = get_context(url,classname,category='ELK')
    try:
        for new in news:
            user = readUserConf(2)
            send_news(user,new)
    except Exception as e:
        print traceback.format_exc()