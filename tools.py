#coding=utf-8

import os
import types
import zipfile
import calendar
import hashlib

from datetime import datetime
from datetime import timedelta


def get_datetime_by_str(s_datetime):
    """通过str获得datetime
    """
    s_datetime = s_datetime.split('-')
    d = datetime(int(s_datetime[0]), int(s_datetime[1]), int(s_datetime[2]))
    return d

def week_sday():
    """获取本周第一天的日期
    """
    now = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    while now.weekday() != calendar.MONDAY:
        now -= oneday
    print now.strftime('%Y-%m-%d')
    
def week_eday():
    """获取本周最后一天的日期
    """
    now = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    while now.weekday() != calendar.SUNDAY:
        now += oneday
    print now.strftime('%Y-%m-%d')
    
def month_day(date):
    """获取date的月份的天数
    """
    # 20120616
    return calendar.monthrange(int(date[:4]), int(date[4:6]))[1]

def month_sday():
    """获取本月第一天的日期
    """
    d = datetime.now()
    c = calendar.Calendar()
    
    year = d.year
    month = d.month

    return datetime(year ,month, 1).strftime('%Y-%m-%d')

def month_eday():
    """获取本月最后一天的日期
    """
    d = datetime.now()
    c = calendar.Calendar()

    year = d.year
    month = d.month

    days = calendar.monthrange(year, month)[1]
    return (datetime(year,month,1)+timedelta(days=days-1)).strftime('%Y-%m-%d')

def pre_month_sday(d=None):
    """获取上一个月第一天的日期
    """
    if not d:
        d = datetime.now()
    c = calendar.Calendar()
    
    year = d.year
    month = d.month
    
    if month == 1 :
        month = 12
        year -= 1
    else :
        month -= 1

    return datetime(year ,month, 1).strftime('%Y-%m-%d')

def pre_month_eday():
    """获取上一个月最后一天的日期
    """
    d = datetime.now()
    c = calendar.Calendar()

    year = d.year
    month = d.month

    if month == 1:
      month = 12
      year -= 1
    else:
      month -= 1

    days = calendar.monthrange(year, month)[1]
    return (datetime(year,month,1)+timedelta(days=days-1)).strftime('%Y-%m-%d')

#将日期格式进行转换
def trans_date(date):
    date = datetime.strptime(date,'%Y%m%d')
    return date.strftime('%Y-%m-%d')

#在文件中添加内容
def append(file, obj):
    if not obj and obj != 0:
        obj = None
    if type(obj) == types.UnicodeType:
        file.write(obj.encode('utf-8'))
    else:   
        file.write(str(obj))
    file.write('\t')
    return file

#在文件中写入一个列表
def append_collection(file, clt):
    for obj in clt:
        append(file, obj)
    file.write('\n')
    return file

def zip_file(*args):
    zip = zipfile.ZipFile(args[0], 'w')
    for i in range(1,len(args)):
        file = os.path.basename(args[i])
        zip.write(args[i], file, zipfile.ZIP_DEFLATED)
        i+=1
    zip.close()
    
def sha1_qf(contents):
    """sha1加密内容
    """
    hash_qf = hashlib.sha1()
    hash_qf.update(contents)
    hash_value = hash_new.hexdigest()
    
    return hash_value

def maskcard(cardcd):
    if len(cardcd) > 10:
      return cardcd[0:6] + '*' * (len(cardcd) - 10) + cardcd[-4:]
    else:
      return cardcd

def get_ip_address():
    import socket
    localIP = socket.gethostbyname(socket.gethostname())#得到本地ip
    print "local ip:%s "%localIP
    
    iplist = []
    iptuple = socket.gethostbyname_ex(socket.gethostname())
    for i in ipList:
        if i != localIP:
           iplist.extend(i)
           print "external IP:%s" % i


    

    
