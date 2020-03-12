# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
if __name__=='__main__':
    import os,sys
    sys.path.append('\\'.join(os.getcwd().split('\\')[:-1]))
from tools.basic import exception
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
'''
把requests跟BeautifulSoup的一些常用功能做簡寫and另立function
以便使過程能夠被@exception監控
'''
@exception
def session():#->session obj.
    return requests.Session()

@exception
def post(url,payload,req = requests):#->response obj.
    response = req.post(url, headers = headers,data = payload)
    response.raise_for_status()
    return response

@exception
def get(url,req = requests):#->response obj.
    response = req.get(url, headers = headers)
    response.raise_for_status()
    return response

@exception
def bs(response):#->BeautifulSoup obj.
    return BeautifulSoup(response.text,'html.parser')

@exception
def find(soup_obj,*args,**kwargs):#->BeautifulSoup obj.
    result = soup_obj.find(*args,**kwargs)
    if not result:return
    return result

@exception
def findall(soup_obj,*args,**kwargs):#->ResultSet
    result = soup_obj.find_all(*args,**kwargs)
    if not result:return
    return result
