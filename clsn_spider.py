#coding:utf-8


from wppost import *

def get_url(url):
    bsObj = requests.session()
    bsObj = BeautifulSoup(get_info(url),'html.parser')
    links = []
    for link in bsObj.find('div',{'class':'small-thumbs'}).findAll('h2'):
        links.append(link.a['href'])
    return links

def get_context(links,tags='',category=''):
    # links = list(set(get_url(url)))
    news =[]
    for link in links:
        if link:
            print link
            bsObj = requests.session()
            bsObj = BeautifulSoup(get_info(link), 'html.parser')
            conObj =bsObj.find('div', {'class': 'entry clearfix'})
            try:
                title = conObj.find('div',{'class':'entry-title'}).h2.get_text()
                print title

                soup = conObj.find('div',{'class':'entry-content'})
                print soup

                ###删除script标签，很多时候爬取内容中带有内嵌的广告script
                # [s.extract() for s in soup('script')]
                context = u"%s \n 本文转载自 <a href='%s'> %s</a> " % (str(soup),str(link),str(title))
                print context
                image_name=''
                # 查找图片
                a_tag = conObj.find('img')
                if a_tag != None and a_tag.attrs['src'] != '':
                    image_url = a_tag.attrs['src']
                    image_name = os.path.basename(image_url).split('!')[0]
                    # 下载图片
                    get_image(image_url, image_name)
                    # 删除标签
                    a_tag.extract()
                else:
                    image_name = ''
                news.append(Contexts(title, tags, category, context, image_name))
            except Exception as e:
                print traceback.format_exc()
    return news




if __name__ == '__main__':
    url = 'https://www.nmtui.com/clsn-ops/play-linux'
    classname='content-area'
    # links =  get_url(url)
    links =['https://www.nmtui.com/clsn/lx382.html']
    # get_context(links)
    news = get_context(links, category='Linux', tags='Linux')
    try:
        for new in news:
            user = {'website': 'http://www.along.party/xmlrpc.php', 'username': '', 'password': '@.COM'}
            send_news(user,new)
    except Exception as e:
        print traceback.format_exc()