#!/usr/bin/env python


from Utils.http_helper import HttpHelper
from bs4 import BeautifulSoup
from Utils.mongo_helper import MongoHelper


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


if __name__ == "__main__":
    # fetch_dx()
    # fetch_banggood()
    # fetch_tomtop()
    # fetch_gearbest()
    fetch_theverge()