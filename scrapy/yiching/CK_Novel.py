# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 18:59:30 2019

@author: pipiching
"""

import requests
from bs4 import BeautifulSoup as bs
import queue
import threading


# ---------- 卡提諾小說 ---------- ##
def start(n, semaphore, queue):
    url = 'https://ck101.com/novel/'
        
    res_novel = requests.get(url, headers = headers)
    soup = bs(res_novel.text, 'html.parser')
    titles = soup.select('div.novelidx-box.categories div div a')
    
    def Get_Content(url, semaphore, queue, n):
        print(url, ' start')
        global counts
        
        while url:
            if counts > n:
                return
            res = requests.get(url, headers=headers)
            soup = bs(res.text, 'html.parser')    
            Books_Url = soup.select('table tbody td a')
            
            
            threads_2 = []
            for i in range(len(Books_Url)): # 每個小說一個線程
                threads_2.append(threading.Thread(target=Get_String, args=(Books_Url[i]['href'], semaphore, queue, n)))
                threads_2[i].start()
                
            for thread in threads_2:
                thread.join()
            
            url = Next_page(soup)
                
        print('---finish---')
        
    def Get_String(url, semaphore, queue, n):    
        global counts
        semaphore.acquire()
        #print(url + ' sub start')
        if counts > n:
            semaphore.release()
            return    
        
        orig_url = url
        string = ''
        # 第一回忽略 抓出來特別做
        res = requests.get(url, headers=headers)
        soup = bs(res.text, 'html.parser')
        contents = soup.find_all('td', class_='t_f')
        cla = soup.select_one('div.ts a')
        if cla:
            cla = cla.text[1:-1]
        for content in contents[1:]:                
            string += str.strip(content.text)
        url = Next_page(soup)
        
        while url: 
            res = requests.get(url, headers=headers)
            soup = bs(res.text, 'html.parser')
            contents = soup.find_all('td', class_='t_f')                     
            
            for content in contents:                
                string += str.strip(content.text) + '\n'
                                       
            url = Next_page(soup) # 換頁
        
        if string:
            queue.put([cla, orig_url, string])
            counts += 1       
            print('完成{}篇'.format(counts) )
            
        semaphore.release() 

    def Next_page(soup): # 下一頁   
        url = soup.find(class_='nxt')
        if url:
            url = url['href']
        
        return url
        ####### 卡提諾小說 ###########

    
    # 取得各類型小說
    Class_Url = []
    Class = [] 
    for cla in titles:
        Class_Url.append('https://ck101.com/' + cla['href']) 
        Class.append(str.strip(cla.text))
        if titles.index(cla) == 9:
            break        
    
    threads = []  # 每種小說一個線程    
    for i in range(len(Class_Url)):
        res = requests.get(Class_Url[i], headers = headers)
        soup = bs(res.text, 'html.parser')
        url = soup.find(class_='nxt')
        if url:  
            url = url['href']
        else:
            url = Class_Url[i]
        
        threads.append(threading.Thread(target = Get_Content, args = (url, semaphore,queue,n)))
        
    for i in range(len(threads)):    
        threads[i].start()
    for i in range(len(threads)):
        threads[i].join()
        
    print('Done')
    

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}       
counts = 0

if __name__=='__main__':
    my_queue = queue.Queue()
    semaphore = threading.Semaphore(10)
    start(10, semaphore, my_queue)    
    
