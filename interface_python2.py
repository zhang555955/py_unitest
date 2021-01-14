#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : interface_python2.py
# @Author: 橘子
# @Date  : 2021/1/11
# @Desc  : execise

# from HTMLTestRunner3 import HTMLTestRunner
from HTMLTestRunner import HTMLTestRunner
import unittest
import time
from common.send_Emain import sendreport

testcase_dir = "./testcase"

discover = unittest.defaultTestLoader.discover(testcase_dir, pattern="*test*.py")

if __name__ == '__main__':
    testreport_dir = "./testreport"

    now = time.strftime("%y-%m-%d %H_%M_%S")
    report_name = testreport_dir + "/" + now + "_test_report.html"

    with open(report_name, 'wb')as f:
        runner = HTMLTestRunner(stream=f, verbosity=1, title="Interface API Test Reporter", description="Test Report")
        runner.run(discover)

    f.close()

    #发送邮件模块
    sendreport()

