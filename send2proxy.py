#!/usr/bin/env python
# -*- coding:utf-8 -*-


from Utils.mongo_helper import MongoHelper
from crawler_dynamic_robot import sendPage


DOMAIN = "D:/pages/gearbest.com/"
MONGO_HOST = "172.16.40.140"
MONGO_DATABASE_NAME = "ZDBTechradarCom"


# 将采集到本地的html上传（商品）
def test():
    collection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, "pages")
    doclist = []
    total = 1

    while True:
        slist = collection.nextPage(100)
        if slist == None or len(slist) == 0:
            break
        for i in slist:
            doclist.append(i)

    for page in doclist:
        try:
            if page['state'] != 'fetched':
                continue
            prefix = page['filename'][0:1]
            filepath = DOMAIN + prefix + "/" + page['filename']
            with open(filepath, encoding="utf-8") as fp:
                html = fp.read()
                task = {"id": "id", "url": page['url'], 'topic': 'crawler_data_p123',
                        'routingKey': '256'}  # dx.com 225, banggood.com 224 ,tomtop 195 ,gearbest 256
                sendPage(task, html)
            fp.close()
            page['state'] = 'sended'
            collection.updateOne(page)
            print(total)
            total += 1
        except Exception as err:
            print(err)


if __name__ == "__main__":
    test()
