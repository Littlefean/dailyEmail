# -*- encoding: utf-8  -*-
import pathlib
from random import choice

import yagmail
import time
import json
import datetime
import requests


def main():
    # 开启死循环
    with open("config/receivers.json", encoding="utf-8") as f:
        receivers: list = json.loads(f.read())

    contentObj = {
        "特殊节日祝福": "",
        "彩虹屁": "祝你今天好运！\n"
    }

    while True:
        # 生成今日内容
        contentObj = generateContent(contentObj)
        print(contentObj)
        # 开始发送邮件
        for userDic in receivers:
            sendEmail(userDic['email'], choice(userDic['nameList']), getEmailContent(userDic, contentObj))
            time.sleep(1)  # 冷却时间
        time.sleep(60 * 60 * 24)  # 一天
        ...


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
