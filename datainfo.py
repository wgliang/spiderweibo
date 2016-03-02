#-*- coding:utf-8 -*-
import urllib2
import requests
import gzip
import StringIO
import ConfigParser
import sys
from bs4 import BeautifulSoup
import time
import re
import MySQLdb
import redis

homePage = 'http://weibo.cn/'
infoPage = '/info'
fansPage = 'fans?page='
weiboPage = 'u/'


def get_content(toUrl):
    """ Return the content of given url

        Args:
            toUrl: aim url
            count: index of this connect

        Return:
            content if success
            'Fail' if fail
    """

    cf = ConfigParser.ConfigParser()
    cf.read("config.ini")
    cookie = cf.get("cookie","cookie")
    cookdic = dict(Cookie=cookie)

    try:
        req = requests.get(toUrl,cookies = cookdic, timeout=100)
    except:
        return None
    if req.status_code != requests.codes.ok:
        print "haven't get 200, status_code is: "+str(req.status_code);
        # sys.exit(-1)
        return None
    return req


def padata(r, fileObj, uid):
    for i in range(1,10):
        url = homePage + uid + '?page=' + str(i)
        print url
        content = get_content(url)
        if content == None:
            break
        time.sleep(2)
        soup = BeautifulSoup(content.text)
        time.sleep(1)
        divlabel = soup.select('.c')
        time.sleep(1)
        print "====================="
        # print divlabel
        flag = 0
        for weibo in divlabel:
            flag = 1
            weibo =str(weibo)
            # print weibo
            idl = weibo.find('id=')
            if idl != -1:
                idv = weibo[(idl+4):(idl+15)]
                # print idv

                weibot = weibo[(idl+40):]
                index = weibot.find('转发了')
                if index == 0:
                    continue
                else:
                    weibor = weibot.find('</span>')
                    weibov = weibot[:weibor]

                zanl = weibot.find('赞[')
                zant = weibot[(zanl+4):]
                zanr = zant.find(']')
                zanv = zant[:zanr]
                # print zanv

                zhuanl = weibot.find('转发[')
                zhuant = weibot[(zhuanl+7):]
                zhuanr = zhuant.find(']')
                zhuanv = zhuant[:zhuanr]
                # print zhuanv

                comml = weibot.find('评论[')
                commt = weibot[(comml+7):]
                commr = commt.find(']')
                commv = commt[:commr]
                # print commv

                shoul = weibot.find('收藏</a>')
                srct = weibot[shoul:]
                srcl = srct.find('class="ct"')
                srcv = srct[(srcl+11):]
                timer = srcv.find('来自')
                timev = srcv[:(timer-2)]
                srcr = srcv.find('</span></div>')
                srcv = srcv[(timer+6):srcr]
                # print timev,srcv
                weibos = '{ wid:'+idv +', weiboinfo:'+weibov+', zan:'+zanv+', comm:'+commv+', zhuan:'+zhuanv+', src:'+srcv+', time:'+timev+' }'
                print weibos
                r.lpush(str('weibo-' + uid), weibos)
                fileObj.write(weibos+'\n')
                # idr = idt.find('">')
                # idv = idt[idl:idr]
                # print idv
        if flag == 0:
            break
        

def main():
    # print "weibo spider test begin ~~"
    # mainid = "3275251324"

    r = redis.Redis(host='localhost',port=6379,db=0)
    fileObj = open("weibo.txt", 'a')

    keys = r.keys()
    for uid in keys:
        print uid
        padata(r,fileObj, uid)
        
    fileObj.close()

if __name__ == "__main__":
    main()