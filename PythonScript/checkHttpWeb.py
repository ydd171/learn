#!/usr/bin/python
import pycurl
import time
import sys
import os,sys

url=input("Enter the url you want to query:\n   ")
c=pycurl.Curl()
c.setopt(pycurl.URL,url)
c.setopt(pycurl.CONNECTTIMEOUT,5) #定义超时时间
c.setopt(pycurl.NOPROGRESS,1) #屏蔽下载进度条
c.setopt(pycurl.FORBID_REUSE,1)#完成交互后强制断开连接，不重用
c.setopt(pycurl.MAXREDIRS,1) #指定HTTP重定向的最大数为1
c.setopt(pycurl.DNS_CACHE_TIMEOUT,30) #设置保存DNS信息的时间为30秒

indexfile=open(os.path.dirname(os.path.realpath(__file__))+"/content.txt","wb")
c.setopt(pycurl.WRITEHEADER,indexfile)
c.setopt(pycurl.WRITEDATA,indexfile)

try:
      c.perform()   #提交请求
except Exception as e:
      print("Connection   error:",str(e))
      indexfile.close()
      c.close()
      sys.exit()
dns_time=c.getinfo(c.NAMELOOKUP_TIME) #获取DNS计息时间
connect_time=c.getinfo(c.CONNECT_TIME) #获取建立连接的时间
pretransfer_time=c.getinfo(c.PRETRANSFER_TIME) #获取从建立连接到准备传输的时间
starttransfer_time=c.getinfo(c.STARTTRANSFER_TIME) #获取从建立连接到传输开始的时间
total_time=c.getinfo(c.TOTAL_TIME) #获取传输的总时间
http_code=c.getinfo(c.HTTP_CODE) #获取http状态码
size_downland=c.getinfo(c.SIZE_DOWNLOAD) #获取下载包大小
head_size=c.getinfo(c.HEADER_SIZE) #获取http头部大小
speed_downland=c.getinfo(c.SPEED_DOWNLOAD) # 获取平均下载速度
print("HTTP状态码:%s" % (http_code) )
print("DNS解析时间:%.2f" % (dns_time))
print("建立连接时间:%.2f" % (connect_time))
print("准备传输时间:%.2f:" % (pretransfer_time))
print("传输开始时间:%.2f:" % (starttransfer_time))
print("传输结束总时间:%.2f" % (total_time))
print("下载数据包大小:%d byte" % size_downland)
print("HTTP头部大小:%d byte" % head_size)
print("平均下载速度:%d bytes/s" % speed_downland)
indexfile.close()
c.close()