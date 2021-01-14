#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : interface_python.py
# @Author: 橘子
# @Date  : 2021/1/11
# @Desc  : execise

import unittest

import requests

from config import config


class JieKoutest(unittest.TestCase):
    def setUp(self):
        print("setUp")
        pass
    def tearDown(self):
        print("tearDown")
        pass
    #测试注册接口的函数
    def test_register(self):
        """  测试注册接口    """

        r = requests.post(config.url_register['注册接口'], config.url_register['parmras'])
        status = r.status_code
        #使用unittest断言

        self.assertEqual(200, r.status_code)
        print(status)
        print(r.content)
        print(r.text)

    def test_login(self):
        """测试登录接口"""
        r  = requests.post(config.url_logine)

        status = r.status_code
        self.assertEqual(200, r.status_code)
        print(status)
        expected = '裤子男夏季'
        j = r.json()
        print(j)
        j['result'][1][1]
        self.assertEqual(expected, j['result'][1][0])
        print(r.text)

if __name__ == '__main__':

    #通过makeSuite方式加载测试用例
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(JieKoutest))
    runner = unittest.TextTestRunner(0)
    runner.run(suite)

