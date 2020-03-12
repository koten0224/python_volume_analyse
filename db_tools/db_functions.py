# -*- coding: utf-8 -*-
import re
import copy
import time
import queue
from threading import Semaphore as sm
from threading import Thread as thr
from time import sleep
if __name__=='__main__':
    import os,sys
    sys.path.append('\\'.join(os.getcwd().split('\\')[:-1]))
from tools.basic import exception
import tools.koten_analyze as koten_analyze

@exception
def analyze(que_in,que_out):
    while 1:
        if que_in.empty():
            time.sleep(10)
            continue
        type,url,txt=que_in.get()
        result = koten_analyze.start(txt)
        if not result:
            print('\nresult empty.')
            return
        else:
            obj=type,url,result
            que_out.put(obj)

@exception
def mp_analyze(que_in,que_out):
    que_check = queue.Queue()
    for _ in range(10):thr(target=analyze,args=(que_check,que_out)).start()
    while 1:
        if que_in.empty():
            time.sleep(10)
            continue
        obj=que_in.get()
        if not obj[2] or len(re.sub('[\Wa-zA-Z0-9_]+','',obj[2]))<200 :continue
        que_check.put(obj)

    

'''
dic type is about:
{
'total_amount':2121,
'key_words':{
            '是':{
                'val':1,
                'types':{
                        '生活':1
                        }
                    },
            '一':{
                'val':4,
                'types':{
                        '生活':1,
                        '政治':3
                        }
                    },
            '馬英九':{
                'val':5,
                'types':{
                        '政治':5
                        }
                    }
            },
'urls':{
        '**url':'政治',
        '**url':'政治',
        '**url':'政治',
        }
}
'''
@exception
def input_tempdic(tempdic,type,url,result):
    if 'total_amount' not in tempdic:tempdic['total_amount']=0
    if 'key_words' not in tempdic:tempdic['key_words']={}
    if 'urls' not in tempdic:tempdic['urls']={}
    
    cur_val=set(result.values()).pop()
    tempdic['total_amount']+=cur_val

    key_words=tempdic['key_words']
    for key in result:
        if key in key_words:
            word_dic=key_words[key]
            word_dic['val']+=cur_val
            if type in word_dic['types'] : word_dic['types'][type]+=cur_val
            else:word_dic['types'][type]=cur_val
        else:key_words[key]={'val':cur_val,'types':{type:cur_val}}
        
    tempdic['urls'][url]=type

@exception
def input_db(tempdic,cursor):
    print('\ninput db..',end='\r')
    cursor.execute("select val from variable where name = 'total_amount'")
    total_amount=cursor.fetchone()[0]+tempdic['total_amount']
    cursor.execute("update variable set val={} where name='total_amount'".format(total_amount))
    
    key_words=tempdic['key_words']
    key_words_length = len(key_words)
    key_words_count = 0
    for key,content in key_words.items():
        key_words_count+=1
        print('input db..',round(key_words_count/key_words_length*100,2),'%',end='\r')
        val=content['val']
        if val==1:continue
        types_input=content['types']
        cursor.execute("select * from key_words where name='{}'".format(key))
        result=cursor.fetchone()
        if result:
            val+=result[1]
            types_db=str_to_dic(result[2])
            for i,v in types_db.items():
                if i in types_input:types_input[i]+=v
                else:types_input[i]=v
            cursor.execute("update key_words set val={1},types='{2}' where name='{0}'".format(key,val,dic_to_str(types_input)))
        else:
            cursor.execute("insert into key_words values('{}',{},'{}')".format(key,val,dic_to_str(types_input)))
        

    urls=tempdic['urls']
    for url,type_ in urls.items():
        cursor.execute("insert into urls values('{}','{}')".format(type_,url))
    print('\ninput finish.')
@exception
def dic_to_str(dic):
    return re.sub('[\{\}\' ]+','',str(dic))

@exception
def str_to_dic(string):
    dic={}
    for obj in string.split(','):
        key,val=obj.split(':')
        dic[key]=int(val)
    return dic

