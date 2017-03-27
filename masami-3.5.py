#-*- coding: utf-8 -*-
##############################
# by fermi
# 爬取豆瓣影人图片 例子：长泽雅美
###############################
import urllib
import urllib.request
from urllib.request import urlopen, urlretrieve
import time
import os
import re
import requests
from bs4 import BeautifulSoup

headers = {
    "referer": "https://movie.douban.com/celebrity/1276051/",
    # 自己使用的浏览器
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Cookie": 'bid = Bgywljn1xF0;ll = "118146";gr_user_id = 6686bb9c - b4ef - 4b18 - 939f - 4e78f8d8894d;viewed = "1985875";ps = y;ct = y;ap = 1;_ga = GA1.2.454041090.1465957319;dbcl2 = "50144819:bpy9uZi6Xo0";ck = kFvi;__utmt = 1;_vwo_uuid_v2 = B30AC40B221A4FE539E42DBBE369B97A | 2347d7f84d94228e2c3427da5a24ebfe;_pk_ref.100001.4cf6 = % 5B % 22 % 22 % 2C % 22 % 22 % 2C1470702514 % 2C % 22https % 3A % 2F % 2Fwww.douban.com % 2F % 22 % 5D;push_noty_num = 0;push_doumail_num = 0;__utma = 30149280.454041090.1465957319.1470624031.1470702511.35;__utmb = 30149280.2.10.1470702511;__utmc = 30149280;__utmz = 30149280.1470487004.33.20.utmcsr = douban.com | utmccn = (referral) | utmcmd = referral | utmcct = / group / topic / 76597301 /;__utmv = 30149280.5014;__utma = 223695111.803188614.1465957319.1470624897.1470702514.23;__utmb = 223695111.0.10.1470702514;__utmc = 223695111;__utmz = 223695111.1470702514.23.16.utmcsr = douban.com | utmccn = (referral) | utmcmd = referral | utmcct = /; _pk_id.100001.4cf6 = 8ef1bd7f0403cc70.1465957319.23.1470702549.1470625514.;_pk_ses.100001.4cf6 = *',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch"
}


def getAllImageLink(url):
    response = urllib.request.Request(url)
    html = urlopen(response).read()
    soup = BeautifulSoup(html, "html.parser")

    divResult = soup.findAll('div', attrs={"class": "cover"})
    for div in divResult:
        imageEntityArray = div.findAll('img')
        for image in imageEntityArray:
            link = image.get('src')
            newlink = re.sub(r'thumb', 'raw', link)
            imageName = link[-15:]
            filesavepath = 'F:/pythonspider/masami/%s' % imageName
            with open(filesavepath, mode="wb") as f:
                # 将jpg图片写入在目标文件夹创建的文件
                f.write(requests.get(newlink, headers=headers).content)
            print(filesavepath)


def startspider(url):
    # 启动爬虫
    os.mkdir("F:/pythonspider/masami/")  # 创建存储文件夹
    url_process = url.split("&", 2)     # 分解目标url
    for x in range(0, 20 * 40, 40):
        print("正在爬取第%s页..." % ((x / 40) + 1))
        url_new = url_process[0] + "&" + "start=" + \
            str(x) + "&" + url_process[2]  # 重组获得下一页的目标url
        getAllImageLink(url_new)
    print("完成，已爬完所以图片！")


if __name__ == '__main__':
    # 链接可以替换成你像爬取得豆瓣明星图片！
    startspider(
        'https://movie.douban.com/celebrity/1018667/photos/?type=C&start=0&sortby=vote&size=a&subtype=a')
