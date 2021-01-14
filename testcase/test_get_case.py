#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : test_get_case.py
# @Author: 橘子
# @Date  : 2021/1/11
# @Desc  : execise

import requests
import unittest
from config import config

class Login(unittest.TestCase):
    def Up(self):
        print("setUp")
        pass
    def Down(self):
        print("tearDown")
        pass
    #测试注册接口的函数
    def test_login(self):
        """  测试注册接口    """

        r = requests.get(config.url_home)
        status = r.status_code
        #使用unittest断言
        if status == 200:
            return('测试用例pass')
        else:
            return('测试用例FAIL')
        print(status)
        #判断接口返回内容，存在则PASS，否则为FAIL
        j = r.json()
        if '裤子男夏季1' in str(j):
            print('存在此数据')
        else:
            print('不存在此数据')
        print(j)

if __name__ == '__main__':

    #通过makeSuite方式加载测试用例
    suite = unittest.TestSuite()
    suite.addTest(Login("test_login"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

