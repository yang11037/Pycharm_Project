#!/usr/bin/env python
# -*- coding:utf-8 -*-


from Utils.mongo_helper import MongoHelper
from blog import parseBlog
from Utils.crypt_helper import CryptHelper
from Utils.url_helper import UrlHelper
from article import importAllArticle


MONGO_HOST = "172.16.40.140"
MONGO_DATABASE_NAME = "ZDBThevergeCom"
DOMAIN = "D:/pages/theverge.com/"
CATEGORY = "Electronics - Article"
IMPORT_URL = "http://popular123.dev.chn.gbl/DataImport/Article"


'''对采集的每个详情页进行解析，并将之后要上传的属性抠下来存入库'''
def Resolve():
    collection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, "pages")
    doclist = []
    while True:
        slist = collection.nextPage(100)
        if slist == None or len(slist) == 0:
            break
        for i in slist:
            doclist.append(i)


    for article in doclist:
        try:
            if article['state'] != "fetched":
                continue
            prefix = article['filename'][0:1]
            filepath = DOMAIN + prefix + "/" + article['filename']
            with open(filepath, encoding="utf-8") as fp:
                html = fp.read()
                p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12 = parseBlog(html)
                md5 = CryptHelper.getMD5Hash(article['url'])
                key = UrlHelper.getHostPath(article['url'])[1]
                excerpt = p3 if p3 else p11
                doc = {"_id": article['_id'],
                            "filename": article['filename'],
                            "url": article['url'],
                            "state": "pass",
                            "domain": article['domain'],
                            'md5': md5,
                            'title': p2,
                            'excerpt': excerpt,
                            'content': p9,
                            'author': article['domain'],
                            'categories': CATEGORY,
                            'tags': "",
                            'status': 0,
                            'key': key}
                collection.updateOne(doc)
                doc.clear()
            fp.close()


        except Exception as err:
            print(err)
    '''for i in doc:
        print(i['blog'])'''


'''接下来将库中属性提出并上传'''
def upload():
    importAllArticle(MONGO_HOST, MONGO_DATABASE_NAME, IMPORT_URL)


'''此为对数据库中单个数据进行修改的代码，不必理会'''
def test2():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBDigitaltrendsCom", "pages")
    doclist = []
    newlist = []
    while True:
        slist = collection.nextPage(10)
        if len(slist) == 0:
            break

        for article in slist:
            blog = article['blog']
            article['state'] = "pass"
            newlist.append(article)
            collection.updateOne(newlist)
            newlist.clear()


if __name__ == "__main__":
    Resolve()
    # test2()