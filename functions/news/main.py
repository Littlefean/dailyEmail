"""
抓新闻

"""
from tools.spider import HtmlGetter
from bs4 import BeautifulSoup


def main():
    # https://news.sina.com.cn/
    html = HtmlGetter("https://news.sina.com.cn/", encode="ISO-8859-1", decode="utf-8").get()
    soup = BeautifulSoup(html, "lxml")
    # headlines = soup.select('h1[data-client="headline"] a')
    li_as = soup.select('li a[href^="https://"]')

    # 要筛选出含有href属性并且是https开头的地址的a标签
    # a标签里没有嵌套其他标签
    # a标签里的文字内容长度大于5
    li_as = list(filter(lambda x: x.has_attr("href") and len(x.text.strip()) > 8 and not x.find(), li_as))

    result = []
    for li_a in li_as:
        title = li_a.text.strip()
        url = li_a['href']
        result.append({"title": title, "url": url})

    # 关键词筛选

    keywords = read_keywords_file("functions/news/keywords.txt")
    # keywords = read_keywords_file("keywords.txt")
    filtered_result = [r for r in result if any(kw in r['title'] for kw in keywords)]
    excludeKeywords = read_keywords_file("functions/news/excludeKeywords.txt")
    # excludeKeywords = read_keywords_file("excludeKeywords.txt")
    filtered_result = [r for r in filtered_result if not any(kw in r['title'] for kw in excludeKeywords)]

    # for obj in filtered_result:
    #     print(obj)
    # print(html)
    return objectListToStr(filtered_result)


def objectListToStr(objList):
    res = "以下是今天抓到的新闻：\n"
    for item in objList:
        res += f"{item['title']}：{item['url']}\n"
    return res


def read_keywords_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    keywords = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):  # 如果是空行或注释行则跳过
            continue
        keywords.append(line)

    return keywords


if __name__ == "__main__":
    main()
