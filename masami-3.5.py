# -*- coding: utf-8 -*-
##############################
# by fermi
# 爬取豆瓣影人图片 例子：新垣结衣
###############################
import os
import re
import urllib
import urllib.request
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup

headers = {
    "referer": "https://movie.douban.com/",
    # 自己使用的浏览器
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36",
}


def getAllImageLink(url):
    response = urllib.request.Request(url, headers=headers)
    html = urlopen(response).read()
    soup = BeautifulSoup(html, "html.parser")

    divResult = soup.findAll('div', attrs={"class": "cover"})
    for div in divResult:
        imageEntityArray = div.findAll('img')
        for image in imageEntityArray:
            link = image.get('src')
            newLink = re.sub(r'thumb', 'raw', link)
            imageName = link[-15:]
            fileSavePath = './aragaki/%s' % imageName
            with open(fileSavePath, mode="wb") as f:
                # 将jpg图片写入在目标文件夹创建的文件
                f.write(requests.get(newLink, headers=headers).content)
            print(fileSavePath)


def startSpider(url):
    # 启动爬虫
    try:
        os.mkdir("./aragaki/")
        print("目录创建成功")
    except FileExistsError:
        print("目录已经存在")
    url_process = url.split("&", 2)  # 分解目标url
    for x in range(0, 20 * 40, 40):
        print("正在爬取第%s页..." % ((x / 40) + 1))
        url_new = url_process[0] + "&" + "start=" + \
                  str(x) + "&" + url_process[2]  # 重组获得下一页的目标url
        getAllImageLink(url_new)
    print("完成，已爬完所以图片！")


if __name__ == '__main__':
    # 链接可以替换成你像爬取得豆瓣明星图片！
    startSpider(
        'https://movie.douban.com/celebrity/1018562/photos/?type=C&start=0&sortby=vote&size=a&subtype=a')
