# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.http.response import HttpResponse
from django.db.models import QuerySet
from datetime import datetime, date as datetime_date
from decimal import Decimal
import string
import random
import json


# 转换时间格式到字符串
def human_datetime(date=None):
    if date:
        assert isinstance(date, datetime)  #assert断言，相当于if true dosomething, False会立即触发异常。
		                                   #isinstance() 函数来判断一个对象是否是一个已知的类型，类似 type()。
										   #type() 不会认为子类是一种父类类型，不考虑继承关系。
                                           #isinstance() 会认为子类是一种父类类型，考虑继承关系。
                                           #如果要判断两个类型是否相同推荐使用 isinstance()。
    else:
        date = datetime.now()              #如果data不存在，返回当前时间
    return date.strftime('%Y-%m-%d %H:%M:%S')  #格式化时间为字符串输出

# 转换时间格式到字符串(天)
def human_date(date=None):
    if date:
        assert isinstance(date, datetime)
    else:
        date = datetime.now()
    return date.strftime('%Y-%m-%d')

#转换时间为字符串（时分秒）
def human_time(date=None):
    if date:
        assert isinstance(date, datetime)
    else:
        date = datetime.now()
    return date.strftime('%H:%M:%S')


# 解析时间类型的数据
def parse_time(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        if len(value) == 10:
            return datetime.strptime(value, '%Y-%m-%d')
        elif len(value) == 19:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    raise TypeError('Expect a datetime.datetime value')


# 传两个时间得到一个时间差
def human_diff_time(time1, time2):
    time1 = parse_time(time1)
    time2 = parse_time(time2)
    delta = time1 - time2 if time1 > time2 else time2 - time1
    if delta.seconds < 60:
        text = '%d秒' % delta.seconds
    elif delta.seconds < 3600:
        text = '%d分' % (delta.seconds / 60)
    else:
        text = '%d小时' % (delta.seconds / 3600)
    return '%d天%s' % (delta.days, text) if delta.days else text


def json_response(data='', error=''):
    content = AttrDict(data=data, error=error)
    if error:
        content.data = ''
    elif hasattr(data, 'to_dict'): #hasattr() 函数用于判断对象是否包含对应的属性。
        content.data = data.to_dict() #转换为字典
    elif isinstance(data, (list, QuerySet)) and all([hasattr(item, 'to_dict') for item in data]):
	     #如果是list,queryset类型，all函数遍历内部值，并判断内部值是否以字典形式存在。
        content.data = [item.to_dict() for item in data] #将item值转换为字典，总体以列表形式，赋值给content.data
    return HttpResponse(json.dumps(content, cls=DateTimeEncoder), content_type='application/json')
        #将content的值，以日期的返回，cls=DateTimeEncoder 序列化时间为json格式。

# 继承自dict，实现可以通过.来操作元素
class AttrDict(dict):
    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __delattr__(self, item):
        self.__delitem__(item)


# 日期json序列化
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime_date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, Decimal):
            return float(o)

        return json.JSONEncoder.default(self, o)


# 生成指定长度的随机数
def generate_random_str(length: int = 4, is_digits: bool = True) -> str: #（->为函数添加元数据，描述函数的返回类型）
    words = string.digits if is_digits else string.ascii_letters + string.digits
	#digits方法的作用是生成数组，包括0-9 。ascli_letters方法是生成全部字母包括a-z,A-Z.
    return ''.join(random.sample(words, length))
     #从words中随机找出length长度的值，返回。