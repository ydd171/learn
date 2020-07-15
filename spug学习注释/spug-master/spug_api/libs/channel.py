# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from channels.layers import get_channel_layer  #定义将消息发送到渠道层
from asgiref.sync import async_to_sync   #定义同步发送消息的包装器
import uuid

layer = get_channel_layer() #取简化名字


class Channel:
    @staticmethod  #定义不需要接受self参数的方法
    def get_token():   #获取token,有uuid自动生成
        return uuid.uuid4().hex

    @staticmethod
    def send_ssh_executor(hostname, port, username, command, token=None):  #定义执行命令函数
        message = {
            'type': 'exec',
            'token': token,
            'hostname': hostname,
            'port': port,
            'username': username,
            'command': command
        }
        async_to_sync(layer.send)('ssh_exec', message) #同步返回消息message,message作为ssh_exec的值返回。
