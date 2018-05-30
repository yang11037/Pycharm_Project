# coding=utf-8
import requests
import hashlib
import os
import json

class HttpHelper:
    
    def __init__(self):
        pass
    
    @staticmethod
    def fetch(url, encoding = "utf-8", headers = None):
        try:
            defaultHeaders = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            }
            if headers != None:
                defaultHeaders = headers;
                
            rsp = requests.get(url, headers=defaultHeaders)
            statusCode = rsp.status_code
            html = None
            if statusCode == 200 or statusCode == 201:
                if rsp.apparent_encoding != None:
                    html = rsp.content.decode("utf-8")
                else:
                    html = rsp.content.decode(encoding)
                        
            return [statusCode, html]
        except Exception as err :
            print(err)
            return [407, None]        

    @staticmethod
    def fetchAndSave(url, encoding, rootPath):
        try:
            statusCode, html = HttpHelper.fetch(url, encoding)
            if statusCode != 200:
                return None
            
            m = hashlib.md5()
            m.update(url.encode("utf-8"))
            fileName = m.hexdigest() + ".html"
            prefix = fileName[0:1]
            filePath = rootPath + "\\" + prefix
            if not os.path.exists(filePath):
                os.makedirs(filePath, 0o755);
            filePath += "\\" + fileName    
            # save html
            if html == None or len(html) <= 2048:
                return None
            
            with open(filePath, 'w', encoding='utf-8') as file:
                file.write(html)
            return fileName
        except Exception as err :
            print(err)
            return None
        
    @staticmethod
    def getFullPath(rootPath, fileName):
        prefix = fileName[0:1]
        filePath = rootPath + "/" + prefix + "/" + fileName
        return filePath

    @staticmethod
    def get(url):
        try:
            defaultHeaders = {
                #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            }
            httpRsp = requests.get(url, headers=defaultHeaders)
            statusCode = httpRsp.status_code
            if statusCode == 200:
                jsonBody = httpRsp.content.decode("utf-8")
                response = json.loads(jsonBody)
                return ['OK', response]
            else:
                return ['HTTP_ERROR', None]
        except Exception as err:
            print(err)
            return ['OTHER', None]

    @staticmethod
    def post(url, request, basicAuth = None):
        try:
            defaultHeaders = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                'Content-Type': 'application/json',
            }
            httpRsp = requests.post(url, json=request, headers=defaultHeaders, auth=basicAuth)
            statusCode = httpRsp.status_code
            if statusCode == 200:
                jsonBody = httpRsp.content.decode("utf-8")
                response = json.loads(jsonBody)
                return ['OK', response]
            else:
                return ['HTTP_ERROR', None]
        except Exception as err :
            print(err)
            return ['OTHER', None]

if __name__=="__main__":
    print("main")
    print("exit")
