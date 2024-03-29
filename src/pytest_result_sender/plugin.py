#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : plugin.py
# @Time    : 2024/3/16 18:15
# @Author  : 一蒋晓勇
# @Software: PyCharm
from datetime import datetime
import pytest
import logging

data = {}


@pytest.hookimpl(tryfirst=True)
def pytest_collection_finish(session: pytest.Session) -> None:
    """用例加载完成之后，包含了全部的用例"""
    logging.info('获取用例总数')
    data['total'] = len(session.items)
    print("用例的总数", data['total'])


@pytest.hookimpl(tryfirst=True)
def pytest_configure():
    # 配置加载完毕之后执行，测试用例执行前执行
    logging.info('用例执行开始时间')
    data['start_time'] = datetime.now()
    # print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, pytest开始执行")
    print(f"{datetime.now()}, pytest开始执行")


@pytest.hookimpl(tryfirst=True)
def pytest_unconfigure():
    # 配置卸载完毕之后执行，测试用例执行后执行
    logging.info('用例执行结束时间')
    data['end_time'] = datetime.now()
    # print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, pytest结束执行")
    print(f"{datetime.now()}, pytest结束执行")
    logging.info("用例执行所有时长")
    data['duration'] = data['end_time'] - data['start_time']
    logging.info("测试用例通过率")
    data['pass_ratio'] = data['passed'] / data['total'] * 100
    data['pass_ratio'] = f"{data['pass_ratio']:.%}"
    print(f'{data["duration"]}')
