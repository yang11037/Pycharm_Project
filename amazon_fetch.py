#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Utils.http_helper import HttpHelper
from bs4 import BeautifulSoup
import csv
import re
from Utils.mongo_helper import MongoHelper
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains


def amazonfetch():
    total = 1
    goods = 1
    url = "https://www.amazon.com/s/ref=sr_as_oo?rh=i%3Aaps%2Ck%3Ablood+pressure+monitor&keywords=blood+pressure+mon" \
          "itor&ie=UTF8&qid=1527130301"
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
                print(flag)
                continue
            #print("flagok")
            a = li.find_all("a", attrs={"class": re.compile("^a-link-normal s-access-detail-page.*")})
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
                span = i.find_all("span", attrs={"class": "a-size-small a-color-secondary"})
                if span == []:
                    continue
                #print("spanok")
                for j in span:
                    brand += j.text
            brand = brand[3:]
            p = li.find_all("span", attrs={"class": "sx-price-whole"})
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


        try:
            status, html = HttpHelper.fetch(x['url'])
            soup = BeautifulSoup(html, "lxml")
            title = soup.find_all("span", attrs={"id": "productTitle"})
            for i in title:
                text = i.text
                title = text.strip()
            a = soup.find_all("a", attrs={"id": "bylineInfo"})  # bylineInfo brand
            for i in a:
                href = i['href']
                if re.match("^/{1}.*", href):
                    href = "http://www.amazon.com" + href
            description = soup.find_all("ul", attrs={"class": "a-unordered-list a-vertical a-spacing-none"})
            for i in description:
                doc.append({"_id": x['_id'], "brand": x['brand'], "url": x['url'], "state": "pass", "price": x['price']
                            , "title": title, "brand_a": href, "inner_des": str(i)})
            collection.updateOne(doc)
            doc.clear()
        except Exception as err:
            print(err)
            continue
        print(total)
        total += 1


def test_chromedriver():
    try:
        total = 1
        doclist = []
        doc = []
        collection = MongoHelper("172.16.40.140", 27017, "ZDBTestCom", "bloodglucosemeter")
        while True:
            slist = collection.nextPage(100)
            if slist == None or len(slist) == 0:
                break
            for i in slist:
                doclist.append(i)

        for page in doclist:
            print(total)
            total += 1
            if page['state'] != 'pass':
                continue

            driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')
            driver.get(page['url'])
            print("wait for u")

            size = driver.find_elements_by_tag_name("img")
            for i in size:
                if i.location['x'] == 19 or i.location['x'] == 71:
                    if i.size == {'height': 40, 'width': 40}:
                        ActionChains(driver).move_to_element(i).click(i).perform()

            html = driver.page_source.encode('utf-8')
            driver.close()
            soup = BeautifulSoup(html, "lxml")
            with open("./product.csv", "a+", newline='', encoding="utf-8") as c:
                writer = csv.writer(c, dialect='excel')
                list = soup.find_all("div", attrs={"class": "imgTagWrapper"})

                img = ""
                for i in list:
                    imge = i.find_all("img")
                    for j in imge:
                        img = img + j['src'] + ","
                img = img[0:-1]

                price = ""
                pricetxt = soup.find_all("span", attrs={"id": "priceblock_ourprice"})
                for i in pricetxt:
                    price = i.text
                    price = price.strip()

                des = ""
                text2 = soup.find_all("div", attrs={"id": "productDescription"})
                '''div,class:aplus-v2 desktop celwidget  
                   div id: productDescription
                '''
                for i in text2:
                    des = i
                des = des.encode("utf-8").decode()
                des = des.strip()
                des_html = "<div class=\"productdescription\">" + des +"</div>"

                img = img.encode("utf-8").decode()
                img = img.strip()

                sdes = page['inner_des']
                sdes = "<div class = \"short-des\">" + "<a href = \"" + page['brand_a'] + "\">" + \
                       "<font size=1 color=blue>" + page['brand'] + "</font></a><br>About the product<br>"\
                       + sdes + "</div>"

                writer.writerow(['', 'simple', '', page['title'], '1', '0', 'visible', sdes, des_html, '', '',
                                 'taxable', '', '1', '', '0', '0', '', '', '', '', '1', '', '', price,
                                 'blood glucose meter', '', '', img, '', '', '', '', '', '', '', '', '0'])
                print("csv ok")

                doc.append({"_id": page['_id'], "brand": page['brand'], "url": page['url'], "state": "posted",
                            "price": price, "title": page['title'], "brand_a": page['brand_a'],
                            "inner_des": page['inner_des'], "product_des": des})
                collection.updateOne(doc)
                doc.clear()
                print("mongo ok")
            c.close()

    except Exception as err:
        print(err)

def test():
    try:
        driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')
        driver.get("https://www.amazon.com/KINGDOMCARES-Moisturizing-Blackheads-Humidifier-Hydration/dp/B01M0HBUXR/ref"
                   "=sr_1_49_sspa/132-1314774-3806241?ie=UTF8&qid=1525248585&sr=8-49-spons&keywords=mist%2Binhaler&th=1")
        time.sleep(5)
        html = driver.page_source.encode('utf-8')
        driver.close()
        soup = BeautifulSoup(html)
        list = soup.find_all("span", attrs={"id":"priceblock_ourprice"})
        price = ""
        for i in list:
            price = i.text
            price = price.strip()
        print(price)
    except Exception as err:
        print(err)

if __name__ == "__main__":
    # amazonfetch()
    # amazonfetch_detail()
    test_chromedriver()
    # test()
    print("exit")