# -*- coding: utf-8 -*-
import queue
import time
from random import randint as rd
from threading import Semaphore as sm
from threading import Thread as thr

if __name__=='__main__':
    import os,sys
    sys.path.append('\\'.join(os.getcwd().split('\\')[:-1]))

import scrapy.ettoday_functions as ettoday
from tools.basic import basic_scrapy,exception
from tools.net import get,bs

@exception
def start(max_mount,que,sem):
    counter = [0]
    class single_news(basic_scrapy):#單篇新聞爬蟲
        @exception
        def run_content(self):
            counter[0]+=1
            web = bs(get(self.url))
            mtext = ettoday.get_mtext(web)
            obj = self.type,self.url,mtext
            que.put(obj)

    class newses(basic_scrapy):#各新聞串爬蟲
        @exception
        def run_content(self):
            web = bs(get(self.url))
            thr_list=[]
            for url,type_ in ettoday.newslist(web):
                thr_list.append(single_news(url,type_))
                if len(thr_list)>=10:
                    for thread in thr_list:thread.start()
                    for thread in thr_list:thread.join()
                    thr_list=[]
            
    thr_list = []
    for url in ettoday.date_generator('2017-10-03'):
        if counter[0] > max_mount:break
        if len(thr_list)<10:thr_list.append(newses(url,''))#各新聞串爬蟲啟動
        else:
            for thread in thr_list:thread.start()
            for thread in thr_list:thread.join()
            thr_list=[]
    print('finish.')
'''
if __name__=='__main__':
    que = queue.Queue()
    sem = sm(10)
    thr(target=start,args=(500,que,sem)).start()
    time.sleep(10)
    print('done.')
    while not que.empty():
        input()
        print(que.qsize())
        obj = que.get()
        print(obj[:2])
        print()
'''

