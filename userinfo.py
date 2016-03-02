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

# def paid(r, fileObj):
#     user = r.keys()
#     for u in user:
#         mainid = 'alexyyek'+"/"  
    
#         for i in range(1,10):
#             url = homePage + mainid + fansPage + str(i)
#             print url
#             content = get_content(url)
#             if content == None:
#                 break
#             time.sleep(2)
#             soup = BeautifulSoup(content.text)
#             time.sleep(1)
#             divlabel = soup.select('.c table')
#             time.sleep(1)
#             print "====================="
#             print divlabel
#             for strv in divlabel:
#                 time.sleep(1)
#                 print "------------------"
#                 time.sleep(1)
#                 # get uid
#                 print strv
#                 strv = str(strv)
#                 val = strv
#                 indexs = val.index('http://weibo.cn/')
#                 tmp = val[(indexs+16):]
#                 indexe = tmp.index('">')
#                 val = tmp[:indexe]
#                 if val.find('u/') > -1:
#                     uid = val[2:-1]
#                 else:
#                     uid = val
#                 #get fans
#                 fensl = strv.index('粉丝')
#                 fensr = strv.index('人<br')
#                 fansn = strv[(fensl+6):fensr]

#                 # get name

#                 tmp = strv[0:(fensl-9)]
#                 namel = tmp.rfind('>')
#                 name = tmp[(namel+1):fensl-9]
#                 # name[]
#                 print uid,fansn,name
#                 string = '['+uid +']:|n|'+name+'|fn|'+fansn
#                 fileObj.write(string+'\n')
#                 r.hset(str(uid),'uid',uid)
#                 r.hset(str(uid),'name',name)
#                 r.hset(str(uid),'fans',fansn)
#                 time.sleep(5)
#             time.sleep(5)

def painfo(r, uid):
    
    url = homePage + uid + infoPage
    print url
    content = get_content(url)
    if content == None:
        print "content error"
        return
    time.sleep(1)
    soup = BeautifulSoup(content.text)
    time.sleep(1)
    divlabel = soup.select('.c')
    time.sleep(1)
    print "====================="
    print divlabel
    divlabel = str(divlabel)

    sexl = divlabel.find('性别:')
    if sexl != -1:
        sexval = divlabel[sexl:-1]
        sexr = sexval.index('<br/>')
        sex = sexval[7:sexr]
        print sex
        r.hset(str(uid),'sex',sex)

    areal = divlabel.find('地区:')
    if areal != -1:
        areaval = divlabel[areal:-1]
        arear = areaval.index('<br/>')
        area = areaval[7:arear]
        print area
        r.hset(str(uid),'area',area)

    birhl = divlabel.find('生日:')
    if birhl != -1:
        birhval = divlabel[birhl:-1]
        birhr = birhval.index('<br/>')
        birh = birhval[7:birhr]
        r.hset(str(uid),'birth',birh)

    oriel = divlabel.find('性取向：')
    if oriel != -1:
        orieval = divlabel[oriel:-1]
        orier = orieval.index('<br/>')
        orie = orieval[12:orier]
        print orie
        r.hset(str(uid),'sexorie',orie)

    emol = divlabel.find('感情状况：')
    if emol != -1:
        emoval = divlabel[emol:-1]
        emor = emoval.index('<br/>')
        emo = emoval[15:emor]
        print emo
        r.hset(str(uid),'emotion',emo)

    intrl = divlabel.find('简介:')
    if intrl != -1:
        intrval = divlabel[intrl:-1]
        intrr = intrval.index('<br/>')
        intr = intrval[7:intrr]
        print intr
        r.hset(str(uid),'intro',intr)

    tagl = divlabel.find('标签:')
    if tagl != -1:
        tagval = divlabel[tagl:-1]
        tagr = tagval.index('<br/>')
        tag = tagval[7:tagr]
        print tag
        tagv = ''
        while (1):
            tag1 = tag.find('stag=1')
            if tag1 == -1:
                break
            tag2 = tag[tag1:-1]
            tagrig = tag2.find('</a>')
            tagv = tagv + tag2[8:tagrig] +'|'
            tag = tag2[tagrig:-1]
        r.hset(str(uid),'tag',tagv)
    
    schl = divlabel.rfind('stag=1')
    if schl != -1:
        schval = divlabel[schl:-1]
        schr = schval.index('<br/>')
        sch = schval[7:tagr].index('<div class="c">')
        schoolt = schval[(sch+23):-1]
        schoolr = schoolt.index('<br/>')
        school = schoolt[1:schoolr]
        print school
        r.hset(str(uid),'school',school)
        
def stroeinfo():
    r = redis.Redis(host='localhost',port=6379,db=0)
    fileObj = open("userinfo.txt", 'a')  
    keys = r.keys()
    for uid in keys:
        print uid
        val = r.hgetall(uid)
        fileObj.write(uid+':')
        for k in val:
            fileObj.write(k+':'+val[k]+'|')
        # painfo(r,fileObj)
        fileObj.write('\n')
    fileObj.close()

def main():
    # print "weibo spider test begin ~~"
    # uid = "3275251324"

    # r = redis.Redis(host='localhost',port=6379,db=0)
    # keys = r.keys()
    # for uid in keys:
    #     painfo(r,uid)
    #     print uid
    stroeinfo()
if __name__ == "__main__":
    main()