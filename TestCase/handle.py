# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
from TestTools import data_read
import re
import demjson
import requests
# 解决报错：InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised.
# See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings InsecureRequestWarning)
# requests.packages.urllib3.disable_warnings()
import json


class handle():
    # 将初始值添加到全局变量中
    def set_global(self, data):
        # 先读取数据
        yamldata = data_read.get_yaml()
        if yamldata == None:
            yamldata = data
        else:
            # 如果有读取数据，则更新数据
            yamldata.update(data)
        # 数据写入文件
        data_read.set_yaml(yamldata)

    # 处理url中参数
    def handle_url(self, data):
        if "{" in data:
            param = re.findall('{(.*?)}', data)
            for i in param:
                yamldata = data_read.get_yaml()
                u = data.replace("{"+i+"}", yamldata[i])
                data = u
        return data

    # 处理body中参数
    def handle_param(self, data):
        if "{" in data:
            param = re.findall("{(.*?)}", data)
            for i in param:
                yamldata = data_read.get_yaml()
                u = data.replace("{"+i+"}", '"'+yamldata[i]+'"')
                data = u
        # 打印到报告的日志中
        print "handle_param-data:%s && type(data):%s" % (data, type(data))
        return demjson.decode(data)

    # 处理header
    def handle_header(self, header):
        self.head_name = header
        if self.head_name == "admin_header":
            self.header = self.get_header("admin_token")
        elif self.head_name == "doctor_header":
            self.header = self.get_header("doctor_token")
        elif self.head_name == "check_header":
            self.header = self.get_header("check_token")
        elif self.head_name == "user_header":
            self.header = self.get_header("user_token")

        return self.header

    # 组合token的方法，返回给header
    def get_header(self, key):
        yamldata = data_read.get_yaml()
        token = yamldata[key]
        header = "{'authorization': 'Bearer %s'}" % token

        return demjson.decode(header)

    # 提交接口请求
    def handle_request(self, method, url, data, header=None):
        if method == "post":
            if header == "":
                res = requests.post(url, data=data, verify=False)
            else:
                res = requests.post(url, json=data, headers=header, verify=False)
        elif method == "get":
            # print "url:%s" % url
            res = requests.get(url, headers=header, verify=False)
        elif method == "put":
            # 打印到报告的日志中
            print "data:%s" % data
            print "header:%s" % header
            res = requests.put(url, json=data, headers=header, verify=False)

        return res.status_code, res.content, res.headers

    # 处理后置teardown，获取其中后续接口需要的参数，并保存到全局变量中
    def handle_teardown(self,teardown, response):
        # 为什么不用demjson.decode() ????
        self.teardown = json.loads(teardown)
        self.response = json.loads(response)
        teardown_dict = {}
        # 判断返回值类型是list还是dict
        if isinstance(self.response, list):
            for i in self.teardown.keys():
                res_value = self.response[int(i)]
                t_value = self.teardown[i]
                for keys in t_value.keys():
                    teardown_dict[t_value[keys]] = res_value[keys]
        else:
            for i in self.teardown.keys():
                value = self.response[i]
                if isinstance(self.teardown[i], dict):
                    for a in self.teardown[i].keys():
                        if isinstance(value, list):
                            value2 = value[int(a)]
                            aa = self.teardown[i][a]
                            for aaa in aa.keys():
                                b = aa[aaa]
                                teardown_dict[b] = value2[aaa]
                        elif isinstance(value, dict):
                            value2 = value[a]
                            key = self.teardown[i][a]
                            teardown_dict[key] = value2
                else:
                    key = self.teardown[i]
                    teardown_dict[key] = value
        self.set_global(teardown_dict)
