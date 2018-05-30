#!/usr/bin/python
# coding=utf-8

from Utils.mongo_helper import MongoHelper

MONGO_HOST = "172.16.40.140"
MONGO_DATABASE_NAME = "ZDBBingCom"

def dump():
    collection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, 'keyword')
    total = 0
    while True:
        list = collection.nextPage(100)    
        if list == None or len(list) == 0:
            break
        total += len(list)
        print ("total=" + str(total))
    print ("total=" + str(total))

    collection.resetStartId()
    total = 0
    while True:
        list = collection.nextPage(100)    
        if list == None or len(list) == 0:
            break
        total += len(list)
        print ("second total=" + str(total))
    print ("second total=" + str(total))

if __name__=="__main__":
    print("main")
    dump()
    print("exit")
    
    
    
    
    