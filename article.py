# coding=utf-8
import time
import sys
from datetime import datetime
from Utils.http_helper import HttpHelper
from Utils.mongo_helper import MongoHelper

MONGO_HOST = "172.16.40.140"
MONGO_DATABASE_NAME = "ZDBBlog"
IMPORT_URL = "http://localhost:54691/DataImport/Article"
IMPORT_URL = "https://www.popular123.com/DataImport/Article"

def importAllArticle():
    try: 
        articleCollection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, 'article')
        total = 0
        while True:
            articleList = articleCollection.nextPage(10)
            if len(articleList) == 0:
                break

            total += len(articleList)
            print ("total=" + str(total))
            newArticleList = []
            for article in articleList:
                #print (str(article['_id']))
                blog = article['blog']
                doc = {
                    'id': blog['md5'],
                    'title': article['titleContent'],
                    'excerpt': article['excerpt'],
                    'content': article['content'],
                    'author': article['author'],
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
                print ("import article list ok")
            else:
                print ("import article list error")
                
    except Exception as err :
        print(err)
    finally:
        print ("exit")    

def updateAllArticle():
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
    
if __name__=="__main__":
    print("main")
    print (sys.argv)
    if sys.argv[1] == "import":
        importAllArticle()
    elif sys.argv[1] == "update":
        updateAllArticle()
    else:
        print ("usage python article.py [import|update]")
    print("exit")