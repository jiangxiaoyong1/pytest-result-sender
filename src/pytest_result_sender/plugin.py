#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : plugin.py
# @Time    : 2024/3/16 18:15
# @Author  : 一蒋晓勇
# @Software: PyCharm
from datetime import datetime

import pytest


def pytest_configure():
    # 配置加载完毕之后执行，测试用例执行前执行
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, pytest开始执行")


def pytest_unconfigure():
    # 配置加载完毕之后执行，测试用例执行后执行
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, pytest结束执行")
