# -*- coding:utf-8 -*-
##爬取文章到wordpress

import urllib2
import logging
import sys,os
import traceback
import ssl
import requests
import urllib
import configparser
import random
from bs4 import BeautifulSoup
from wordpress_xmlrpc import Client,WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media

#全局取消证书验证
ssl._create_default_https_context = ssl._create_unverified_context
reload(sys)
sys.setdefaultencoding('utf-8')


#新闻类
class Contexts(object):
	def __init__(self,title,tags,category,content,image_name):
		self.title = title     #标题
		self.tags=tags         #标签
		self.category=category #分类
		self.content=content   #内容
		self.image_name=image_name

headers={'Content-Type':'application/json;charset=UTF-8','User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

#读取WordPress站点配置
def readUserConf(n=1):
    cf = configparser.ConfigParser()
    cf.read('wp.conf')
    useri = 'user0%s' % random.randint(1, n)
    website=cf.get('web',useri).split('|')[0]
    username=cf.get('web',useri).split('|')[1]
    password=cf.get('web',useri).split('|')[2]
    user={'website': website, 'username': username, 'password': password}
    return user


#加载user_agents配置文件
def load_user_agent():
	user_agents=[]
	fp = open('user_agents', 'r')
	line  = fp.readline().strip('\n')
	while(line):
		user_agents.append(line)
		line = fp.readline().strip('\n')
	fp.close()
	return user_agents

#下载图片
'''
将图片保存到本地
'''
def get_image(image_url,image_name):
    # os.makedirs('images',exist_ok=True)mport
    save_path = 'images/'+image_name
    import json
    print json.dumps(image_url)
    print image_url.decode('utf-8')
    image_url= urllib.unquote(urllib.quote(image_url))
    pic_file = urllib.urlopen(image_url).read()
    f = open(save_path, "wb")
    f.write(pic_file)
    f.close()

#上传图片
'''
根据图片路径将图片上传到wordpress

返回attachment_id
'''
def upload_image(image_name,client):
	data={
		'name':image_name,
		'type':'image/jpeg'
	}
	with open('images/'+image_name, 'rb') as img:
		data['bits'] = xmlrpc_client.Binary(img.read())
	response = client.call(media.UploadFile(data))
	#print('上传了--->'+image_name)
	attachment_id = response['id']
	return attachment_id


def get_proxy():
    return requests.get("http://172.96.247.193:8080/get/").content

def delete_proxy(proxy):
    requests.get("http://172.96.247.193:8080/delete/?proxy={}".format(proxy))


def my_spider(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    proxy = get_proxy()
    print proxy
    try:
        response = requests.get(url, proxies={"http": "http://{}".format(proxy)}, headers = headers,timeout = 10)
        return response.content
    except:
        print "error" ,traceback.format_exc()
        logging.info(url)
        ##删除代理池中代理
        delete_proxy(proxy)

def get_info(url):
    ##避免python2.7 ssl不信任https证书验证
    context = ssl._create_unverified_context()
    postData = {
        'origURL': 'http://www.nmtui.com',
        'domain': 'nmtui.com',
    }
    req = urllib2.Request(url,headers=headers)
    response = None
    # retry_count = 5
    # proxy = get_proxy()
    # print proxy

    try:
        ###添加代理访问
        # proxies = {"http": "http://{}".format(proxy)}
        # proxy_s = urllib2.ProxyHandler(proxies)
        # opener = urllib2.build_opener(proxy_s)
        # urllib2.install_opener(opener)
        response = urllib2.urlopen(req, timeout=5,context=context)
        contexts = response.read()
        return contexts

    except urllib2.URLError as e:
        logging.error(e)
        print traceback.format_exc()
        if hasattr(e, 'code'):
            print 'Error code:', e.code
            return {'code':e.code}
        elif hasattr(e, 'reason'):
            print 'Reason:', e.reason

    finally:
        if response:
            response.close()
    # ##出错5次, 删除代理池中代理
    # delete_proxy(proxy)


def send_news(user,news):
    wp=Client(user['website'],user['username'],user['password'])
    post=WordPressPost()
    if news.image_name!='':
        print news.title
        for image in news.image_name:
            attachment_id=upload_image(image,wp)
            post.thumbnail = attachment_id
    post.title=news.title
    post.content=str(news.content)
    post.post_status ='publish'
    post.terms_names={
        'post_tag':news.tags,
        'category':[news.category]
    }
    wp.call(NewPost(post))


if __name__ == '__main__':
    print get_info("http://ip.catr.cn/")