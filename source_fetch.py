#!/usr/bin/env python
# -*- coding=utf-8 -*-

from Utils.http_helper import HttpHelper
from bs4 import BeautifulSoup
from Utils.mongo_helper import MongoHelper
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

# 商品
def fetch_dx():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBDxCom", "pages")
    entrance = "http://www.dx.com/c/computer-office-399/networking-314"
    pageNum = 1
    total = 1
    doc = []
    while pageNum < 11 and entrance is not None:
        html = HttpHelper.fetch(entrance)[1]
        soup = BeautifulSoup(html, "lxml")
        proUl = soup.find_all("ul", attrs={"class": "productList subList"})
        for proList in proUl:
            li = proList.find_all("li", attrs={"class": "c_cates"})
            for i in li:
                try:
                    photo = i.find("div", attrs={"class": "photo"})
                    url = "https://www.dx.com" + photo.find("a")['href']
                    filename = HttpHelper.fetchAndSave(url, "utf-8", "D:/pages/dx.com")
                    doc.append({"filename": filename, "url": url, "state": "fetched"})
                    print(total)
                    total += 1
                except Exception as err:
                    print(err)
        a = soup.find_all("a", attrs={"class": "next"})
        if a is None:
            entrance = None
            print("NO." + str(pageNum))
            pageNum += 1
            continue
        next = a[-1]
        entrance = "https://www.dx.com" + next['href']
        print(entrance)
        print(pageNum)
        pageNum += 1
    if doc != []:
        collection.insertMany(doc)


# 商品
def fetch_banggood():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBBgoodCom", "pages")
    entrance = "https://www.banggood.com/Wholesale-Indoor-Lighting-c-2514.html"
    pageNum = 1
    total = 1
    doc = []

    while pageNum < 11 and entrance is not None:
        html = HttpHelper.fetch(entrance)[1]
        soup = BeautifulSoup(html, 'lxml')
        proUl = soup.find("ul", attrs={"class": "goodlist_1"})
        li = proUl.find_all("li")
        for i in li:
            try:
                photo = i.find_all("span", attrs={"class": "img"})
                for j in photo:
                    a = j.find("a")
                    url = a['href']
                    filename = HttpHelper.fetchAndSave(url, 'utf-8', 'D:/pages/banggood.com')
                    doc.append({"filename": filename, "url": url, "state": "fetched"})
                    print(total)
                    total += 1
            except Exception as err:
                print(err)
        div = soup.find("div", attrs={"class": "page_num"})
        next = div.find("a", attrs={"id": "listNextPage"})
        if next is None:
            entrance = None
            print("NO." + str(pageNum))
            pageNum += 1
            continue
        entrance = next['href']
        print("NO." + str(pageNum))
        pageNum += 1
    if doc != []:
        collection.insertMany(doc)


# 商品
def fetch_tomtop():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBTomtopCom2", "pages")
    entrance = "https://www.tomtop.com/vehicle-infotainment-11035/"
    pageNum = 1
    total = 1
    doc = []

    while pageNum < 11 and entrance is not None:
        html = HttpHelper.fetch(entrance)[1]
        soup = BeautifulSoup(html, 'lxml')
        proUl = soup.find("ul", attrs={"class": "lbBox categoryProductList"})
        li = proUl.find_all("li")
        for i in li:
            try:
                photo = i.find_all("div", attrs={"class": "productImg"})
                for j in photo:
                    a = j.find("a")
                    url = "https://www.tomtop.com" + a['href']
                    filename = HttpHelper.fetchAndSave(url, 'utf-8', 'D:/pages/tomtop.com')
                    doc.append({"filename": filename, "url": url, "state": "fetched"})
                    print(total)
                    total += 1
            except Exception as err:
                print(err)
        ul = soup.find("ul", attrs={"class": "lbBox pagingWarp"})
        next = ul.find("li", attrs={"class": "lineBlock pageN pageClick"})
        if next is None:
            entrance = None
            print("NO." + str(pageNum))
            pageNum += 1
            continue
        entrance = "https://www.tomtop.com" + next.find("a")['href']
        print("NO." + str(pageNum))
        pageNum += 1
    if doc != []:
        collection.insertMany(doc)


# 商品
def fetch_gearbest():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBGearbestCom", "pages")
    entrance = "https://www.gearbest.com/health-care-c_11689/"
    pageNum = 1
    total = 1
    doc = []
    while pageNum < 11 and entrance is not None:
        html = HttpHelper.fetch(entrance)[1]
        soup = BeautifulSoup(html, "lxml")
        proUl = soup.find_all("ul", attrs={"class": "clearfix js_seachResultList"})
        for proList in proUl:
            li = proList.find_all("li")
            for i in li:
                try:
                    photo = i.find_all("a", attrs={"class": "icon-loading gbGoodsItem_thumb js-selectItemd"})
                    for j in photo:
                        url = j['href']
                        filename = HttpHelper.fetchAndSave(url, "utf-8", "D:/pages/gearbest.com")
                        doc.append({"filename": filename, "url": url, "state": "fetched"})
                        print(total)
                        total += 1
                except Exception as err:
                    print(err)
        a = soup.find_all("a", attrs={"class": "pageNext"})
        if a is None:
            entrance = None
            print("NO." + str(pageNum))
            pageNum += 1
            continue
        next = a[-1]
        entrance = next['href']
        print("NO." + str(pageNum))
        pageNum += 1
    if doc != []:
        collection.insertMany(doc)


# 文章
def fetch_theverge():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBThevergeCom", "pages")
    url = "https://www.theverge.com/camera-review"
    doc = []
    html = HttpHelper.fetch(url)
    soup = BeautifulSoup(html[1], "lxml")
    total = 1

    div = soup.find_all("div", attrs={"class": "c-compact-river"})
    for i in div:
        try:
            a = i.find_all("a", attrs={"class": "c-entry-box--compact__image-wrapper"})
            for j in a:
                filename = HttpHelper.fetchAndSave(j['href'], "utf-8", "D:/pages/theverge.com")
                doc.append({"filename": filename, "url": j['href'], "state": "fetched", "domain": "www.theverge.com"})
                print(total)
                total += 1
        except Exception as err:
            print(err)
    collection.insertMany(doc)


# 文章
def fetch_digitaltrends():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBDigitaltrendsCom", "pages")
    entrance = "https://www.digitaltrends.com/tv-reviews/"
    doclist = []
    total = 1
    while total < 120 and entrance is not None:
        html = HttpHelper.fetch(entrance)
        soup = BeautifulSoup(html[1], "lxml")

        div = soup.find("div", attrs={"class": "m-products"})
        item = div.find_all("div", attrs={"class": "item"})
        for i in item:
            try:
                h3 = i.find("h3", attrs={"class": "title"})
                url = h3.find("a")['href']
                filename = HttpHelper.fetchAndSave(url, "utf-8", "D:/pages/digitaltrends.com")
                doclist.append({"filename": filename, "url": url, "state": "fetched", "domain": "www.digitaltrends.com"})
                print(total)
                total += 1
            except Exception as err:
                print(err)

        a = soup.find_all("a", attrs={"class": "next page-numbers"})
        if a is None:
            entrance = None
            continue
        next = a[-1]
        entrance = next['href']
    if doclist != []:
        collection.insertMany(doclist)


# 文章
def fetch_cnet():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBCnetCom", "pages")
    entrance = "https://www.cnet.com/topics/tablets/products/"
    doclist = []
    total = 1
    while total < 80 and entrance is not None:
        html = HttpHelper.fetch(entrance)
        soup = BeautifulSoup(html[1], "lxml")

        section1 = soup.find("section", attrs={"id": "dfllResults"})
        section2 = section1.find_all("section", attrs={"class": "col-3 searchItem product "})
        for i in section2:
            try:
                a = i.find("a", attrs={"class": "imageWrap"})
                url = "https://www.cnet.com" + a['href']
                filename = HttpHelper.fetchAndSave(url, "utf-8", "D:/pages/cnet.com")
                doclist.append({"filename": filename, "url": url, "state": "fetched", "domain": "www.cnet.com"})
                print(total)
                total += 1
            except Exception as err:
                print(err)

        a = soup.find_all("a", attrs={"class": "next"})
        if a is None:
            entrance = None
            continue
        next = a[-1]
        entrance = "https://www.cnet.com" + next['href']
    if doclist != []:
        collection.insertMany(doclist)


# 文章
def fetch_techradar():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBTechradarCom", "pages")
    entrance = "https://www.techradar.com/reviews/car-tech?"
    doclist = []
    total = 1
    html = HttpHelper.fetch(entrance)
    soup = BeautifulSoup(html[1], "lxml")

    div = soup.find("div", attrs={"class": "listingResults"})
    divitem = div.find_all("div", attrs={"class": re.compile("^listingResult small result*")})
    for i in divitem:
        try:
            a = i.find("a")
            url = a['href']
            filename = HttpHelper.fetchAndSave(url, "utf-8", "D:/pages/techradar.com")
            doclist.append({"filename": filename, "url": url, "state": "fetched", "domain": "www.techradar.com"})
            print(total)
            total += 1
        except Exception as err:
            print(err)
    collection.insertMany(doclist)


# 文章 trend by webdriver
def fetch_highsnobiety():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBHighsnobietyCom", "pages")
    entrance = "https://www.highsnobiety.com/style/"
    driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')
    driver.get(entrance)
    print("waiting for u")
    doclist = []  # 此处设置断点
    total = 1
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    div = soup.find("div", attrs={"class": "sub-contents__item"})
    articles = div.find_all("article")
    for i in articles:
        try:
            a = i.find("a")
            url = a['href']
            filename = HttpHelper.fetchAndSave(url, "utf-8", "D:/pages/highsnobiety.com")
            doclist.append({"filename": filename, "url": url, "state": "fetched", "domain": "www.highsnobiety.com"})
            print(total)
            total += 1
        except Exception as err:
            print(err)
    collection.insertMany(doclist)


# 文章
def fetch_fashionbeans():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBFashionbeansCom", "pages")
    entrance = "http://www.fashionbeans.com/category/mens-hairstyles/"
    doclist = []
    total = 1
    num = 1
    while total < 200 and entrance is not None:
        html = HttpHelper.fetch(entrance)
        soup = BeautifulSoup(html[1], "lxml")

        div = soup.find("div", attrs={"id": "catmainBody"})
        articles = div.find_all("div", attrs={"class": "catArticles"})
        for i in articles:
            try:
                a = i.find("a", attrs={"class": "left relative"})
                url = a['href']
                filename = HttpHelper.fetchAndSave(url, "utf-8", "D:/pages/fashionbeans.com")
                doclist.append({"filename": filename, "url": url, "state": "fetched", "domain": "www.fashionbeans.com"})
                print(total)
                total += 1
            except Exception as err:
                print(err)

        a = soup.find("a", attrs={"class": "nextLink right"})
        print("页数:" + str(num))
        if a is None:
            entrance = None
            continue
        num += 1
        entrance = a['href']
    if doclist != []:
        collection.insertMany(doclist)


# 文章 webdriver
def fetch_whowhatwear():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBWhowhatwearCom", "pages")
    entrance = "https://www.whowhatwear.com/channel/trends"
    driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')
    driver.get(entrance)
    print("waiting for u")
    doclist = []  # 此处设置断点
    total = 1
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    div = soup.find("div", attrs={"class": "card__group card__group--river card__group--river-channel"})
    articles = div.find_all("div", attrs={"class": "card__item card__item--river card__item--river-channel"})
    for i in articles:
        try:
            a = i.find("a")
            url = "https://www.whowhatwear.com" + a['href']
            filename = HttpHelper.fetchAndSave(url, "utf-8", "D:/pages/whowhatwear.com")
            doclist.append({"filename": filename, "url": url, "state": "fetched", "domain": "www.whowhatwear.com"})
            print(total)
            total += 1
        except Exception as err:
            print(err)
    collection.insertMany(doclist)


# 文章 webdriver
def fetch_fashionista():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBFashionistaCom", "pages")
    entrance = "https://fashionista.com/style"
    driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')
    driver.get(entrance)
    print("waiting for u")
    doclist = []  # 此处设置断点
    total = 1
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    articles = soup.find_all("article", attrs={"class": "m-card mm-card--landscape-image mm-card--type-list"})
    for i in articles:
        try:
            a = i.find("a", attrs={"class": "m-card--image-link m-background-image"})
            url = "https://fashionista.com" + a['href']
            filename = HttpHelper.fetchAndSave(url, "utf-8", "D:/pages/fashionista.com")
            doclist.append({"filename": filename, "url": url, "state": "fetched", "domain": "www.fashionista.com"})
            print(total)
            total += 1
        except Exception as err:
            print(err)
    collection.insertMany(doclist)


if __name__ == "__main__":
    # fetch_dx()
    # fetch_banggood()
    # fetch_tomtop()
    # fetch_gearbest()
    # fetch_theverge()
    # fetch_digitaltrends()
    # fetch_cnet()
    # fetch_techradar()
    # fetch_highsnobiety()
    # fetch_fashionbeans()
    # fetch_whowhatwear()
    fetch_fashionista()