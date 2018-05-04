#!/usr/bin/env python
# coding=utf-8

import requests
import MySQLdb
import csv,codecs
import logging
import traceback
import ConfigParser,os

from datetime import datetime
from bs4 import BeautifulSoup
from myspider import get_info
from sendEmail import sendmail
import sys
sys.setrecursionlimit(2000)

# logging.basicConfig(filename='logs/monitor.log',level=logging.DEBUG,format='[%(asctime)s -%(name)s - %(levelname)s] %(message)s')

def btc_mark(url,encoding='utf-8'):
    bsObj = requests.session()
    bsObj = BeautifulSoup(get_info(url), 'html.parser')

    boxContain = bsObj.find('div', {'class': 'boxContain'})

    table = boxContain.findAll('table', {'class': 'table maintable'})[0]

    name = ""  # 名字
    market = ""  # 流通市值
    price = ""  # 售价
    count = ""  # 流通数量
    cir_rate = ""  # 流通率
    volume = ""  # 24小时内成交量
    change_1 = ""  #1小时涨跌幅
    change_24 = ""  #24小时涨跌幅
    change_168 = ""  #7天涨跌幅
    ranking=""  ##当前市值排名

    LT = []
    i=0
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 10:
            i += 1
            btc_name = cells[1].a.get_text().strip()
            market = cells[2].get_text()
            price = cells[3].get_text().strip()
            counts = cells[4].get_text().strip()
            cir_rate = cells[5].get_text().strip()
            volume = cells[6].get_text().strip()
            change_1 = cells[7].get_text().strip()
            change_24 = cells[8].get_text().strip()
            change_168 = cells[9].get_text().strip()
            T = [x.encode(encoding) for x in [btc_name, market, price, counts,cir_rate, volume, change_1,change_24,change_168]]
            T.append(i)
            LT.append(T)
        elif len(cells) == 8:
            i += 1
            btc_name = cells[1].a.get_text().strip()
            market = cells[2].get_text()
            price = cells[3].get_text().strip()
            counts = cells[4].get_text().strip()
            volume = cells[5].get_text().strip()
            change_24 = cells[6].get_text().strip()
            T = [x.encode(encoding) for x in[btc_name, market, price, counts, volume, change_24]]
            LT.append(T)
    return LT



def load_config(option, key):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = ConfigParser.ConfigParser()
    path = os.path.join(BASE_DIR, '.config.ini')
    try:
        config.read('.config.ini')
    except:
        config.read(path)
    value = config.get(option, key)
    return value


def insert_db():
    # 打开数据库连接
    db = MySQLdb.connect("172.96.247.193", "root", "kbsonlong", "btchq", port=13306, charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    ##获取行情数据列表
    LT = btc_mark(url)
    try:
        sql = "INSERT INTO hangqing(btc_name,market,price,counts,volume,changes) VALUES (%s,%s,%s,%s,%s,%s)"
        sql_hh = "INSERT INTO hangqing_history (btc_name, market, price, counts,cir_rate, volume, change_1,change_24,change_168,ranking) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # 执行sql语句
        cursor.executemany(sql_hh, LT)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # Rollback in case there is any error
        print e
        db.rollback()
    # 关闭数据库连接
    db.close()
    cursor.close()

def W_csv(filename):
    LT = btc_mark(url)
    nows = datetime.now().strftime( '%Y-%m-%d_%H%M%S' )
    fileName = u"%s%s.csv" % (filename,nows)
    try:
        csvFile = open(fileName,'wt')
        ##设置BOM_UTF8，避免windows下打开csv文件中文乱码
        csvFile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvFile)
        writer.writerow(['名称', '流通市值', '售价', '流通数量', '流通率', '成交量(24)', '涨跌幅(1h)', '涨跌幅(24h)', '涨跌幅(7d)', '市值排名'])
        for row in LT:
            writer.writerow(row)
        csvFile.close()
    finally:
        pass
    return fileName

def show_table(url):
    bsObj = requests.session()
    bsObj = BeautifulSoup(get_info(url), 'html.parser')
    boxContain = bsObj.find('div', {'class': 'boxContain'})
    table = boxContain.findAll('table', {'class': 'table maintable'})[0]
    LT = []
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        print len(cells)
        btc_name = cells[1].a.get_text().strip()
        market = cells[2].a.get_text()
        price = cells[3].a.get_text().strip()
        counts = cells[4].a.get_text().strip('*')
        volume = cells[5].a.get_text().strip()
        change_24 = cells[6].get_text().strip()
        LT.append(u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (btc_name,market,price,counts,volume,change_24))
    context = u'<table border="1"><tr><th>名称</th><th>流通市值</th><th>售价</th><th>流通数量</th><th>成交量(24)</th></tr> %s</table> <p>数据来源于<a href="https://www.feixiaohao.com">非小号</a><br>点击进入<a href="http://www.along.party">蜷缩的蜗牛</a><br></p>' % ''.join(
        s for s in LT)
    return context


##日交易量排行
def btc_vol(url,encoding='utf-8',page=14):
    contexts = []
    for i in range(1, page):
        uri = '%s/%s' % (url,i)
        bsObj = requests.session()
        bsObj = BeautifulSoup(get_info(uri), 'html.parser')
        boxContains = bsObj.findAll('div', {'class': 'vol-rank'})
        for boxContain in boxContains:
            tit = boxContain.find('div',{'class':'rank'}).get_text()
            name = boxContain.a.get_text()
            volume =  boxContain.find('span', {'class': 'volume'}).get_text()
            price =  boxContain.find('span', {'class': 'price'}).get_text()
            contexts.append(u'<tr> <td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'  % (tit,name,volume,price))
    context = u'<table border="1"><tr><th>排名</th><th>名称</th><th>平均成交量</th><th>平均价格</th></tr> %s</table> <p>数据来源于<a href="https://www.feixiaohao.com">非小号</a><br>点击进入<a href="http://www.along.party">蜷缩的蜗牛</a><br></p>' % ''.join(s for s in contexts[0:49])
    return context

if __name__ == '__main__':
    ###成交量
    url = 'https://api.feixiaohao.com/currencies/volrank'
    ##发送邮件
    smtp_server = load_config('smtp', 'smtp_server')
    smtp_user = load_config('smtp', 'smtp_user')
    smtp_pass = load_config('smtp', 'smtp_pass')
    subject = u'数字货币24小时交易量前50预览'
    sendto = [load_config('smtp', 'sendto')]
    context =  btc_vol(url,page=14)
    sendmail(smtp_server, smtp_user, smtp_pass, subject, sendto, context=context)
