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


def pacomment(r):
    for i in range(1,21):
        #url = "http://weibo.cn/1642634100/Dl9ETwUNb?type=comment&page=" + str(i)
        #url = "http://weibo.cn/1642634100/Dm4R54EIJ?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/Dm4XWf6Hi?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/Dm56PkBsQ?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/Dm5jyB2JM?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/Dm5HIbl3R?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/Dm9JdsvgP?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/DmavYleKT?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/DmaNHzQnM?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/DmbLN8IeH?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/Dmm099C2u?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/Dmnd5qYVh?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/Dmnj40gBB?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/DmnxMt43N?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/DmnAqaUpu?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/Dmo6g4KIw?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/DmoqSDjVJ?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/DmslAhUT3?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/DlsoREBjg?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/Dlsq0hgdX?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/DlssYno7L?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/Dlt5b2BFY?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/DlCbf7ZYE?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/DlCcT3X2T?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/DlV4fwtVQ?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/DlXtB3HUf?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/Dm40eD6bP?filter=hot&type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/Dl9ETwUNb?type=comment&page=" + str(i)
	#url = "http://weibo.cn/1642634100/Dlgyl393t?type=comment&page=" + str(i)
	url = "http://weibo.cn/1642634100/DlpvAqCrP?type=comment&page=" + str(i)
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
        # divlabel = str(divlabel)
        for val in divlabel:
            val = str(val)
            cidl = val.find('id=')
            if cidl == -1:
                continue
            cid = val[(cidl+4):(cidl+22)]
            uidl = val.find('href="/u/')
            val2 =  val[(uidl+9):]
            uidr = val2.find('>')
            uid = val2[:(uidr-1)]

            tuname = val2[(uidr+1):]
            unamer = tuname.find('</a>')
            uname = tuname[:unamer]

            tuname = tuname[(unamer+5):]
            contl = tuname.find('</a>:')
            tcont = tuname[(contl+5):]
            contr = tcont.find('</span>')
            cont = tcont[:contr]
            index = cont.find('class="ctt">')
            if index != -1:
                cont = cont[(index+12):]

            data8srcl = tcont.find('class="ct">')
            tdata8src = tcont[(data8srcl+11):]
            data8srcr =  tdata8src.find('</span>')
            data8src  = tdata8src[:data8srcr]
            comments = '{ cid:'+cid +', uid:'+uid+', uname:'+uname+', cont:'+cont+', data8src:'+data8src + '}'
            r.lpush('alphago-comments', comments)
            r.lpush('comments-alphago', cont)
            print cid,uid,uname,cont,data8src

def main():
    # print "weibo spider test begin ~~"
    # mainid = "3275251324"

    r = redis.Redis(host='localhost',port=6379,db=0)
    # fileObj = open("weibo.txt", 'a')

    # keys = r.keys()
    # for uid in keys:
    #     print uid
    #     padata(r,fileObj, uid)
        
    # fileObj.close()
    pacomment(r)

if __name__ == "__main__":
    main()
