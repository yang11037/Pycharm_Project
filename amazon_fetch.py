#!/usr/bin/env python
# -*- coding:utf-8 -*-

import xlrd
import xlwt
from http_helper import HttpHelper
from bs4 import BeautifulSoup
import csv
import re
from mongo_helper import MongoHelper
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains


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


def test_chromedriver():
    try:
        driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')
        driver.get("https://www.amazon.com/Diabetes-Testing-Glucose-Lancets-Lancing/dp/B0"
                   "1HF5L98E/ref=sr_1_2_sspa?ie=UTF8&qid=1525005047&sr=8-2-spons&keywords=Blood%2Bglucose%2Bmeter&th=1")
        time.sleep(5)
        '''input = driver.find_elements_by_css_selector("#a-autoid-9 > span > input")
        total = 1
        for i in input:
            ActionChains(driver).move_to_element(i).double_click(i).perform()
            if total == 6:
                break
            total += 1
        time.sleep(5)'''

        html = driver.page_source.encode('utf-8')
        driver.close()
        soup = BeautifulSoup(html, "lxml")
        with open("./product.csv", "a+", newline='',encoding="utf-8") as c:
            writer = csv.writer(c, dialect='excel')
            list = soup.find_all("div", attrs={"class": "imgTagWrapper"})

            img = ""
            for i in list:
                imge = i.find_all("img")
                for j in imge:
                    img = j['src']
                #img += imge['src'] + ","
            #img = img[0:-1]
            sdes = ""
            text1 = soup.find_all("div", attrs={"id":"fbExpandableSectionContent"})
            for j in text1:
                sdes = j
            des = ""
            text2 = soup.find_all("div", attrs={"id": "productDescription_feature_div"})
            for i in text2:
                des = i
            title = ""
            text3 = soup.find_all("span", attrs={"id": "productTitle"})
            for i in text3:
                title = i.text
            title = title.encode("utf-8").decode()
            title = title.strip()
            sdes = sdes.encode("utf-8").decode()
            sdes = sdes.strip()
            des = des.encode("utf-8").decode()
            des = des.strip()
            img = img.encode("utf-8").decode()
            img = img.strip()
            writer.writerow(['', 'simple', '', title, '1', '0', 'visible', sdes, des, '', '', 'taxable', '', '1',
                             '', '0', '0', '', '', '', '', '1', '', '', '39', 'blood glucose meter', '', '', img, '', '',
                             '', '', '', '', '', '', '0'])
            c.close()

    except Exception as err:
        print(err)



if __name__ == "__main__":
    # amazonfetch()
    # amazonfetch_detail()
    test_chromedriver()
    print("exit")