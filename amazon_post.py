#!/usr/bin/env python
# -*- coding:utf-8 -*-

import xlrd
import xlwt
from bs4 import BeautifulSoup
import re
import random
from http_helper import HttpHelper
from mongo_helper import MongoHelper

ROOT_URL = "http://trackglucose.com"


def createPost(pd):
    url = ROOT_URL + "/wp-content/plugins/post-api/insert_post.php?token=P@ssw0rd&dummy=" + str(random.random())
    req = {
        'post_title': pd['title'],
        'excerpt': pd['inner_des'],
        'categories': "blood glucose meter",
        '_regular_price': pd['price']
    }
    errorCode, rsp = HttpHelper.post(url, req)
    if errorCode == 'OK' and 'errorCode' in rsp and rsp['errorCode'] == 'OK':
        print(rsp['ID'])
        return rsp['ID']
    else:
        return None


def createAllPost():
    doc = []
    try:
        pdCollection = MongoHelper("172.16.40.140", 27017, "ZDBTestCom", "bloodglucosemeter")

        total = 0
        while True:
            pdList = pdCollection.nextPage(10)
            if pdList == None or len(pdList) == 0:
                break

            for pd in pdList:
                if pd['state'] != 'pass':
                    continue

                newID = createPost(pd)
                if newID != None:
                    doc.append({"_id": pd['_id'], "ID": newID, "brand": pd['brand'], "url": pd['url'],
                                "state": "posted", "price": pd['price'], "title": pd['title'], "brand_a": pd['brand_a']
                                , "inner_des": pd['inner_des']})
                    print(doc[0]['ID'])
                    pdCollection.updateOne(doc)
                    doc.clear()
                    print("create post ok")
                else:
                    print("create post error")

                total += 1
                print('total=' + str(total) + ', title=' + pd['title'])
                return

        print('Creawte all posts ok')

    except Exception as err:
        print(err)


if __name__ == "__main__":
    print("main")
    createAllPost()
    print("exit")