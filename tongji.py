#-*- coding:utf-8 -*-
import urllib2
import requests
import gzip
import StringIO
import ConfigParser
import sys
import time
import re
import redis


        
def Init(r):
    for i in range(-50,51):
        r.hset("tongji-zhengshuang",i,0)

def Tongji(r):
    length = r.llen('result-zhengshuang')
    for i in range(0,length):
        val = r.lindex('result-zhengshuang',i)
        if val != None:
            print val
            num = r.hget('tongji-zhengshuang',int(float(val)))
            if num != None:
                num = int(num)
                num = num + 1
                print num
                r.hset('tongji-zhengshuang',int(float(val)),num)

def Write(r,fileObj):
    su = 0
    for k in range(-50,51):
        print k
        val = r.hget('tongji-zhengshuang', k)
        if k == -2:
            fileObj.write(str(su) +'\n')
            su = 0
        elif k == -1:
            fileObj.write(val +'\n')
        elif k == 0:
            fileObj.write(val +'\n')
        elif k == 1:
            fileObj.write(val +'\n')
        elif k == 50:
            fileObj.write(str(su) +'\n')
        else:
            su = su + int(val)

def main():
    r = redis.Redis(host='localhost',port=6379,db=0)
    fileObj = open("res.txt", 'w')  
    # keys = r.keys("weibo-*")
    # for uid in keys:
    #     getweibo(r, fileObj, uid)
    #     # print val
    # fileObj.close()
    # Init(r)
    # Init(r)
    # Tongji(r)
    Write(r,fileObj)
    fileObj.close()

if __name__ == "__main__":
    main()