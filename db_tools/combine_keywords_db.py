# -*- coding: utf-8 -*-
from tools.basic import exception
import copy
import sqlite3 as sql
import re


@exception
def keyword_plus(key,val,type_dic):
    check = db_get('key_words',key)
    type_dic=str_to_dic(type_dic)
    if check:
        pval,pdic = check
        if not (pdic and type_dic):print(key,val)
        newval=pval+val
        pdic = str_to_dic(pdic)
        dic = dic_combine(type_dic,pdic)
        keyword_update('key_words',key,newval,dic)
    else:keyword_insert('key_words',key,val,type_dic)
    
@exception
def dic_to_str(dic):
    s = re.sub("[\'\{\} ]+",'',str(dic))
    return s

@exception
def str_to_dic(string):
    dic={}
    for item in string.split(','):
        key,val = item.split(':')
        dic[key] = int(val)
    return dic

@exception
def db_get(table,keyword):
    cursor.execute("select * from {} where name = '{}'".format(table,keyword))
    result = cursor.fetchone()
    if result:return result[1:]

@exception
def keyword_update(table,keyword,val,dic):
    cursor.execute("update {0} set val={2} ,types='{3}' where name='{1}'".format(table,keyword,val,dic_to_str(dic)))

@exception
def keyword_insert(table,keyword,val,dic):
    cursor.execute("insert into {0} values('{1}',{2},'{3}')".format(table,keyword,val,dic_to_str(dic)))

@exception
def dic_combine(dic1,dic2):#from 2 to 1
    dic=copy.copy(dic1)
    for i,v in dic2.items():
        if i in dic:dic[i]+=v
        else:dic[i]=v
    return dic

if __name__=='__main__':
    db = sql.connect('tech.db')
    cursor = db.cursor()
    cursor.execute('select * from key_words')
    result=cursor.fetchall()
    total=len(result)
    count=0
    db.close()
    db = sql.connect('test.db')
    cursor = db.cursor()
    for key,val,type_dic in result:
        count+=1
        print('input db..',round(count/total*100,2),'%',end='\r')
        #print(key,val,type_dic)
        keyword_plus(key,val,type_dic)
    db.commit()
    db.close()


