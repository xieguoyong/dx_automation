# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import unittest
import handle
from TestTools import data_read
from parameterized import parameterized
import traceback

# 定义测试类，父类为unittest.TestCase。
# 可继承unittest.TestCase的方法，如setUp和tearDown方法，不过此方法可以在子类重写，覆盖父类方法。
# 可继承unittest.TestCase的各种断言方法
class TestMain(unittest.TestCase):
    # 设定输出的用例报告中的用例名格式
    # *************add.3*************
    def custom_name_func(testcase_func=None, param_num=None, param=None):
        return "%s_%s_%s" % ("test", str(param.args[0]), str(param.args[3]))

    # @classmethod 是一个函数修饰符，它表示接下来的是一个类方法，而对于平常我们见到的则叫做实例方法。
    # 类方法的第一个参数cls，而实例方法的第一个参数是self，表示该类的一个实例
    # 初始化运行
    # ********run.1*********
    @classmethod
    def setUpClass(cls):
        print u"________用例执行_________"
        cls._handle = handle.handle()
        setupsheet = data_read.get_xls('dict', u"dx_interauto_qa_case.xls", 'setup')
        cls._handle.set_global(setupsheet)

    # 读取用例文件中的用例（Excel文件名,sheet名）
    # ******add.1******
    case = data_read.get_xls('list', u'dx_interauto_qa_case.xls', 'test')

    # *******add.2********
    # 参数化数据，将获取的用例参数化读取；testcase_func_name参数化用例名称
    @parameterized.expand(case, testcase_func_name=custom_name_func)
    # *******run.2*******
    def testmain(self, case_id, setup, header, case_name, url, method, path, param, teardown, test_assert):
        # 打印到报告的日志中
        try:
            print "case_%s" % case_id
            print "yaml_data:%s" % data_read.get_yaml()
            self.path = self._handle.handle_url(path)
            self.url = "%s%s" % (url, self.path)
            print "url:%s" % self.url
            print("--------------------------------------------")

            # 处理param，将其中参数替换成具体值
            # 此处当手动修改excel中admin_pwd的值为11111时无法获取到值，当复制黏贴user_pwd的值过去时可以获取，当为非数字时也可以
            if "{" in param:
                self.param = self._handle.handle_param(param)
            else:
                self.param = param

            # 处理前置hender，从yaml中获取token
            if header != "":
                self.header = self._handle.handle_header(header)
            else:
                self.header = header

            # 获取接口返回
            res_code, res_content, res_headers = self._handle.handle_request(method, self.url, self.param, self.header)
            # 打印到报告的日志中
            print "res.code:%s, type:%s" % (res_code, type(res_code))
            print "res.content:%s" % res_content
            print "res.headers:%s" % res_headers

            # 断言，res_code返回值在这个范围则用例成功，否则失败
            assert res_code >= 200 and res_code < 300

            # 处理返回值，将其中后续接口需要用到的参数保存到yaml，如token,cardid等
            if teardown != "":
                self._handle.handle_teardown(teardown, res_content)

        except Exception, e:
            print 'traceback.print_exc():%s,%s' % (traceback.print_exc(), e)
            self.assertTrue(0)

    # *******run.3*******
    @classmethod
    def tearDownClass(cls):
        data_read.del_yaml()
