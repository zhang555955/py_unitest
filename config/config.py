#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : config.py
# @Author: 橘子
# @Date  : 2021/1/11
# @Desc  : execise
"""
(接口代码封装---请示地址与逻辑代码区分之post请求)
"""
#baseurl接口一般分为测试接口和正式接口

baseurl = 'http://suggest.taobao.com'

#设定登录接口为baseurl
url_logine = baseurl + '/sug?code=utf-8&q=裤子&callback=cb 用例'

#设定注册接口为
url_register = {'注册接口': baseurl + '/sug', 'parmras': {'code': 'utf-8', 'q': '裤子', 'callback': 'cb 用例'}}

#设定首页接口
url_home = baseurl + '/sug?code=utf-8&q=裤子&callback=cb 用例'