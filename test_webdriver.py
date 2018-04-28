#coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import pickle
import json

#driver = webdriver.PhantomJS(executable_path='D:\work\nutch\resource\phantomjs-2.1.1-windows\phantomjs.exe')

def screenCapture() :
    #phantomjs_path = r'D:\work\nutch\resource\phantomjs-2.1.1-windows\phantomjs.exe'
    #driver = webdriver.PhantomJS(phantomjs_path)
    driver = webdriver.PhantomJS('phantomjs.exe')

    urlList = ["http://www.focuschina.com/", "http://www.google.com/", "https://item.jd.com/2967929.html"]
    fileId = 0
    for url in urlList:
        print(time.time())
        driver.get(url)
        try: 
            div = driver.find_element_by_id('ckepop')
        except Exception as err: 
            print(err) 
        finally: 
            print("Goodbye!")
        print (driver.current_url)
        path = 'd:\show' + str(fileId) + '.png'
        driver.get_screenshot_as_file(path)
        fileId += 1
        print (time.time())
        print ("=================")
    driver.quit()

def brandCapture() :
    #phantomjs_path = r'D:\work\nutch\resource\phantomjs-2.1.1-windows\phantomjs.exe'
    #driver = webdriver.PhantomJS(phantomjs_path)
    driver = webdriver.PhantomJS('phantomjs.exe')

    urlList = ["http://www.beautypedia.com/skin-care-reviews/by-brand/acneorg"]
    fileId = 0
    for url in urlList:
        print (time.time())
        driver.get(url)
        try: 
            title = driver.find_element_by_xpath("//A[@class='integration name']")
            logo = driver.find_element_by_xpath("//A[@class='integration image']/IMG")
            story = driver.find_element_by_xpath("//p[@class='description']")
        except Exception as err: 
            print(err) 
        finally: 
            print("Goodbye!")
        print (driver.current_url)
        path = 'd:\show' + str(fileId) + '.png'
        driver.get_screenshot_as_file(path)
        fileId += 1
        print (time.time())
        print ("=================")
    driver.quit()
    
def amazonLoad() :
    #phantomjs_path = r'D:\work\nutch\resource\phantomjs-2.1.1-windows\phantomjs.exe'
    #driver = webdriver.PhantomJS(phantomjs_path)
    driver = webdriver.PhantomJS('phantomjs.exe')

    urlList = ["http://www.amazon.com/gp/product/B00I15SB16", "https://www.amazon.com/gp/product/B00I15SB16"]
    fileId = 0
    for url in urlList:
        print (time.time())
        try: 
            driver.get(url)
            print ('ok')
            print (driver.current_url)
            print (len(driver.page_source))
            path = 'd:/amazon.' + str(fileId) + '.html'
            file = open(path, 'w')
            file.write(driver.page_source)
            file.close()
            fileId += 1
            print (time.time())
            print ("=================")
        except Exception as err: 
            print(err) 
        finally: 
            print("Goodbye!")
    driver.quit()

def chromeLoad() :

    try:
        #driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
        driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')  # Optional argument, if not specified will search path.
        driver.get('http://www.google.com/xhtml');
        print("ok")
        return
        time.sleep(5) # Let the user actually see something!
        search_box = driver.find_element_by_name('q')
        search_box.send_keys('ChromeDriver')
        search_box.submit()
        time.sleep(5) # Let the user actually see something!
        pickle.dump( driver.get_cookies() , open("d:/cookies.pkl", "wb"))
    except Exception as err: 
        print(err)
    
    driver.quit()

def weiboLoad() :

    try:
        #driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
        driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')  # Optional argument, if not specified will search path.
        driver.get('http://weibo.com');
        time.sleep(5) # Let the user actually see something!
        pickle.dump( driver.get_cookies() , open("d:/cookies.pkl", "wb"))
        with open("d:/cookies.pkl", "rb") as fpick:
            with open("d:/data.json", "w") as fjson:
                json.dump(pickle.load(fpick), fjson)
    except Exception as err: 
        print(err)
    
    driver.quit()

if __name__=="__main__":
    print("main")
    #screenCapture()
    #brandCapture()
    #amazonLoad()
    chromeLoad()
    #weiboLoad()
    print("exit")
