#!/usr/bin/env python
# coding:utf-8


import os, sys, json,urllib2,re,time,traceback


# 将要监控的web站点url添加到urllist列表
# urllist = ["http://baidu.com",
#            "http://www.qq.com",
#            "http://www.sina.com.cn/"]


"""
#WEB.txt
#注意VAULES是dict类型，并且花括号里面用单引号(')引住字符串，如果使用双引号(")可能会提示参数异常
#SITENAME|URL|TYPE|VAULES
蜷缩的蜗牛|https://www.along.party|get|{}
蜷缩的蜗牛|https://www.along.party|port|{'id':1,'key':'value'}
"""
files='/etc/zabbix/test/WEB.txt'


fd = open(files,'r')
urllist=[]
for i in fd.readlines():
    if i[0] != '#':
        urllist.append(i.strip('\n'))
fd.close()


# 这个函数主要是构造出一个特定格式的字典，用于zabbix
def web_site_discovery():
    web_list = []
    web_dict = {"data": None}


    for url in urllist:
        url_dict = {}
        url_dict["{#SITENAME}"] = url.split('|')[0]
        url_dict["{#URL}"] = url.split('|')[1]
        url_dict["{#TYPE}"] = url.split('|')[2]
        url_dict["{#VALUES}"] = url.split('|')[3]
        web_list.append(url_dict)


    web_dict["data"] = web_list
    jsonStr = json.dumps(web_dict, sort_keys=True, indent=4)
    return jsonStr




# 这个函数用于测试站点返回的状态码，注意在cmd命令中如果有%{}这种字符要使用占位符代替，否则会报错
def web_site_code_cmd():
    cmd = 'curl --connect-timeout 10 -m 20 -o /dev/null -s -w %s %s' % ("%{http_code}", sys.argv[2])
    reply_code = os.popen(cmd).readlines()[0]
    return reply_code

headers={'Content-Type':'application/json;charset=UTF-8'}
def web_site_code(url,TYPE,VALUES):
    req = None
    if TYPE.lower() == "get":
        req = urllib2.Request(url,headers=headers)
    elif TYPE.lower() == "post":
        data = json.dumps(VALUES)
        req = urllib2.Request(url,data,headers)
    response = None
    try:
        response = urllib2.urlopen(req,timeout=30)
        result = response.code()
        return result
    except urllib2.URLError as e:
        print traceback.format_exc()
        return e
    finally:
        if response:
            response.close()




if __name__ == "__main__":
    try:
        if sys.argv[1] == "web_site_discovery":
            print web_site_discovery()
        elif sys.argv[1] == "web_site_code":
            url = sys.argv[2]
            TYPE = sys.argv[3]
            VALUES = eval(sys.argv[4])
            print web_site_code(url,TYPE,VALUES)
        else:
            print "Pls sys.argv[0] web_site_discovery | web_site_code[URL,TYPE,VALUES]"
    except Exception as msg:
        print traceback.format_exc()
