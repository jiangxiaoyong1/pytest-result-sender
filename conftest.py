#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : conftest.py
# @Time    : 2024/3/17 14:04
# @Author  : 一蒋晓勇
# @Software: PyCharm
import time
from datetime import datetime
import pytest
import logging

import requests

data = {
    "passed": 0,
    "failed": 0,
}


def pytest_addoption(parser):
    """识别pytest.ini配置"""
    parser.addini(
        'send_when',
        help='什么时候发送测试结果，every：每次执行完自动发送结果，on_fail:用例存在执行失败发送结果'
    )
    parser.addini(
        'send_api',
        help='发送到哪'
    )


def pytest_runtest_logreport(report: pytest):
    if report.when == 'call':
        # print("本次用例执行结果：", report.outcome)
        data[report.outcome] += 1


@pytest.hookimpl(tryfirst=True)
def pytest_collection_finish(session: pytest.Session) -> None:
    """用例加载完成之后，包含了全部的用例"""
    logging.info('获取用例总数')
    data['total'] = len(session.items)
    print("用例的总数:", data['total'])


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest):
    # 配置加载完毕之后执行，测试用例执行前执行
    data['start_time'] = datetime.now()
    print(f"{datetime.now()}, pytest开始执行")
    # 动态获取pytest.ini内容
    data['send_when'] = config.getini('send_when')
    data['send_api'] = config.getini('send_api')


@pytest.hookimpl(tryfirst=True)
def pytest_unconfigure():
    # 配置卸载完毕之后执行，测试用例执行后执行
    data['end_time'] = datetime.now()
    # print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, pytest结束执行")
    print(f"{datetime.now()}, pytest结束执行")
    logging.info("用例执行所有时长")
    data['duration'] = data['end_time'] - data['start_time']
    logging.info("测试用例通过率")
    data['pass_ratio'] = data['passed'] / data['total'] * 100
    data['pass_ratio'] = f"{data['pass_ratio']:.2f}%"
    send_result()


def send_result():
    """如果配置了失败，但是实际用例执行全部通过则发送测试结果，否则不发送"""
    if data['send_api'] == 'on_fail' and data['failed'] == 0:
        return
    if not data['send_api']:
        return
    url = data['send_api']  # 动态获取制定发送结果地址
    content = f"""
        pytest自动化测试结果
        测试时间：{data['end_time']}
        用例数量：{data['total']}
        执行时长：{data['duration']}
        测试通过：<font color="green">{data['passed']}</font>
        测试失败：<font color="red">{data['failed']}</font>
        测试通过率：{data['pass_ratio']}%
        测试报告地址：http:baidu.com
        """
    try:
        requests.post(url, json={"msgtype": "markdown","markdown": {"content": content}})
    except Exception:
        pass
