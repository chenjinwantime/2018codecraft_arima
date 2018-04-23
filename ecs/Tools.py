#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-12 10:30:54
# @Author  : mianhk (yugc666@163.com)
# @Link    : ${link}
# @Version : $Id$


'''
    工具类
'''
import param_info
import math

OPT_OBJECT = {
    'CPU': 0,
    'MEM': 1
}
# 预测时间粒度
# 训练数据粒度
TIME_GRAIN_HOUR = 0
TIME_GRAIN_DAY = 1
# TIME_GRAIN_MORE_DAY = 2
# TIME_GRAIN_SEVEN_DAY=7

# 训练时间粒度
TRAIN_GRAIN_DAYS=7

# 检查dict中是否存在key
def isContainKey(dic, key):
    return key in dic.keys()


def calcu_days(begin_day,end_day):
    predict_time_grain=0
    st_year, st_month, st_day = begin_day.split(' ')[0].split('-')
    et_year, et_month, et_day = end_day.split(' ')[0].split('-')
    day_index = (int(et_year) - int(st_year)) * 365 + \
                                 (int(et_month) - int(st_month)) * 30 + (int(et_day) - int(st_day))
    return day_index
    # pass

    
def getmin_max(A):
    mini=10000.0
    maxi=0.0
    for i in range(len(A)):
        if mini>A[i]:
            mini=A[i]
        elif maxi<A[i]:
            maxi=A[i]
    return mini,maxi

def average(A):
    averageh=0.0
    for i in range(len(A)):
        averageh+=A[i]
    averageh=averageh/len(A)
    return averageh
def delat(A,averagehi):
    delta=0.0
    for i in range(len(A)):
        delta+=(A[i]-averagehi)*(A[i]-averagehi)
    delta=delta/len(A)
    return delta
       
        