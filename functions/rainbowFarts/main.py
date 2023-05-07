import requests


def main():
    try:
        return requests.get("https://api.shadiao.pro/chp").json()['data']['text']
    except requests.exceptions.RequestException as e:
        print('请求发生异常：', e)
        return "祝你今天开心，RequestException"
    except (KeyError, ValueError) as e:
        print('解析JSON数据发生异常：', e)
        return "祝你今天开心，KeyError, ValueError"
    except Exception as e:
        print('发生未知异常：', e)
        return "祝你今天开心，Exception"
