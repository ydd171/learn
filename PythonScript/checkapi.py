#!/usr/bin/env python
  #coding=utf8
import time,os,sched,requests
import smtplib
import string

schedule = sched.scheduler(time.time, time.sleep)
def perform_command(self, inc):
    schedule.enter(inc, 0, perform_command, (self, inc))
    monitoring(self)
def timming_exe(self, inc = 5):
    schedule.enter(inc, 0, perform_command, (self, inc))
    schedule.run()
 
def monitoring(self):
    print("开始监控...")
    try:
        r = requests.get('https://api.github.com')
        print (r.elapsed.total_seconds())
         
        if r.status_code == 200:
            print (u"正常")
        else:
            print (u"异常")
            sendmsg
            print ('邮件已发送....')
    except Exception as e:
        print(e)          
 
def sendmsg():    
     FROM="xxx.com"
     TO="xxx.com"
     PASS="xxx"
     HOST="smtp.sina.com"
     PORT="25"
     SUBJECT="Interface alarm "
     TEXT="The alarm information !"
     BODY= string.join((
             "From: %s" % FROM,
             "To: %s" % TO,
             "Subject: %s" % SUBJECT,
             "",
             TEXT
     ), "\r\n")
     server=smtplib.SMTP()
     server.connect(HOST,"25")
     server.login(FROM,PASS)
     server.sendmail(FROM,TO,BODY)
     server.quit()
         
print("服务监控>>> 一分钟后开始执行(每10秒):")
timming_exe("echo %time%", 10)