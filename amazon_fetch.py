#!/usr/bin/env python
# -*- coding:utf-8 -*-

import xlrd
import xlwt
from http_helper import HttpHelper
from bs4 import BeautifulSoup
import re
from mongo_helper import MongoHelper
from selenium import webdriver


def amazonfetch():
    total = 1
    goods = 1
    url = "https://www.amazon.com/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3ABlood+glucose+meter&" \
          "page=1&keywords=Blood+glucose+meter&ie=UTF8&qid=1524802633"
    collection = MongoHelper("172.16.40.140", 27017, "ZDBTestCom", "bloodglucosemeter")

    '''excel = xlwt.Workbook()
    sheet = excel.add_sheet("Blood glucose meter")
    content = "brand"
    sheet.write(0,0,content)
    content = "url"
    sheet.write(0,1,content)
    row = 1'''
    doc = []

    while url != None:
        statuscode, html = HttpHelper.fetch(url)
        soup = BeautifulSoup(html)
        for s in soup('script'):
            s.extract()
        #print(soup.prettify())
        #return

        li_all = soup.find_all("li", attrs={"id":re.compile("^result_\d{1,2}")})
        #print(li_all[3])
        #return
        for li in li_all:
            print("正在检查第"+ str(goods) + "件商品")
            goods += 1
            flag = li.find_all("p",attrs={"class":"acs-mn2-midwidgetHeader"})
            if flag != []:
                continue
            #print("flagok")
            a = li.find_all("a", attrs={"class":re.compile("^a-link-normal s-access-detail-page.*")})
            if a == []:
                continue
            #print("aok")
            for i in a:
                url2 = i['href']
            branddiv = li.find_all("div", attrs={"class": "a-row a-spacing-none"})
            if branddiv == []:
                continue
            #print("brandok")
            brand = ""
            for i in branddiv:
                span = i.find_all("span", attrs={"class":"a-size-small a-color-secondary"})
                if span == []:
                    continue
                #print("spanok")
                for j in span:
                    brand += j.text
            brand = brand[3:]
            p = li.find_all("span", attrs={"class":"sx-price-whole"})
            if p == []:
                continue
            for i in p:
                price = i.text
            if price == []:
                continue
            #print("priceok")
            div = li.find_all("div", attrs={"class":"a-row a-spacing-mini"})
            if div == []:
                continue
            #print("divok")
            for j in div:
                comment_all = j.find_all("a", attrs={"class":"a-size-small a-link-normal a-text-normal"})
                if comment_all == []:
                    continue
                #print("comok")
                for i in comment_all:
                    comment = i.text

            print("price的类型是:")
            print(type(price))
            print(type(comment))
            price = price.replace(",", "")
            comment = comment.replace(",", "")
            print(price)
            print(comment)

            try:
                if isinstance(price, str):
                    price1 = int(price)
                if isinstance(comment, str):
                    comment1 = int(comment)
            except Exception as err:
                print(err)
                continue

            if price1 > 20 and price1 < 50 and comment1 > 100:
                print(brand)
                print("No." + str(total))
                total +=1
                url3 = url2
                if re.match("^/{1}.*", url2):
                    url3 = "https://www.amazon.com" + url2
                '''sheet.write(row,0,brand)
                sheet.write(row,1,url3)
                row += 1'''
                doc.append({'brand': brand, 'url': url3, 'state': 'fetched', 'price': price + ".99"})

            if total > 90:
                print("completed")
                #excel.save("D:/电商/test.xls")
                collection.insertMany(doc)
                return


        next_page = soup.find_all("a",attrs={"id":"pagnNextLink"})
        if next_page == []:
            url = None
            continue
        for i in next_page:
            if re.match("^/{1}.*", i['href']):
                url = "https://www.amazon.com"+ i['href']
            else:
                url = i['href']

    print("not enough 90")
    # excel.save("D:/电商/test.xls")
    collection.insertMany(doc)


def amazonfetch_detail():
    doclist = []
    doc = []
    total = 1
    collection = MongoHelper("172.16.40.140", 27017, "ZDBTestCom", "bloodglucosemeter")

    while True:
        slist = collection.nextPage(100)
        if slist == None or len(slist) == 0:
            break
        for i in slist:
            doclist.append(i)

    for x in doclist:
        if x['state'] != "fetched":
            continue

        '''driver = webdriver.PhantomJS(r"D:\Anaconda\pkgs\phantomjs-2.1.1-0\Library\bin\phantomjs.exe")
                driver.get(i['url'])
                print(driver.current_url)
                driver.quit()
                return'''
        try:
            status, html = HttpHelper.fetch(x['url'])
            soup = BeautifulSoup(html)
            title = soup.find_all("span", attrs={"id": "productTitle"})
            for i in title:
                text = i.text
                title = text.strip()
            a = soup.find_all("a", attrs={"id": "bylineInfo"})
            for i in a:
                href = i['href']
                if re.match("^/{1}.*", href):
                    href = "http://www.amazon.com" + href
            description = soup.find_all("ul", attrs={"class": "a-unordered-list a-vertical a-spacing-none"})
            for i in description:
                doc.append({"_id": x['_id'], "brand": x['brand'], "url": x['url'], "state": "pass", "price":x['price']
                            , "title": title, "brand_a": href, "inner_des": str(i)})
            collection.updateOne(doc)
            doc.clear()
        except Exception as err:
            print(err)
            continue
        print(total)
        total += 1


if __name__ == "__main__":
    #amazonfetch()
    amazonfetch_detail()
    print("exit")