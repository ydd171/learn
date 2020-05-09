from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse,request,HttpResponseRedirect
from .forms import UserForm
import time, datetime
import os
import subprocess
import paramiko

def login(request):
    if request.session.get('is_login',None):
        return HttpResponseRedirect('/asbui/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            print(username,password)

            #user = 'admin108'
               #user = models.User.objects.get(name=username)
               #username == admin108:
            if username == 'admin108':
                print(username)
                if password == '10810086':
                    request.session['is_login'] = True
                    request.session['user_name'] = username
                    return HttpResponseRedirect('/asbui/index')
                else:
                    message = "密码不正确！"
            else:
                message = "用户不存在！"
            return render(request, 'asbui/login.html', locals())

    login_form = UserForm()
    return render(request, 'asbui/login.html', locals())
def logout(request):
    request.session.clear()
    return HttpResponseRedirect('login')
def historylog(request):
    if not request.session.get('is_login',None):
        return HttpResponseRedirect('/asbui/login')
    logfile = open('historylog/historylog','r')
    listlog = logfile.readlines()
    messagelog = listlog[-50::]
    return render(request,'asbui/historylog.html',{"messagelog":messagelog})

@accept_websocket
def index(request):
    if not request.session.get('is_login',None):
        return HttpResponseRedirect('/asbui/login')
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'asbui/index.html')
    else:
        for message in request.websocket:
            message = message.decode('utf-8')  # 接收前端发来的数据
            print(message)
            listn = message.strip(',').split(',')
            print(listn)
            #print(parameter)
            #if listn[1] == '12345':
             #   print(ok)
             #   continue
            if listn[0] == 'update_time':
                command = 'bash /script/update_time.sh' + ' ' + listn[1] + ' '  + '"' + listn[2] + '"'  # 这里是要执行的命令或者脚本
                print(command)
                execute(request, command)

            elif listn[0] == 'Execute_all':#这里根据web页面获取的值进行对应的操作
                if len(listn) == int(4):
                    command = 'bash /script/Execute_all.sh' + ' ' + listn[1] + ' ' + listn[2] + ' ' + listn[3] #这里是要执行的命令或者脚本
                else:
                    command = 'bash /script/Execute_all.sh' + ' ' + listn[1] + ' ' + listn[2]
                print(command)
                execute(request,command)
            else:
                request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))
def execute(request,command):
    # 远程连接服务器
    hostname = 'qa1'
    username = 'root'
    password = 'root1234'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    # 务必要加上get_pty=True,否则执行命令会没有权限
    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
    # result = stdout.read()
    # 循环发送消息给前端页面
    while True:
        nextline = stdout.readline().strip()  # 读取脚本输出内容
        # print(nextline.strip())
        request.websocket.send(nextline.encode('utf-8'))  # 发送消息到客户端
        # 判断消息为空时,退出循环
        if not nextline:
            request.websocket.send("the end!!!")
            break
    ssh.close()  # 关闭ssh连接
    #增加历史记录功能
    now = datetime.datetime.now()
    now_time = now.strftime("%Y-%m-%d %H:%M:%S")
    fp = open('historylog/historylog', "a", encoding="utf-8")
    fp.write(str(now_time) + "   " + command + "\n")
    fp.close()