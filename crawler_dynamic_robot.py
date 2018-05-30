# coding=utf-8
import time
import sys
import json
from selenium import webdriver
from Utils.http_helper import HttpHelper

DISPATCHER_URL = "http://dispatcher.9in.com:8088"
DATACENTER_URL = "http://datacenter.9in.com:8088"

def getTask():
    try: 
        req = {
            'uid': 'NET_0',
            'whiteList': ['default.robot']
        }
        errorCode, rsp = HttpHelper.post(DISPATCHER_URL + "/webapi/task2", req)
        if rsp != None and 'errorCode' in rsp and rsp['errorCode'] == 'OK' and 'taskList' in rsp and rsp['taskList'] != None:
            task = rsp['taskList'][0]
            print ("get task ok, task=" + json.dumps(task))
            return ['OK', task]
        else:
            print ("get task error, rsp=" + json.dumps(rsp))
            return [rsp['errorCode'], None]
        
    except Exception as err :
        print(err)
        return ['UNKNOWN', None]

def fetchTask(driver, task):
    try: 
        url = task['url']
        html = None
        
        # Fetch
        driver.get('about:blank')
        time.sleep(1)
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        
        if html == None or len(html) < 1024:
            print ("fetchTask ERROR: HTML Error")
            return ['FETCH_ERROR_HTML', None]            

        print ("html.length={0}".format(len(html)))
        
        # Robot Check
        robotRule = task['robotRule']
        value = robotRule['value']
        if value != None and len(value) > 0:
            if value in html:
                print ('Robot check error !!!')
                print ("fetchTask ERROR: Robot Error")
                return ['FETCH_ERROR_ROBOT', None]
            else:
                print ("fetchTask OK")
                return ['OK', html]
        else:
            print ("fetchTask ERROR: Robot Rule Error")
            return ['FETCH_ERROR_RULE', html]            
        
    except Exception as err :
        print(err)
        return ['FETCH_ERROR_EXCEPTION', None]

def sendPage(task, html):
    if html != None and len(html) > 1024:
        req = {
            'task': task,
            'redirectUrl': task['url'],
            'page': {
                'content': None,
                'encoding': 'UTF8',
                'html': html,
            },
        }
        errorCode, rsp = HttpHelper.post(DATACENTER_URL + "/webapi/page2", req)
        if rsp != None and 'errorCode' in rsp and rsp['errorCode'] == 'OK':
            print ("sendPage OK: url: {0}".format(DATACENTER_URL + "/webapi/page2"))
            return True
        else:
            print ("sendPage ERROR: url: {0}".format(DATACENTER_URL + "/webapi/page2"))
            return False

def completeTask(task):
    try: 
        req = {
            'uid': 'NET_0',
            'task': task
        }
        errorCode, rsp = HttpHelper.post(DISPATCHER_URL + "/webapi/complete2", req)
        if rsp != None and 'errorCode' in rsp and rsp['errorCode'] == 'OK':
            print ("complete task ok, task=" + json.dumps(task))
        else:
            print ("complete task error, rsp=" + json.dumps(rsp))
    except Exception as err :
        print(err)

if __name__=="__main__":
    print("main")
    try: 
        runCount = 1
        if len(sys.argv) == 2:
            runCount = int(sys.argv[1])
        print ("##### RunCount={0}".format(runCount))
        
        driver = webdriver.PhantomJS('phantomjs.exe')

        for index in range(0, runCount, 1):
            print ("##### Run: {0} / {1}".format(index, runCount))
            
            errorCode, t = getTask()
            if errorCode == "NO_MORE_TASK":
                break
            elif errorCode == "OK" and t != None:
                errorCode, html = fetchTask(driver, t)
                if errorCode == 'ROBOT':
                    print ('Robot error, exit')
                    break
                elif errorCode == 'OK':
                    if html != None:
                        rc = sendPage(t, html)
                        if rc:
                            completeTask(t)
                else:
                    print ('Fetch error, continue')    
            else:
                time.sleep(1)
                
    except Exception as err :
        print(err)
    finally:
        if driver != None:
            driver.quit()
                
    print("exit")