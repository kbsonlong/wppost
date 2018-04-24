#coding:utf-8
##https://www.kubernetes.org.cn/
from wppost import *
import time,re

def get_url(url):
    bsObj = requests.session()
    bsObj = BeautifulSoup(get_info(url),'html.parser')
    links = []
    for link in bsObj.find('article',{'class':'article-content'}).findAll('li'):
        links.append(link.a['href'])
    return links[::-1]

def get_context(links,tags='',category=''):
    # links = list(set(get_url(url)))
    news =[]
    for link in links:
        if link:
            print link
            bsObj = requests.session()
            bsObj = BeautifulSoup(get_info(link), 'html.parser')
            conObj =bsObj.find('div', {'class': 'content'})
            try:
                title = conObj.find('h1',{'class':'article-title'}).a.get_text()
                soup = conObj.find('article',{'class':'article-content'})
                ###删除script标签，很多时候爬取内容中带有内嵌的广告script
                [s.extract() for s in soup('script')]
                Y = time.strftime("%Y", time.localtime())
                m = time.strftime("%m", time.localtime())
                pattern = re.compile(ur'http(.*)/(.*)/')
                context = u"%s \n 本文转载自 <a href='%s'> %s</a> " % (str(soup),str(link),str(title))
                # context = re.sub(pattern, 'http://www.along.party/wp-content/uploads/%s/%s/' % (Y, m), context)
                image_names=[]
                # 查找图片
                a_tag = conObj.find('img')
                # print a_tag
                # if a_tag != None and a_tag.attrs['src'] != '':
                #     image_url = a_tag.attrs['src']
                #     image_url = image_url.replace(u'https://img.kubernetes.org.cn/',u'https://www.kubernetes.org.cn/img/')
                #     image_name = os.path.basename(image_url)
                #     # 下载图片
                #     get_image(image_url, image_name)
                #     # 删除标签
                #     a_tag.extract()
                #     image_names.append(image_name)
                # else:
                #     image_names = []
                news.append(Contexts(title, tags, category, context, image_names))
            except Exception as e:
                print traceback.format_exc()
    return news




if __name__ == '__main__':
    # url = 'https://www.kubernetes.org.cn/docs'
    classname='content-area'
    # links =  get_url(url)
    links=['https://www.kubernetes.org.cn/3808.html']
    # get_context(links)
    news = get_context(links, category='Kubernetes', tags='Kubernetes')
    try:
        for new in news:
            user = {'website': 'http://www.along.party/xmlrpc.php', 'username': '', 'password': '@.COM'}
            send_news(user,new)
    except Exception as e:
        print traceback.format_exc()