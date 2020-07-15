# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from functools import lru_cache
from apps.setting.models import Setting


class AppSetting:
    keys = ('public_key', 'private_key', 'mail_service', 'api_key', 'spug_key', 'ldap_service')

    @classmethod
    @lru_cache(maxsize=64)
    def get(cls, key):
        info = Setting.objects.filter(key=key).first() #查找数据库内对应的key,返回查到的第一个元素，赋值给info
        if not info: #如果info不存在
            raise KeyError(f'no such key for {key!r}') #返回错误信息
        return info.value #如果查找key正常，返回key的值

    @classmethod
    def get_default(cls, key, default=None):
        info = Setting.objects.filter(key=key).first()
        if not info:
            return default
        return info.value

    @classmethod
    def set(cls, key, value, desc=None): #定义key设置方法
        if key in cls.keys: #如果key存在
            Setting.objects.update_or_create(key=key, defaults={'value': value, 'desc': desc}) #设置key
        else:
            raise KeyError('invalid key') #保存信息
