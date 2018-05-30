#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Utils.http_helper import HttpHelper
from Utils.mongo_helper import MongoHelper
from bs4 import BeautifulSoup
import re
from Utils.nlp_helper import NLPHelper

'''
此方法是第一天作为实践爬取链接并存库所用
'''
def test():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBTestCom", "drugs", "url")
    doclist=[]
    print("dbcom")


    html = HttpHelper.fetch("https://www.drugs.com/alpha/a5.html")
    soup = BeautifulSoup(html[1])
    # print(soup)
    list = soup.find_all('ul', attrs={"class": "doc-type-list"})
    # list = soup.find_all('ul', attrs={"class": re.compile('doc-type*')})
    # print(list)
    for i in list:
        li = i.find_all('a')

        for j in li:
            a = j.text
            # print(a)
            b = j['href']
            # print(b)
            print('\n')
            doclist.append({"url": a, "title": b})
        print(doclist)
        collection.insertMany(doclist)


'''
此方法将db中cat为1和2的url的内容采集，并且生成
content，innerhtml，各subtitle，以及description
'''
def test2():
    '''
    以下过程为提取collection中的所有url，最后得到集合doclist
    :return:
    '''
    collection = MongoHelper("172.16.40.140", 27017, "ZDBMedlineplusOrg", "supplement_copy", "url")
    nlp = NLPHelper()
    doclist = []
    doc = []  # doc作为新key：attrlist的
    doc2 = []
    while True:
        slist = collection.nextPage(100)
        if slist == None or len(slist) == 0:
            break
        for i in slist:
            doclist.append(i)
    # print(doclist)

    total = 0

    '''
    以下过程为解析每一个url
    '''
    for i in doclist:

        if i['state'] != "FETCHED":  # 只采集state为FETCHED的对象
            continue

        # 来源为一号网站时
        if i['cat'] == 1:
            html = HttpHelper.fetch(i['url'])
            soup = BeautifulSoup(html[1])   # html结构为[statusCode, html]，所采集标号为1的元素
            slist = soup.find_all("section")
            content = ""                    # 初始化content为一个空字符串
            for j in slist:  # j是section
                hlist = j.find_all("h2")    # tag为h2的都是小标题
                for x in hlist:  # x是title
                    title = x.text

                tlist = j.find_all("div", attrs={"class":"section-body"})
                for y in tlist:  # y是具体一个上面小标题对应的内容
                    doc.append({"subtitle": title, "innerhtml":str(y), "text": y.text})
                    content += y.text      # 总的一页内容是每一个小标题的内容之和

            description = nlp.getSummary(content,wordCount=20)  # 创建描述

            '''
            加入要覆盖当前collection的doc
            '''
            doc2.append({"_id": i['_id'], "cat": i['cat'], "fileName": i['fileName'], "url": i['url'], "host": i['host'],
                        "state": "completed", "title": i['title'], "content": content, "description": description,
                         "attrlist": doc})
            collection.updateOne(doc2)
            doc.clear()
            doc2.clear()   # 每完成一次更新将两个doc清空
            total += 1
            print(total)   # 打印出当前完成的document总数

        # 来源二号网站,原理基本相同
        elif i['cat'] == 2:
            html = HttpHelper.fetch(i['url'])
            soup = BeautifulSoup(html[1])
            slist = soup.find_all("div", attrs={"class":re.compile('field field-name-body*')})
            content = ""
            for j in slist:
                hlist = j.find_all("h2")
                titlearr = []   # 用来存放当前页面的小标题，以便在插入时与innerhtml一一对应
                for x in hlist:  # x是title
                    title = x.text
                    titlearr.append(title)
                tlist = j.find_all("ul")
                index = 0
                for y in tlist:
                    if index > len(titlearr)-1:   # 防止索引越界
                        break
                    doc.append({"subtitle": str(titlearr[index]), "innerhtml": str(y), "text": y.text})
                    content += y.text
                    index = index + 1
                titlearr.clear()
            #print(content)
            description = nlp.getSummary(content, wordCount=20)
            doc2.append({"_id": i['_id'], "cat": i['cat'], "fileName": i['fileName'], "url": i['url'], "host": i['host'],
                        "state": "completed", "title": i['title'], "content": content, "description":description,
                         "attrlist": doc})
            collection.updateOne(doc2)
            doc.clear()
            doc2.clear()
            # print(j)

            total += 1
            print(total)


'''
此方法是将一页内容中的所有innerhtml
整合到一起，并定义出一个新的键值对添加进去
'''
def test3():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBMedlineplusOrg", "supplement_copy", "url")
    doclist = []
    doc = []
    total = 0

    while True:
        slist = collection.nextPage(100)
        if slist == None or len(slist) == 0:
            break
        for i in slist:
            doclist.append(i)

    for i in doclist:
        if i['state'] != "completed":   # 只操作经过test2（）处理的数据
            continue
        contenthtml = ""

        for j in i['attrlist']:
            contenthtml1 = '<h3 class="h3-subtitle">' + j['subtitle'] + '</h3><br/>' \
                           + '<div class="div-content>'+ j['innerhtml'] + '</div><br/>'
            contenthtml += contenthtml1

        doc.append({"_id": i['_id'], "cat": i['cat'], "fileName": i['fileName'], "url": i['url'], "host": i['host'],
                     "state": "built", "title": i['title'], "content": i['content'], "description": i['description'],
                     "attrlist": i['attrlist'], "contenthtml": contenthtml})

        collection.updateOne(doc)
        doc.clear()

        total += 1
        print(total)


'''
此方法对经过test2操作后，description为空的情况进行处理
'''
def for_blank_des():
    collection = MongoHelper("172.16.40.140", 27017, "ZDBMedlineplusOrg", "supplement_copy", "url")
    doclist = []
    doc = []
    nlp = NLPHelper
    total = 0

    while True:
        slist = collection.nextPage(100)
        if slist == None or len(slist) == 0:
            break
        for i in slist:
            doclist.append(i)


    for i in doclist:
        if i['state'] == "built":
            if i['description'] != "":
                continue
            else:
                description = nlp.getSummary(i['content'],wordCount=35)
                print(i['title'])
                print(description)
                '''doc.append(
                    {"_id": i['_id'], "cat": i['cat'], "fileName": i['fileName'], "url": i['url'], "host": i['host'],
                     "state": "built", "title": i['title'], "content": i['content'], "description": description,
                     "attrlist": i['attrlist'], "contenthtml": i['contenthtml']})
                collection.updateOne(doc)'''
                total += 1
                doc.clear()

    print(total)


if __name__ == "__main__":
    print("main")
    # test()
    # test2()
    # test3()
    # for_blank_des()
    print("exit")