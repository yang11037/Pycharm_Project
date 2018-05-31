# coding=utf-8
import time
import sys
from datetime import datetime
from Utils.http_helper import HttpHelper
from Utils.mongo_helper import MongoHelper


def importAllArticle(MONGO_HOST, MONGO_DATABASE_NAME, IMPORT_URL):
    try: 
        articleCollection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, 'pages')
        total = 0
        while True:
            articleList = articleCollection.nextPage(10)
            if len(articleList) == 0:
                break

            total += len(articleList)
            print("total=" + str(total))
            newArticleList = []
            for article in articleList:
                if article['state'] != "pass":
                    continue
                #print (str(article['_id']))
                doc = {
                    'id': article['md5'],
                    'title': article['title'],
                    'excerpt': article['excerpt'],
                    'content': "",
                    'author': article['domain'],
                    'domain': article['domain'],
                    'categories': article['categories'],
                    'tags': article['tags'],
                    'url': article['url'],
                    'status': article['status'],
                    'key': article['key'],
                }
                newArticleList.append(doc)
                
                errorCode, rsp = HttpHelper.post(IMPORT_URL, newArticleList)
                if errorCode == "OK" and rsp != None and 'isOk' in rsp and rsp['isOk'] == True:
                    print ("import article ok")
                else:
                    print ("import article error")
                newArticleList.clear()
                article['state'] = "sended"
                articleCollection.updateOne(article)


    except Exception as err :
        print(err)
    finally:
        print ("exit")    


def updateAllArticle(MONGO_HOST, MONGO_DATABASE_NAME, IMPORT_URL):
    try: 
        articleCollection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, 'article')
        total = 0
        while True:
            articleList = articleCollection.nextPage(10)
            if len(articleList) == 0:
                break

            newArticleList = []
            for article in articleList:
                total += 1
                print ("total=" + str(total))

                url = article['url']
                retry = 0
                while True:
                    retry += 1
                    if retry > 2:
                        break
                    statusCode, html = HttpHelper.fetch(url)            
                    if html != None and len(html) > 0:
                        article['status'] = 0
                        # Check title, TODO
                        print ("update article ok, retry=" + str(retry) + ", url=" + url)
                        break
                    else:
                        article['status'] = -1
                        print ("update article error, retry=" + str(retry) + ", url=" + url)
                        time.sleep(1)
                article['updateTime'] = datetime.now()
                articleCollection.updateOne(article)
                
    except Exception as err :
        print(err)
    finally:
        print ("exit")    


if __name__ == "__main__":
    print("main")
    print (sys.argv)
    if sys.argv[1] == "import":
        importAllArticle()
    elif sys.argv[1] == "update":
        updateAllArticle()
    else:
        print ("usage python article.py [import|update]")
    print("exit")