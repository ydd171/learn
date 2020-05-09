from channels.generic.websocket import WebsocketConsumer
import json
from . import models
from .views import history_log
import paramiko
import uuid

class ChatConsumer(WebsocketConsumer):
    def receive(self, text_data):
        ssh = paramiko.SSHClient()
        text_data_json = json.loads(text_data)
        stopexec = text_data_json['stopexec']
        if stopexec == 1:
            ssh.close()
            print(stopexec)
            pass
        else:
            jid = text_data_json['jobid']
            hostname = text_data_json['hostname']
            parameter = text_data_json['parameter']

            #与数据库信息对比，取出执行命令所需要参数
            hostname_tmp = models.add_host.objects.get(hostname=hostname)
            keyname = hostname_tmp.keyname
            username = hostname_tmp.username
            port = int(hostname_tmp.port)
            private_key = paramiko.RSAKey.from_private_key_file('pemkey/' + keyname)

            #执行shell脚本传输命令
            tran = paramiko.Transport((hostname, port))
            tran.connect(username=username, pkey=private_key)
            sftp = paramiko.SFTPClient.from_transport(tran)
            localpath = 'job/' + jid
            remotepath = '/tmp/' + jid
            sftp.put(localpath, remotepath)
            tran.close()

            exec_history = "%s.log" % uuid.uuid1()
            history_log(jid,hostname,exec_history)
            #执行命令，回传执行结果。
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname, port=port, username=username, pkey=private_key)
            stdin, stdout, stderr = ssh.exec_command('bash ' + remotepath + " " + parameter, get_pty=True)
            with open('static/history_log/' + exec_history,'w+' ) as hl:
                while True:
                    nextline = stdout.readline().strip()  # 读取脚本输出内容
                    self.send(text_data=json.dumps({
                    'message': nextline
                    }))

                    hl.writelines(nextline + '\n')

                    if not nextline:
                        self.send(text_data=json.dumps({
                            'message': "the end!"
                        }))
                        #self.close()
                        break
                hl.close()
            #删除传输到host主机上面的临时脚本，关闭连接
            ssh.exec_command('rm -f ' + remotepath)
            ssh.close()
