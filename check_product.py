#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Utils.http_helper import HttpHelper
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
import re


'''
该函数用于检测站中产品在电商站中所对应产品是否存在
'''
def check_product():
    url = "https://mistinhaler.com/"
    while url is not None:
        title = ""
        statuscode, html = HttpHelper.fetch(url)
        soup = BeautifulSoup(html, "lxml")
        li_all = soup.find_all("li", attrs={"class": re.compile("^post-\d* product type-product status-publish")})
        for li in li_all:
            # print(li['class'][0])
            title = li.find("h2", attrs={"class": "woocommerce-loop-product__title"}).text
            driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')
            driver.get("https://www.amazon.com/")
            driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').send_keys(title)
            submit = driver.find_element_by_xpath("//*[@id=\"nav-search\"]/form/div[2]/div/input")
            ActionChains(driver).move_to_element(submit).click(submit).perform()
            html = driver.page_source.encode("utf-8")
            driver.close()
            soup2 = BeautifulSoup(html, "lxml")
            a = soup2.find_all("h1", attrs={"id": "noResultsTitle"})
            if a != []:
                print(li['class'][0])

        next_page = soup.find_all("a", attrs={"class": "next page-numbers"})
        if next_page == []:
            url = None
            continue
        for i in next_page:
            url = i['href']


if __name__ == "__main__":
    check_product()
    print("exit")