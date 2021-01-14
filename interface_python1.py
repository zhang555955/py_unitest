#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : interface_python1.py
# @Author: 橘子
# @Date  : 2021/1/11
# @Desc  : execise
import requests
import unittest,time

if __name__ == '__main__':
    suite_get = unittest.TestLoader().loadTestsFromNames(['testcase.test_get_case'])
    suite_post = unittest.TestLoader().loadTestsFromNames(['testcase.test_post_case'])
    runner = unittest.TextTestRunner()
    runner.run(suite_get)
    runner.run(suite_post)