# -*- coding:utf-8 -*-

import os
from TestTools import send_email
from TestTools import HTMLTestRunner
import unittest

# 根目录
# upPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
upPath = os.path.dirname(__file__)

# 组装测试套件
def add_case(case_filename='TestCase', rule='test_*.py'):
    case_path = os.path.join(upPath, case_filename)
    # 通过discover()方法自动根据测试目录case_path匹配查找测试用例文件test*.py
    # 并将查找到的测试用例组装到测试套件
    discover = unittest.defaultTestLoader.discover(case_path, pattern=rule, top_level_dir=None)
    return discover


def run_case(all_case, reportfilename='TestResult'):
    report_dirname = os.path.join(upPath, reportfilename)
    if not os.path.exists(report_dirname):
        os.mkdir(report_dirname)
    report_path = os.path.join(report_dirname, 'result.html')

    result = open(report_path, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=result, title=u"QA环境接口自动化测试", description=u"用例执行情况")
    runner.run(all_case)
    result.close()


if __name__ == '__main__':
    all_case = add_case()
    run_case(all_case)
    send = send_email.sendemail()
    send.send_mail()
