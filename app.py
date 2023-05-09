# -*- encoding: utf-8 -*-

import time
import json
import pathlib
from random import choice
import datetime

import yagmail
import schedule

from functions.get import getContentObject


def main():
    # 定义每天发送电子邮件的时间
    email_time = "07:23"
    # email_time = "21:17"
    print(f"项目已经启动，每天{email_time}发送邮件")

    # 在每天的指定时间执行send_email()函数
    schedule.every().day.at(email_time).do(sendEmailDay)

    while True:
        # 运行所有的已计划任务
        schedule.run_pending()
        time.sleep(25)
        ...


def sendEmailDay():
    """这个函数每天只执行一次，发送邮件"""
    print("正在获取静态内容")
    # 更新模板内容
    contentObj = getContentObject()

    print("正在读取收件人列表")
    # 读取收件人列表
    with open("config/receivers.json", encoding="utf-8") as f:
        receivers: list = json.loads(f.read())
    # 开始发送邮件
    print("正在发送邮件", datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    for userDic in receivers:
        sendEmail(
            userDic['email'],
            choice(userDic['nameList']),
            getEmailContent(userDic, contentObj)
        )
        time.sleep(0.5)  # 冷却时间
    print("发送完毕", datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))


def getEmailContent(userDic: dict, contentDic: dict) -> str:
    """
    根据用户对象生成邮件内容
    :param userDic: 收件人对象，来源于json文件
    :param contentDic: 内容大字典，来源于最开始准备好了的
    :return:
    """
    # 要有顺序讲究
    reqArr = userDic["requirements"]

    with open("email.html", encoding="utf-8") as f:
        html = f.read().replace("\n", "")

    res = ""
    for reqKey in reqArr:
        res += f"<div class='block'>{contentDic[reqKey]}</div>"
    res = res.strip()
    html = html.replace("#HTML_CONTENT#", res)
    return html


def sendEmail(receiverEmail: str, title: str, content: str):
    """发送邮件给单独的一个人"""
    psw = pathlib.Path("config/emailPassword.txt").read_text().strip()
    email = yagmail.SMTP(
        host='smtp.qq.com',
        user="2385190373@qq.com",
        password=psw,
        smtp_ssl=True
    )
    email.send(receiverEmail, title, content)
    del email


if __name__ == "__main__":
    main()
