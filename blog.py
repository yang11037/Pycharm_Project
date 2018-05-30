# coding=utf-8
from bs4 import BeautifulSoup
from Utils.http_helper import HttpHelper
from Utils.mongo_helper import MongoHelper
#from url_helper import UrlHelper
from Utils.str_helper import StrHelper
from Utils.nlp_helper import NLPHelper
#from crypt_helper import CryptHelper

MONGO_HOST = "172.16.40.140"
MONGO_DATABASE_NAME = "ZDBBlog"
HTML_ROOT_PATH = "E:/NutchData/Pages/blog"
IMPORT_URL = "http://localhost:54691/DataImport/Article"

def initCat():
    catDict = {
        '糖尿病':'diabetes',
        '肺癌':'Lung cancer',
        '风湿':'Rheumatism',
        '牛皮癣':'Psoriasis',
        '肺梗阻':'Pulmonary obstruction',
        '失禁':'Incontinence',
        'aarp补充医疗':'aarp supplementary medical treatment',
        '其他疾病':'other illnesses',
        '乳腺癌':'Breast cancer',
        '多发性硬化症':'Multiple sclerosis',
        '哮喘':'Asthma',
        '药瘾':'Drug addiction',
        '酒瘾':'Alcoholism',
#         '小企业融资':'Small Business Financing',
#         'business phone':'business phone',
#         'network security':'network security',
#         'cloud':'cloud',
#         '商业软件':'commercial software',
#         '小企业软件':'Small Business Software',
#         '财务软件':'financial software',
#         '税务软件':'Tax software',
#         '小企业安卓财务app':'Small Business Android Finance app',
#         '薪酬管理软件':'Compensation Management Software',
#         'SAP':'SAP',
#         '补丁管理软件':'Patch management software',
#         '网络服务':'Internet service',
#         '域名':'Domain name',
#         '虚拟服务器':'virtual server'
    }
    collection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, 'category')
    for cname in catDict.keys():
        ename = catDict[cname]
        slug = ename.lower().replace(" ", "-")
        doc = {
            "ename": ename,
            "cname": cname,
            "slug": slug
        }
        collection.insertOne(doc)

'''def importExcelToDB():
    try: 
        catCollection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, 'category')
        collection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, 'blog')
        wb = load_workbook('D:/tmp/disease/疾病文章链接.xlsx')
        sheetNames = wb.get_sheet_names()
        print (sheetNames)
        
        blogList = []
        blogDict = {}
        for name in sheetNames:
            print (name)
            
            found = catCollection.findOneByFilter({'cname': name})
            ename = None
            if found != None:
                ename = found['ename']
            else:
                print ("cat ename NOT found, name=" + name)
                continue
            
            total = 0
            ws = wb.get_sheet_by_name(name)    
            for row in range(1, 500):
                col = "B" + str(row)
                url = ws[col].value
                if url == None or len(url) < 0:
                    continue
                url = url.lower()
                if url.startswith("http"):
                    if url in blogDict:
                        continue
                    
                    hashPos = url.find("#")
                    if hashPos > 0:
                        url = url[0:hashPos]
                    
                    host, path = UrlHelper.getHostPath(url)                    
                    blogDict['url'] = url
                    doc = {
                        "cat": name,
                        "ecat": name,
                        "url": url,
                        "host": host,
                        "key": path,
                        "state": "CREATED"
                    }
                    blogList.append(doc)
                    total += 1
            print ("total=" + str(total))
            
        collection.insertMany(blogList)
    except Exception as err :
        print(err)'''

def fetchAllBlog():
    try: 
        catCollection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, 'category')
        collection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, 'blog')
        total = 0
        while True:
            blogList = collection.nextPage(100)
            if len(blogList) == 0:
                break
            for blog in blogList:
                if blog['state'] == 'CLOSED':
                    fileName = HttpHelper.fetchAndSave(blog['url'], "utf-8", HTML_ROOT_PATH)
                    if fileName != None and len(fileName) > 0:
                        blog['fileName'] = fileName
                        blog['state'] = "FETCHED"
                    else:
                        blog['state'] = "CLOSED"
                    collection.updateOne(blog)
                    total += 1
                    print ("url=" + blog['url'])
                    print ("total=" + str(total))
                    
    except Exception as err :
        print(err)
    finally:
        print ("exit")

def parseBlog(html):
    soup = BeautifulSoup(html, "lxml")
    scripts = soup.findAll(['script', 'style', 'iframe'])
    for match in scripts:
        match.decompose()

    title = soup.find("title")
    titleContent = None
    if title != None:
        titleContent = title.text
    else:
        return [None, None, None, None, None, None, None]
    
    description = soup.find("meta", {"name": "description"})
    descriptionContent = None
    if description != None:
        descriptionContent = description.get("content")
        
    ogTitle = soup.find("meta", {"property": "og:title"})
    ogTitleContent = None
    if ogTitle != None:
        ogTitleContent = ogTitle.get("content")
    
    ogDescription = soup.find("meta", {"property": "og:description"})
    ogDescriptionContent = None
    if ogDescription != None:
        ogDescriptionContent = ogDescription.get("content")
    
    twitterTitle = soup.find("meta", {"name": "twitter:title"})
    twitterTitleContent = None
    if twitterTitle != None:
        twitterTitleContent = twitterTitle.get("content")
    
    twitterDescription = soup.find("meta", {"name": "twitter:description"})
    twitterDescriptionContent = None
    if twitterDescription != None:
        twitterDescriptionContent = twitterDescription.get("content")
    
    keyword = soup.find("meta", {"name": "keywords"})
    keywordContent = None
    if keyword != None:
        keywordContent = keyword.get("content")
    
    # Get title related Header
    headers = soup.find_all(['h1', 'h2'])
    titleHeader = None
    firstH1 = None
    firstH2 = None
    for h in headers:
        ht = h.text
        if len(ht) == 0:
            continue
        tagName = h.name
        if tagName == "h1":
            if firstH1 == None:
                firstH1 = h
        elif tagName == "h2":
            if firstH2 == None:
                firstH2 = h
        sim = StrHelper.getWordSimilarity(ht, titleContent)
        dis = StrHelper.getLevDistance(ht, titleContent) / len(ht)
        if sim > 50.0 or dis < 0.5:
            titleHeader = h
            break
    
    if titleHeader == None:
        if firstH1 != None:
            titleHeader = firstH1
        elif firstH2 != None:
            titleHeader = firstH2
    
    theParentText = None
    found = False
    author = None
    if titleHeader != None:
        theParent = titleHeader.parent
        while theParent != None:
            tagName = theParent.name
            if tagName == "article" or tagName == "div":
                theParentText = theParent.text
                theParentTextList = theParentText.split()
                if len(theParentTextList) > 128:
                    found = True
                    break
            elif tagName == "body" or tagName == "html":
                break
            
            # next parent
            theParent = theParent.parent
    
        # no parent matched
        if not found:
            bodyNode = soup.find("body")
            theParentText = bodyNode.text
            titleHeaderText = titleHeader.text
            index = theParentText.find(titleHeaderText)
            if index >= 0:
                theParentText = theParentText[index:]
            found = True
    else:
        found = True
        bodyNode = soup.find("body")
        theParentText = bodyNode.text        

    # author
    if titleHeader != None:
        titleHeaderText = titleHeader.text
        index = theParentText.find(titleHeaderText)
        if index >= 0:
            pattern = r"By[\s]+[a-zA-Z\s]+"
            authorText = StrHelper.searchOneIgnoreCase(theParentText, pattern)
            # print(authorText)
            if authorText != None:                
                indexAuthor = theParentText.find(authorText)                
                if indexAuthor > index:
                    # search count of linefeed between title and author
                    theText = theParentText[index:indexAuthor]
                    lines = theText.split('\n')
                    countLine = 0
                    for l in lines:
                        l = l.strip()
                        if len(l) > 0:
                            countLine += 1
                    if countLine <= 3:
                        index = authorText.find("\n")
                        if index > 0:
                            authorText = authorText[0:index]
                        authorText = authorText.replace("By", "").replace("by", "").strip()
                        # validate the word count of author
                        words = authorText.split()
                        if len(words) < 5:
                            author = authorText
                            print ("======>" + author)
                        else:
                            print ("======>skip, countWord=" + str(len(words)))
                    else:
                        print ("======>skip, countLine=" + str(countLine))
                            
        
    content = None
    summary = None
    summaryKeywords = None
    if found:
        content = theParentText.strip()
        summary = NLPHelper.getSummary(content)
        summaryKeywords = NLPHelper.getKeywords(summary)
        
    if summary == None or summaryKeywords == None:
        bodyNode = soup.find("body")
        theParentText = bodyNode.text
        content = theParentText.strip()
        summary = NLPHelper.getSummary(content)
        summaryKeywords = NLPHelper.getKeywords(summary)
    
    return [
        found,
        titleContent,
        descriptionContent,
        ogTitleContent,
        ogDescriptionContent,
        twitterTitleContent,
        twitterDescriptionContent,
        keywordContent,
        content,
        author,
        summary,
        summaryKeywords]
    
def parseAllBlog():
    try:
        collection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, 'blog')
        total = 0
        while True:
            blogList = collection.nextPage(100)
            if len(blogList) == 0:
                break
            for blog in blogList:
                if blog['state'] == 'PARSED':
                    filePath = HttpHelper.getFullPath(HTML_ROOT_PATH, blog['fileName'])
                    with open(filePath, 'r', encoding='utf-8') as file:
                        html = file.read()
                    found, title, desc, ogTitle, ogDesc, twTitle, twDesc, keywords, content, author, summary, summaryKeywords = parseBlog(html);
                    if found and (title != None or ogTitle != None or twTitle != None):
                        doc = {
                            'title': title,
                            'ogTitle': ogTitle,
                            'twTitle': twTitle,
                            'desc': desc,
                            'ogDesc': ogDesc,
                            'twDesc': twDesc,
                            'keywords': keywords,
                            'content': content,
                            'author': author,
                            'summary': summary,
                            'summaryKeywords': summaryKeywords
                            }
                        blog['doc'] = doc
                        blog['state'] = 'PARSED'
                        collection.updateOne(blog)
                        print ("ok")
                    else:
                        print ("error")
                        break
                        
                    total += 1
                    print ("url=" + blog['url'])
                    print ("total=" + str(total))
    except Exception as err :
        print(err)
    finally:
        print ("exit")

'''def resetBlog():
    try: 
        catCollection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, 'category')
        collection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, 'blog')
        total = 0
        while True:
            blogList = collection.nextPage(100)
            if len(blogList) == 0:
                break
            for blog in blogList:
                
                found = catCollection.findOneByFilter({'cname': blog['cat']})
                ecat = None
                if found != None:
                    ecat = found['ename']
                else:
                    print ("cat ename NOT found, name=" + blog['cat'])
                    continue

                url = blog['url']
                hashPos = url.find("#")
                if hashPos > 0:
                    url = url[0:hashPos]
                host, path = UrlHelper.getHostPath(url)
                    
                blog['ecat'] = ecat
                blog['url'] = url
                blog['host'] = host
                blog['key'] = path
                
                collection.updateOne(blog)
    except Exception as err :
        print(err)
    finally:
        print ("exit")'''
        
'''def blog2Article(blog):
    theId = ''
    title = ''
    excerpt = ''
    content = ''
    author = ''
    domain = ''
    categories = ''
    tags = ''
    url = ''
    status = 0
    key = ''
    try:
        if 'url' in blog and blog['url'] != None and len(blog['url']) > 0:
            url = blog['url']
            if len(url) >= 1000:
                url = url[0:1000]
            md5 = CryptHelper.getMD5Hash(url)
        else:
            return [None, 'URL_NOT_FOUND']
        
        doc = None
        if 'doc' in blog and blog['doc'] != None:
            doc = blog['doc']
        else:
            return [None, 'DOC_NOT_FOUND']
        
        if 'ogTitle' in doc and doc['ogTitle'] != None and len(doc['ogTitle']) > 0:
            title = doc['ogTitle']
        elif 'title' in doc and doc['title'] != None and len(doc['title']) > 0:
            title = doc['title']
        elif 'twTitle' in doc and doc['twTitle'] != None and len(doc['twTitle']) > 0:
            title = doc['twTitle']
        else:
            return [None, 'TITLE_NOT_FOUND']
        if title != None and len(title) >= 150:
            title = title[0:150]

        if 'ogDesc' in doc and doc['ogDesc'] != None and len(doc['ogDesc']) > 0:
            excerpt = doc['ogDesc']
        elif 'desc' in doc and doc['desc'] != None and len(doc['desc']) > 0:
            excerpt = doc['desc']
        elif 'summary' in doc and doc['summary'] != None and len(doc['summary']) > 0:
            excerpt = doc['summary']
        elif 'twDesc' in doc and doc['twDesc'] != None and len(doc['twDesc']) > 0:
            excerpt = doc['twDesc']
        else:
            return [None, 'EXCERPT_NOT_FOUND']
        if excerpt != None and len(excerpt) >= 500:
            excerpt = excerpt[0:500]
        
        if 'content' in doc:
            content = doc['content']
        
        if 'host' in blog and blog['host'] != None and len(blog['host']) > 0:
            domain = blog['host']
        else:
            return [None, 'DOMAIN_NOT_FOUND']
        
        author = domain
        if author.startswith('www.'):
            author = author.replace('www.', '')
        if 'author' in doc and doc['author'] != None and len(doc['author']) > 0:
            author = doc['author']
        if author != None and len(author) >= 20:
            author = author[0:20]
        
        if 'ecat' in blog and blog['ecat'] != None and len(blog['ecat']) > 0:
            categories = blog['ecat']
        else:
            return [None, 'CATEGORIES_NOT_FOUND']
        if categories != None and len(categories) >= 500:
            categories = categories[0:500]

        if 'keywords' in doc and doc['keywords'] != None and len(doc['keywords']) > 0:
            keywords = doc['keywords']
            kList = keywords.split(',')
            for k in kList:
                tags += k.strip() + ","
        elif 'summaryKeywords' in doc and doc['summaryKeywords'] != None and len(doc['summaryKeywords']) > 0:
            summaryKeywords = doc['summaryKeywords']
            kList = summaryKeywords.split('\n')
            for k in kList:
                tags += k.strip() + ","
        else:
            tags = None
        if tags != None and tags.endswith(","):
            tags = tags[0:len(tags) - 1]
        if tags != None and len(tags) >= 500:
            tags = tags[0:500]

        if 'key' in blog and blog['key'] != None and len(blog['key']):
            key = blog['key']
        else:
            return [None, 'KEY_NOT_FOUND']
        if key != None and len(key) >= 200:
            key = tags[0:200]
        
        article = {
            'md5': md5,
            'title': title,
            'excerpt': excerpt,
            'content': None,
            'author': author,
            'domain': domain,
            'categories': categories,
            'tags': tags,
            'url': url,
            'status': status,
            'key': key,
            'doc': doc
        }
        return [article, 'OK']
        
    except Exception as err :
        print(err)
        return [None, 'OTHER']'''
        
    
'''def blog2ArticleAll():
    try: 
        catDict = {
            '糖尿病':'diabetes',
            '肺癌':'Lung cancer',
            '风湿':'Rheumatism',
            '牛皮癣':'Psoriasis',
            '肺梗阻':'Pulmonary obstruction',
            '失禁':'Incontinence',
            'aarp补充医疗':'aarp supplementary medical treatment',
            '其他疾病':'other illnesses',
            '乳腺癌':'Breast cancer',
            '多发性硬化症':'Multiple sclerosis',
            '哮喘':'Asthma',
            '药瘾':'Drug addiction',
            '酒瘾':'Alcoholism',
        }
        blogCollection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, 'blog')
        articleCollection = MongoHelper(MONGO_HOST, 27017, MONGO_DATABASE_NAME, 'article')
        total = 0
        while True:
            blogList = blogCollection.nextPage(100)
            if len(blogList) == 0:
                break
            for blog in blogList:
                total += 1
                print ("total=" + str(total) + ", url=" + blog['url'])
                if blog['state'] != 'PARSED':
                    print ("invalid state skip")
                    continue
                
                cat = blog['cat']
                if not cat in catDict:
                    print ("invalid cat skip")
                    continue
                
                article, errorCode = blog2Article(blog)
                if errorCode == 'OK' and article != None:
                    found = articleCollection.findOneByFilter({'url': article['url']})
                    if found == None:
                        articleCollection.insertOne(article)
                    else:
                        article['_id'] = found['_id']                        
                        articleCollection.updateOne(article)
                    print ("blog2article ok, code=" + errorCode + ", url=" + blog['url'])
                else:
                    print ("blog2article error, code=" + errorCode + ", url=" + blog['url'])
    except Exception as err :
        print(err)
    finally:
        print ("exit")    '''

if __name__=="__main__":
    print("main")
    #initCat()
    #importExcelToDB()
    #fetchAllBlog()
    #resetBlog()
    #parseAllBlog()
    #blog2ArticleAll()
    print("exit")