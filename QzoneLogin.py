# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import requests
import json
import time
import time
import numpy as np
import math
import Logging


def getGTK(skey):
    h = 5381
    for i in skey:
        h += (h << 5) + ord(i)
    return h & 2147483647


Qzoneurl='https://user.qzone.qq.com/' #修改成你要的地址
referer='https://user.qzone.qq.com/'
tagrgeturl='https://user.qzone.qq.com/'

def loginQzone(qq,pwd):
    
    Logging.logout("INITIAL","程序初始化")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox') 
    driver = webdriver.Chrome(executable_path="./chromedriver",options=chrome_options) 
    # driver = webdriver.Chrome(options=chrome_options) 
    driver.get(Qzoneurl)
    time.sleep(5)
    Logging.logout("INITIAL","程序启动，已打开QQ空间")
    try:
        driver.find_element_by_id("login_frame")
        a = True
    except:
        a = False
        return
    if a == True:
        Logging.logout("INITIAL","找到登陆模块")
        #如果页面存在登录的DIV，则模拟登录
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id("switcher_plogin").click()
        driver.find_element_by_id('u').clear()
        driver.find_element_by_id('u').send_keys(qq)
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys(pwd)
        driver.find_element_by_id('login_button').click()
        time.sleep(15)



        # fo = open("login.html", "w")
        # fo.write(str(driver.execute_script("return document.documentElement.outerHTML")))
        # # 关闭打开的文件

        # fo.close()

        #找到qq登陆拼图模块
        try:



            driver.find_element_by_id("tcaptcha_iframe")
            driver.switch_to.frame('tcaptcha_iframe')
            WebDriverWait(driver, 5, 0.5).until(
                EC.presence_of_element_located((By.ID, "tcaptcha_drag_button"))
            )
            try:
                button = driver.find_element_by_id('tcaptcha_drag_button')
                Logging.logout("INITAIL",'get drag button success')
            except Exception as e:
                Logging.logout('get button failed')
                return


        except:
            Logging.logout("ERROR","未找到拼图模块")
            return 

        distance = 195
        time.sleep(3)
        
        old_strs = driver.current_url
        offsets=[[10,20,30,40,40,25],[10,20,30,40,40,30],[10,20,30,40,40,35]]
        i=0
        while 1:
            Logging.logout("INITIAL",'第 %d 次登陆尝试'% i)
            strs = driver.current_url
            if old_strs!=strs:
                Logging.logout("INITIAL","登陆成功，当前页面%s" %strs)
                break


            
            action = ActionChains(driver)
            action.click_and_hold(button)
            for x in offsets[i%3]:
                action.move_by_offset(x, 0)
            action.release()
            action.perform()
            time.sleep(3)
            i=i+1
    
    driver.switch_to.default_content()

    time.sleep(2)
    cookies=driver.get_cookies()

    
    
    
    cookies_dict = dict()
    qzonetoken = driver.execute_script('return window.g_qzonetoken;')
    Logging.logout("INITIAL","tokens: %s"%qzonetoken)


    for domain in cookies:
        if domain['name']=='p_skey':
            Logging.logout("INITIAL","g_tk: %s"%getGTK(domain['value']))
            g_tk=getGTK(domain['value'])
        cookies_dict[domain['name']] = domain['value']

    driver.quit()


    return cookies_dict,qzonetoken,g_tk

def _getListofvisitors(cookies,qzonetoken,g_tk):



    cookie = cookies
    get_url = targerurl+'&g_tk='+str(g_tk)+'&qzonetoken='+qzonetoken+'&g_tk='+str(g_tk)

    headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'referer': referer,  #修改成你要的地址
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
    
    
    }
    # 每次都要加带有cookie的headers
    b = requests.get(get_url,headers=headers,cookies=cookies) 


    # 使用json解析Callback
    jsonstring=b.text
    jsonstring=jsonstring[jsonstring.find("(")+1:]
    jsonstring=jsonstring[:len(jsonstring)-2]
    jsonstring=jsonstring.replace("\'","\"")

    fo = open("test.txt", "w")
    fo.write(jsonstring)
    # 关闭打开的文件

    fo.close()
 