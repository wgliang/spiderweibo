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

# def getfansnum(page):
#     soup = BeautifulSoup(page.text)
#     time.sleep(1)
#     divlabel = soup.select('.pa')

#     print "pages is ",divlabel


# def spider_id(usid, r, fileObj):
#     if fileObj == 10:
#         return
#     print "weibo spider test begin ~~"
#     mainid = usid+"/"  
    
#     for i in range(10):
#         url = homePage + mainid + fansPage + str(i)
#         print url
#         content = get_content(url)
#         if content == None:
#             break
#         soup = BeautifulSoup(content.text)
#         time.sleep(1)
#         divlabel = soup.select('.c table')

#         fileObj = fileObj +1
#         for strv in divlabel:
#             # get uid
#             print strv
#             strv = str(strv)
#             val = strv
#             indexs = val.index('http://weibo.cn/')
#             tmp = val[(indexs+16):]
#             indexe = tmp.index('">')
#             val = tmp[:indexe]
#             if val.find('u/') > -1:
#                 uid = val[2:-1]
#             else:
#                 uid = val
#             #get fans
#             fensl = strv.index('粉丝')
#             fensr = strv.index('人<br')
#             fansn = strv[(fensl+6):fensr]

#             # get name

#             tmp = strv[0:(fensl-9)]
#             namel = tmp.rfind('>')
#             name = tmp[(namel+1):fensl-9]
#             # name[]
#             print uid,fansn,name
#             string = '['+uid +']:|n|'+name+'|fn|'+fansn
#             # fileObj.write(string+'\n')
#             r.hset(str(uid),'uid',uid)
#             r.hset(str(uid),'name',name)
#             r.hset(str(uid),'fans',fansn)
#             time.sleep(1)
#             spider_id(uid,r,fileObj)
#         time.sleep(5)

def paid(r, fileObj):
    user = r.keys()
    for u in user:
        mainid = u+"/"  
    
        for i in range(1,10):
            url = homePage + mainid + fansPage + str(i)
            print url
            content = get_content(url)
            if content == None:
                break
            time.sleep(2)
            soup = BeautifulSoup(content.text)
            time.sleep(1)
            divlabel = soup.select('.c table')
            time.sleep(1)
            print "====================="
            print divlabel
            for strv in divlabel:
                time.sleep(1)
                print "------------------"
                time.sleep(1)
                # get uid
                print strv
                strv = str(strv)
                val = strv
                indexs = val.index('http://weibo.cn/')
                tmp = val[(indexs+16):]
                indexe = tmp.index('">')
                val = tmp[:indexe]
                if val.find('u/') > -1:
                    uid = val[2:-1]
                else:
                    uid = val
                #get fans
                fensl = strv.index('粉丝')
                fensr = strv.index('人<br')
                fansn = strv[(fensl+6):fensr]

                # get name

                tmp = strv[0:(fensl-9)]
                namel = tmp.rfind('>')
                name = tmp[(namel+1):fensl-9]
                # name[]
                print uid,fansn,name
                string = '['+uid +']:|n|'+name+'|fn|'+fansn
                fileObj.write(string+'\n')
                r.hset(str(uid),'uid',uid)
                r.hset(str(uid),'name',name)
                r.hset(str(uid),'fans',fansn)
                time.sleep(5)
            time.sleep(5)

def main():
    # print "weibo spider test begin ~~"
    # mainid = "3275251324"

    r = redis.Redis(host='localhost',port=6379,db=0)
    fileObj = open("user.txt", 'w+')   
    # spider_id(mainid, r, fileObj)
    paid(r,fileObj)
    fileObj.close()

if __name__ == "__main__":
    main()