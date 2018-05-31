#!/usr/bin/env python
# -*- coding:utf-8 -*-


from Utils.mongo_helper import MongoHelper
from blog import parseBlog
from Utils.crypt_helper import CryptHelper
from Utils.url_helper import UrlHelper


def test1():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBTechradarCom", "pages")
    doclist = []
    doc = []
    while True:
        slist = collection.nextPage(100)
        if slist == None or len(slist) == 0:
            break
        for i in slist:
            doclist.append(i)
    '''with open("./article.csv", "a+", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(["found", "titleContent", "descriptionContent", "ogTitleContent", "ogDescriptionContent",
                         "twitterTitleContent", "twitterDescriptionContent", "keywordContent", "content",
                         "author", "summary", "summaryKeywords"])
    file.close()'''

    for article in doclist:
        try:
            if article['state'] != "fetched":
                continue
            prefix = article['filename'][0:1]
            filepath = "D:/pages/techradar.com/" + prefix + "/" + article['filename']
            with open(filepath, encoding="utf-8") as fp:
                html = fp.read()
                p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12 = parseBlog(html)
                '''with open("./article.csv", "a+", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f, dialect='excel')
                    writer.writerow([p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12])
                f.close()'''
                md5 = CryptHelper.getMD5Hash(article['url'])
                key = UrlHelper.getHostPath(article['url'])[1]
                doc.append({"_id": article['_id'],
                            "filename": article['filename'],
                            "url": article['url'],
                            "state": "pass",
                            "domain": article['domain'],
                            "md5": md5,
                            "key": key,
                            "blog": {"category": "Automobiles - Article",
                                     "found": p1,
                                     "titleContent": p2,
                                     "descriptionContent":p3,
                                     "ogTitleContent": p4,
                                     "ogDescriptionContent": p5,
                                     "twitterTitleContent": p6,
                                     "twitterDescriptionContent":p7,
                                     "keywordContent": p8,
                                     "content": p9,
                                     "author": p10,
                                     "summary": p11,
                                     "summaryKeywords": p12}})
                collection.updateOne(doc)
                doc.clear()
            fp.close()


        except Exception as err:
            print(err)
    '''for i in doc:
        print(i['blog'])'''


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
    # test1()
    test2()