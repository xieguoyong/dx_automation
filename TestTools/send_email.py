# -*- coding:utf-8 -*-
__author__ = u'he.jianjun'
# TODO(he.jianjun@dr-elephant.com):这是邮件发送的代码

import smtplib
import time
import os
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

upPath = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
att_path = os.path.join(upPath, "TestResult", "result.html")


class sendemail:
    def send_mail(self):
        #
        # email_from = "he.jianjun@dr-elephant.com" #邮件发送人
        email_from = "xie.guoyong@dr-elephant.com"
        email_to = ["xie.guoyong@dr-elephant.com"]    #收件人
        # email_to = ["he.jianjun@dr-elephant.com"]
        email_Sub = "接口自动化报告"+str(time.strftime("%Y/%m/%d",time.localtime()))

        msg = MIMEMultipart('alternative')
        htmlfile = open(att_path,'r').read()
        msg['From'] = Header(email_from, 'utf-8')
        msg['To'] = Header(u"谢国勇", 'utf-8')
        msg['Subject'] = Header(email_Sub,'utf-8')
        # 邮件主体内容
        mail_body = ''

        # 邮件正文内容  "plain","html"
        msg.attach(MIMEText(htmlfile, 'html', 'utf-8'))
        # 构造附件，传送当前目录下的 文件
        att = MIMEText(open(att_path, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att["Content-Disposition"] = 'attachment; filename="auto_result_report.html"'
        msg.attach(att)

        try:
            conn = smtplib.SMTP('smtp.dr-elephant.com',587)
            conn.ehlo()
            conn.starttls()
            conn.ehlo()
            conn.login("xie.guoyong@dx.com","Dx123456")
            conn.sendmail(email_from, email_to, msg.as_string())
            print("邮件已发送成功")
            conn.close()
        except smtplib.SMTPException as e:
            print("Error:邮件发送失败:%s"% e)

# if __name__ == '__main__':
#     post = sendemail()
#     post.send_mail()
#     # print(att_path)
