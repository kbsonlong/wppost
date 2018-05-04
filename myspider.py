#!/usr/bin/env python
# coding=utf-8


import logging
import urllib2
import traceback

headers = {'Content-Type':'application/json;charset=UTF-8'}

logging.basicConfig(filename='monitor.log',level=logging.DEBUG,format='[%(asctime)s -%(name)s - %(levelname)s] %(message)s')



def get_info(url):
    req = urllib2.Request(url, headers=headers)
    response = None
    try:
        response = urllib2.urlopen(req, timeout=10)
        # print response.getcode()
        # print response.geturl()
        # print response.info()
        result = response.read()
        logging.info("Success")
        return result

    except urllib2.URLError as e:
        logging.error(e)
        if hasattr(e, 'code'):
            print 'Error code:', e.code
            # print e.read()
            print e.geturl()
            print e.info()
        elif hasattr(e, 'reason'):
            print 'Reason:', e.reason
    except:
        pass
    finally:
        if response:
            response.close()


def Format_Alarm(url):
    infos = get_info(url)['result']
    try:
        if len(infos) == 0:
            logging.info('Not Alarm info!!')
        else:
            return infos
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())