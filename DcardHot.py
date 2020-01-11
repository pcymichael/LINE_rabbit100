import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver

def Hot():
    url1='https://www.dcard.tw/f'
    print("******************新頁面******************")
        
    #瀏覽器轉跳至當前的網址
    resp=requests.get(url1)
    soup = BeautifulSoup(resp.text,"html.parser") #讀進soup中
    li=soup.find_all('h3',class_='Title__Text-v196i6-0 gmfDU')
    rf=soup.find_all('a',class_='PostEntry_root_V6g0rd')
    li_rf=[]
    for i in rf:
        li_rf.append('https://www.dcard.tw'+i.get('href'))
    return li_rf