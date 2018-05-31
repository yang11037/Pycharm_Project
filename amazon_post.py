#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Utils.mongo_helper import MongoHelper
import random
from Utils.http_helper import HttpHelper

ROOT_URL = "http://trackglucose.com"

def Mongo2Csv():
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
    Mongo2Csv()
    print("exit")