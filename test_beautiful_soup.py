# coding=utf-8

from bs4 import BeautifulSoup
from Utils.http_helper import HttpHelper
 
def testSoup():
    url = "https://www.drugs.com/comments/abobotulinumtoxina/"
    html = HttpHelper.fetch(url)
    
    soup = BeautifulSoup(html)

    #Remove all table in div
    tableList = soup.select("div.user-comment table")
    if (len(tableList) > 0):
        for table in tableList:
            table.decompose()
    
    # get div outer html       
    divList = soup.select("div.user-comment")
    if (len(divList) > 0):
        reviewDivList = []
        for div in divList:
            divHtml = str(div)
            divText = div.text
            print (divHtml)
            reviewDivList.append(divHtml)

    
if __name__=="__main__":
    print("main")
    testSoup()
    print("exit")
