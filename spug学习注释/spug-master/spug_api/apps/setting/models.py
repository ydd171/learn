# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.db import models
from libs import ModelMixin


class Setting(models.Model, ModelMixin):
    key = models.CharField(max_length=50, unique=True) #定义key的字符串类型，长度，唯一性
    value = models.TextField() #定义value值为大文本模式
    desc = models.CharField(max_length=255, null=True) #排序字符串类型， 长度，可为空

    def __repr__(self):
        return '<Setting %r>' % self.key #实例化对象时，用来做自我介绍用

    class Meta:  #定义构建类
        db_table = 'settings'  #数据库表settings
