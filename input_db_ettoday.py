# -*- coding: utf-8 -*-
'''
整合爬蟲程式跟分析關鍵字並輸入資料庫
只要改import的爬蟲py檔
再標誌好該網站對應的category(詳見category_dic)
就可以開始作業
'''
import time
import sqlite3 as sql
from db_tools.db_functions import mp_analyze,input_tempdic,input_db
from threading import Thread as thr
from threading import Semaphore as sm
import queue
import scrapy.ettoday_scrapy as ettoday

if __name__=='__main__':
    category_dic = {"政治":"政治","財經":"投資","論壇":"政治",
                    "國際":"政治","大陸":"政治","社會":"生活",
                    "地方":"生活","新奇":"生活","生活":"生活",
                    "寵物動物":"生活","影劇":"娛樂","體育":"運動",
                    "旅遊":"娛樂","消費":"娛樂","名家":"娛樂",
                    "ET來了":"閒聊","3C家電":"科技","健康":"生活",
                    "男女":"心情","公益":"生活","遊戲":"遊戲",
                    "電影":"娛樂","時尚":"娛樂","網搜":"閒聊",
                    "電商":"投資","親子":"心情","房產雲":"投資",
                    "ET車雲":"娛樂","軍武":"政治","保險":"投資",
                    "法律":"學術","直銷雲":"投資","探索":"生活",
                    "運勢":"閒聊"}

    db = sql.connect('test.db')
    cursor = db.cursor()
    que_scrapy = queue.Queue()
    que_input = queue.Queue()
    sem_scrapy = sm(10)
    temp_dic = {}
    counter = 0
    
    thr(target=ettoday.start,args=(1000000,que_scrapy,sem_scrapy)).start()
    print('scrapy already.')
    time.sleep(5)
    thr(target=mp_analyze,args=(que_scrapy,que_input)).start()
    print('analyze already.')
    time.sleep(5)
    print('go')
    
    while 1:
        if que_input.empty():
            time.sleep(10)
            if que_input.empty():
                print('\nmain input waiting..')
                continue
        type,url,result = que_input.get()
        print(' '*79,end='\r')
        print(type,url,end='\r')
        cursor.execute("select * from urls where url = '{}'".format(url))
        if cursor.fetchone():
            print('\ndrop out.find url.')
            continue
        input_tempdic(temp_dic,category_dic[type],url,result)
        counter+=1
        if counter>=3000 or que_input.empty():
            print('\n',counter,'datas to insert.')
            input_db(temp_dic,cursor)
            db.commit()
            counter=0
            temp_dic={}
        
