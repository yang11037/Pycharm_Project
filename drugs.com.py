# coding=utf-8
import string
import time
import hashlib
import os
import re
import random
from http_helper import HttpHelper
from mongo_helper import MongoHelper
from nlp_helper import NLPHelper
#from file_helper import FileHelper

HTQ_ROOT_URL = "http://htq.dev.chn.gbl"
CAT_ID = 5

def createPost(pd):
    url = HTQ_ROOT_URL + "/wp-content/plugins/post-api/insert_post.php?token=P@ssw0rd&dummy=" + str(random.random())
    req = {
        'ID': 0,
        'author': 1,
        'title': pd['title'],
        'excerpt': pd['description'],
        'content': pd['contenthtml'],
        'categories': [CAT_ID],
        'tags': [],
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
        pdCollection = MongoHelper("172.16.40.140", 27017, "ZDBMedlineplusOrg", "supplement_copy")
        
        total = 0
        while True:
            pdList = pdCollection.nextPage(10)
            if pdList == None or len(pdList) == 0:
                break
            
            for pd in pdList:
                if pd['state'] != 'built':
                    continue
                
                newID = createPost(pd)
                if newID != None:
                    doc.append({"_id": pd['_id'], "ID":newID, "cat": pd['cat'], "fileName": pd['fileName'],
                                "url": pd['url'],
                                 "host": pd['host'],
                                 "state": "posted", "title": pd['title'], "content": pd['content'],
                                 "description": pd['description'],
                                 "attrlist": pd['attrlist'], "contenthtml": pd['contenthtml']})
                    print(doc[0]['ID'])
                    pdCollection.updateOne(doc)
                    doc.clear()
                    print ("create post ok")
                else:
                    print ("create post error")
                
                total += 1
                print('total=' + str(total) + ', title=' + pd['title'])
                
        print ('Creawte all posts ok')
        
    except Exception as err :
        print(err)
        
if __name__=="__main__":
    print("main")
    createAllPost()
    print("exit")