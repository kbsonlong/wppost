#coding: utf8

from wppost import get_info
from bs4 import BeautifulSoup
import requests,traceback



def get_context(links,tags='',category=''):
    # links = list(set(get_url(url)))
    link ='https://block.cc/flow/coin'
    bsObj = requests.session()
    bsObj = BeautifulSoup(get_info(link), 'html.parser')
    print bsObj
    conObj =bsObj.findAll('div', {'class': 'chain-coinInfo-item hide-sm'})
    try:

        print conObj

    except Exception as e:
        print traceback.format_exc()
