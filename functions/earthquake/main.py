"""
获取今日地震信息

"""
from tools.spider import HtmlGetter
from bs4 import BeautifulSoup
import datetime


def main():
    try:
        text = HtmlGetter("https://news.ceic.ac.cn/index.html", encode="ISO-8859-1", decode="utf-8").get()
    except Exception as e:
        return f"获取地震内容失败，请告知作者。{e}"

    try:
        soup = BeautifulSoup(text, 'lxml')
        arr = soup.select("tr")
        if len(arr) == 0:
            return ""

        arr = arr[1:]
        resText = ""
        for elementTag in arr:
            try:
                tdArr = elementTag.select("td")
                level = tdArr[0].text
                timeStr = tdArr[1].text
                y = tdArr[2].text  # 维度
                x = tdArr[3].text  # 经度
                deep = tdArr[4].text  # km
                placeName = tdArr[5].select_one("a").text
                detailsUrl = tdArr[5].select_one("a").get("href")

                if isTimeLimit(timeStr):
                    # 是25小时以内的
                    resText += f"【{placeName}】于{timeStr}发生了{level}级地震，地震深度{deep}km，经度{x}纬度{y}\n{computeLevel(level)}\n详细信息：{detailsUrl}\n"
            except Exception as e:
                return f"解析页面内容失败，请督促机器人作者，检查地震页面结构是否发生变化。{e}"

        return resText
    except Exception as e:
        return f"解析地震的内容失败，请督促机器人作者，检查地震页面结构是否发生变化。{e}"


def computeLevel(levelStr):
    try:
        level = float(levelStr)
    except ValueError:
        return ""
    if level < 4:
        return "大多数人不会察觉。"
    if level < 5:
        return "有点动静但影响不大"
    if level < 6:
        return "家具会晃动"
    if level < 7:
        return "房屋会受到不同程度的损坏"
    if level < 8:
        return "大多数建筑物都会受到损坏，一些建筑物和桥梁甚至可能会倒塌。车辆和火车无法继续行驶"
    else:
        return "这是一次具有破坏性和灾难性的地震，几乎所有的建筑物都会受到严重损坏，许多建筑物和桥梁都可能会倒塌。地面会产生明显的裂缝，地形也会发生重大改变。人们很难站立和移动，大多数人会陷入恐慌和混乱中。"


def isTimeLimit(time_str):
    """
    传入的时间字符串是否在25小时内
    :param time_str: “2023-05-06 21:23:45”
    :return: bool
    """
    now = datetime.datetime.now()

    # 将时间字符串转换为datetime对象
    time_obj = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

    # 计算时间差
    time_delta = now - time_obj

    # 如果时间差小于等于25小时，说明时间在25小时内
    return time_delta <= datetime.timedelta(hours=25)


if __name__ == "__main__":
    main()
