# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 18:04:05 2019

@author: pipiching
"""

import requests
from bs4 import BeautifulSoup as bs
import datetime
import pandas as pd
import queue
import threading

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}    
counts = 0

def start(n, semaphore, queue): 
    global counts
    def Get_list():# 取得月份 
        today = datetime.datetime.today().strftime('%Y-%m')
        Month_list = pd.date_range('2003-03',today,freq='MS').strftime("%Y-%m").tolist()
       
        return Month_list
    
    def GNN_News(date, n, queue, semaphore): # GNN 底下的新聞
        url = 'https://gnn.gamer.com.tw/'
        year = date[:4]
        month = date[5:7]
        payLoad={'yy':year, 'mm':month}
        res = requests.get(url, headers = headers, params=payLoad)
        print(year, month)
        soup = bs(res.text, 'html.parser')
        news = soup.select('div.GN-lbox2B h1 a')
        
        threads = []
        for i in range(len(news)):
            url_new = 'https:' + news[i]['href']
            threads.append(threading.Thread(target=Get_string, args=(url_new, n, queue, semaphore)))
            threads[i].start()
            
        for thread in threads:
            thread.join()
        
    def Get_string(url, n, queue, semaphore): # 取得文章內容
        global counts
        semaphore.acquire()
        if counts > n:
            semaphore.release()
            return
        res_new = requests.get(url)
        res_new.encoding = 'utf8'
        soup_new = bs(res_new.text, 'html.parser')
        content = soup_new.select('div.GN-lbox3B')
        
        string = ''
        for i in content:
            temp = i.text
            if temp:
                string += temp + '\n'
        if string:
            queue.put(['遊戲', url, string])
            counts += 1
            print('完成{}篇'.format(counts))
        else:
            print(url) # 沒爬成功的
        semaphore.release() 
    Month_list = Get_list() 
    Month_list.reverse()
    for date in Month_list:
        #threads.append(threading.Thread(target=GNN_News, args=(date, n, queue, semaphore)))
        GNN_News(date, n, queue, semaphore)

if __name__=='__main__':
    que = queue.Queue()
    semaphore = threading.Semaphore(10)
    threading.Thread(target=start, args=(1000, semaphore, que)).start()
