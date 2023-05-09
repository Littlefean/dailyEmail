"""
获取内容的主方法


"""
from functions.holiday.main import main as f1
from functions.rainbowFarts.main import main as f2
from functions.earthquake.main import main as f3
from functions.news.main import main as f4
from functions.robotDiary.main import main as f5


def getContentObject():
    """
    运行此方法会将所有功能内容爬取生成一遍获得一个内容对象。
    :return:
    """
    return {
        "特殊节日祝福": f1(),
        "彩虹屁": f2(),
        "地震信息": f3(),
        "网页新闻": f4(),
        "机器人日记": f5(),
    }
