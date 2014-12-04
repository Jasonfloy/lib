#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import calendar
from datetime import datetime


def datetimeToTimestamp(date_time):
    '''
    datetime 转换为 timestamp
    '''
    return time.mktime(date_time.timetuple())


def timestampToDateTime(timestamp, millisecond=False):
    '''
    timestamp float
    timestamp 转为 dateTime 类型, 针对 js(精度 millisecond 毫秒) 需要除以 1000
    '''
    if millisecond:
        #timestamp = (decimal.Decimal(timestamp))/1000
        timestamp = timestamp / 1000
    return datetime.datetime.fromtimestamp(timestamp)


def timeLen(date_time):
    '''
    计算距今的时间间隔
    '''
    second = 1
    minute = second * 60
    hour = minute * 60
    day = hour * 24
    month = day * 30
    year = month * 12

    now = datetimeToTimestamp(datetime.now())
    that_time = datetimeToTimestamp(date_time)
    interval = now - that_time

    if interval > year:
        return "%s年前" % int(interval / year)
    elif interval > month:
        return "%s个月前" % int(interval / month)
    elif interval > day * 7:
        return "1周前"
    elif interval > day:
        return "%s天前" % int(interval / day)
    elif interval > hour:
        return "%s小时前" % int(interval / hour)
    elif interval > minute:
        return "%s分钟前" % int(interval / minute)
    elif interval > second:
        return "%s秒前" % int(interval / second)
    else:
        return "1秒前"


def getLastMonth():
    '''
    取上个月 仅要月份
    '''
    return getYearMonth(-1, fmt='%m')


def getYearMonth(months=0, fmt='%Y%m'):
    '''取当年当月
       可以取上月,返回 str
       返回格式: 01
    '''
    date = datetime.datetime.now()
    for i in range(0, abs(months)):
        if months < 0:
            date = date - datetime.timedelta(days=date.day)
        elif months > 0:
            max_days = calendar.monthrange(date.year, date.month)[1]
            date = date + datetime.timedelta(days=max_days - date.day + 1)
    return date.strftime(fmt)
if __name__ == '__main__':
    print timeLen(datetime(2014, 10, 3))
