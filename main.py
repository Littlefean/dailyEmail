# -*- encoding: utf-8  -*-
import pathlib
from random import choice

import yagmail
import time
import schedule
import json
import datetime
import requests


def main():
    # 开启死循环

    # 下一步更新计划，开成flask框架，开一个管理端页面
    # 能够随时添加移除接受消息的QQ号
    # 每个qq号随时添加/删除 需求

    # 定义每天发送电子邮件的时间
    email_time = "07:23"

    # 在每天的指定时间执行send_email()函数
    schedule.every().day.at(email_time).do(sendEmailDay)

    while True:
        # 运行所有的已计划任务
        schedule.run_pending()
        time.sleep(25)
        ...


def sendEmailDay():
    """这个函数每天只执行一次，发送邮件"""
    # 邮件模板内容
    contentObj = {
        "特殊节日祝福": "",
        "彩虹屁": "祝你今天好运！\n"
    }
    # 更新模板内容
    contentObj = generateContent(contentObj)
    # 读取收件人列表
    with open("config/receivers.json", encoding="utf-8") as f:
        receivers: list = json.loads(f.read())
    # 开始发送邮件
    for userDic in receivers:
        sendEmail(userDic['email'], choice(userDic['nameList']), getEmailContent(userDic, contentObj))
        time.sleep(0.5)  # 冷却时间


def generateContent(defaultDic: dict) -> dict:
    """爬虫，生成全部内容的对象"""
    res = eval(repr(defaultDic))
    # 特殊节日祝福
    with open("SpecialDaySayHello.json", encoding="utf-8") as f:
        dayDic = json.loads(f.read())
        now = datetime.datetime.now()
        todayStr = f"{now.month}.{now.day}"
        if todayStr in dayDic:
            res["特殊节日祝福"] = dayDic[todayStr]
    # 彩虹屁
    try:
        res["彩虹屁"] = requests.get("https://api.shadiao.pro/chp").json()['data']['text']
    except requests.exceptions.RequestException as e:
        print('请求发生异常：', e)
    except (KeyError, ValueError) as e:
        print('解析JSON数据发生异常：', e)
    except Exception as e:
        print('发生未知异常：', e)
    return res


def getEmailContent(userDic: dict, contentDic: dict) -> str:
    """根据用户对象生成邮件内容"""
    res = ""
    for k, v in contentDic.items():
        res += v.strip() + "\n"
    return res.strip()


def sendEmail(receiverEmail: str, title: str, content: str):
    """发送邮件"""
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
