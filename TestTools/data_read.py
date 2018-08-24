# -*- coding:utf-8 -*-

import os
from xlrd import open_workbook
from xlrd import xldate_as_datetime
from xlutils.copy import copy
import yaml
import datetime

upPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
yamlPath = os.path.join(upPath, 'TestData', 'g_data.yaml')
# print upPath
# print yamlPath

def get_xls(type, xls_name, sheet_name):
    # xls文件路径
    xlsPath = os.path.join(upPath, 'TestData', xls_name)

    # 打开文件
    file = open_workbook(xlsPath)

    # 获取sheet内容
    sheet = file.sheet_by_name(sheet_name)
    # 行数
    nrows = sheet.nrows
    # 判断type是list还是dict
    if type == 'list':
        cls = []
        # 去掉首行即表头，然后将数据导入list
        for i in range(nrows):
            if sheet.row_values(i)[0] != u'id' and sheet.row_values(i)[0] != u'moudle' and sheet.row_values(i)[0] != u'name':
                cls.append(sheet.row_values(i))

    elif type == 'dict':
        cls = {}
        # 去掉首行即表头，然后将数据导入dict
        for i in range(nrows):
            if sheet.row_values(i)[0] != u'id' and sheet.row_values(i)[0] != u'moudle' and sheet.row_values(i)[0] != u'name':
                cls.setdefault(sheet.row_values(i)[0],sheet.row_values(i)[1])

    # print cls
    if sheet_name == 'setup':
        # num = cls['num']
        # 复制一个excel
        newfile = copy(file)
        # 获取第一个sheet的内容，get_sheet有write方法
        newsheet = newfile.get_sheet(u'setup')
        #newsheet = newfile.get_sheet(0)
        # 修改第一行第一列的数据
        newsheet.write(1, 1, int(cls['num']) + 1)
        # 修改第四行第一列的数据
        newsheet.write(3, 1, int(cls['user_phone']) + 1)
        # 保存修改后的文件
        newfile.save(xlsPath)

        cls = handle_setup_data(cls)

    return cls

# 数据类型转化
def handle_setup_data(cls):
    num = int(cls['num'])
    cardno = "%s%s" % (cls['cardno'], num)
    admin_pwd = cls['admin_pwd']
    user_phone = int(cls['user_phone'])
    doctor_name = int(cls['doctor_name'])
    doctor_pwd = int(cls['doctor_pwd'])
    check_name = int(cls['check_name'])
    check_pwd = int(cls['check_pwd'])
    user_name = "%s%s" % (cls['user_name'], num)
    # 获取当前日期，类型为str
    startDate = datetime.datetime.now().strftime('%Y-%m-%d')
    # 先将excel中时间unicode类型转化为str类型，再与当前日期组合
    StartDateTime = "%s %s" % (startDate, str(cls['StartDateTime']))
    EndDateTime = "%s %s" % (startDate, str(cls['EndDateTime']))

    cls['num'] = str(num)
    cls['cardno'] = str(cardno)
    cls['user_name'] = str(user_name)
    cls['admin_pwd'] = str(admin_pwd)
    cls['doctor_name'] = str(doctor_name)
    cls['doctor_pwd'] = str(doctor_pwd)
    cls['check_name'] = str(check_name)
    cls['check_pwd'] = str(check_pwd)
    # 增加startDate、endDate字段，字段为unicode格式
    cls[u'startDate'] = str(startDate)
    cls[u'endDate'] = str(startDate)
    # 再将组合后的时间放回cls
    cls['StartDateTime'] = str(StartDateTime)
    cls['EndDateTime'] = str(EndDateTime)
    cls['user_phone'] = str(int(user_phone))

    return cls

# 读取文件
def get_yaml():
    f = open(yamlPath, 'r')
    # 读取
    x = yaml.load(f)
    f.close()
    return x
    #print x

# 追加写入
def set_yaml(data):
    f = open(yamlPath, 'w')
    yaml.dump(data, f)
    f.close()

# 清空文件
def del_yaml():
    f = open(yamlPath, 'w')
    f.truncate()
