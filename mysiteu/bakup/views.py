from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import paramiko

@accept_websocket
def index(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'asbui/index.html')
    else:
        listn = []
        for message in request.websocket:
            message = message.decode('utf-8')  # 接收前端发来的数据
            listn.append(message)
            print(listn)
            if len(listn) == int(1):
                print(len(listn))
                continue
            #print(parameter)
            #if listn[1] == '12345':
             #   print(ok)
             #   continue
            elif listn[1] == 'update_time':
                command = 'bash /tmp/date.sh' + ' ' + '"' + listn[0] + '"'  # 这里是要执行的命令或者脚本
                print(command)
                # 远程连接服务器
                hostname = '172.21.161.117'
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
                        break
                ssh.close()  # 关闭ssh连接

            elif listn[1] == 'backup_all':#这里根据web页面获取的值进行对应的操作
                command = 'bash /tmp/test.sh'#这里是要执行的命令或者脚本
                # 远程连接服务器
                hostname = '172.21.161.117'
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
                    #print(nextline.strip())
                    request.websocket.send(nextline.encode('utf-8')) # 发送消息到客户端
                    # 判断消息为空时,退出循环
                    if not nextline:
                        break

                ssh.close()  # 关闭ssh连接
            else:
                request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))
