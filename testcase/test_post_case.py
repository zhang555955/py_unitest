#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : test_post_case.py
# @Author: 橘子
# @Date  : 2021/1/11
# @Desc  : execise

import requests
from config import config
import unittest

class Register(unittest.TestCase):
    def Up(self):
        print("setUp")
        pass
    def Down(self):
        print("tearDown")
        pass

    #测试注册接口函数
    def test_register(self):
        """测试注册接口"""
        #发送post请求，通过config文件获取接口url和接口的参数，如果参数更改了，咱们就修改config文件就可以
        r = requests.post(config.url_register['注册接口'], config.url_register['parmras'])
        status = r.status_code
        self.assertEqual(200, r.status_code)
        return (status)
        print(r.content)
        print(r.text)

    #测试登录接口函数
    def test_login(self):
        """        测试登录接口   """
        #因为发送的get请求，参数是跟在接口的后面的，所以不用通过字典形式获取
        r = requests.post(config.url_logine)
        status = r.status_code
        self.assertEqual(200, r.status_code)

        return (status)
        print(r.json())
        #预期结果在接口返回结果后，查看接口里有没有此值，断言
        expected = '88'
        #获取接口的返回信息
        j = r.json()
        print(j)
        j['result'][1][1]
        self.assertEqual(expected, j['result'][1][0])
        print(r.text)

if __name__ =='__main__':
    suite = unittest.TestSuite()
    suite.addTest(Register("test_register"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

