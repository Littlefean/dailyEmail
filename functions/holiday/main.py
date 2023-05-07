import json
import datetime


def main():
    with open("functions/holiday/SpecialDaySayHello.json", encoding="utf-8") as f:
        dayDic = json.loads(f.read())
        now = datetime.datetime.now()
        todayStr = f"{now.month}.{now.day}"
        if todayStr in dayDic:
            return dayDic[todayStr]
    return ""
