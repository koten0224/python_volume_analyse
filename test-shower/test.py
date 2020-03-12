# -*- coding: utf-8 -*-

import sqlite3 as sql
import re
'''
關鍵字權重測試功能
'''
def show(search_keys):
    db = sql.connect('test.db')
    cursor = db.cursor()
    cursor.execute("select * from key_words where length(name)>1")
    dic={}
    for i in range(len(search_keys)):
        search_keys[i]='(?<='+search_keys[i]+':)\d+'
    search_key = '|'.join(search_keys)

    for key,val,types in cursor.fetchall():
        result = re.findall(search_key,types)
        if len(result)==len(search_keys):
            type_val=0
            for num in result:type_val+=int(num)
            dic[key]=type_val**1.1/val,type_val,val
    db.close()
    return sorted(list(dic.items()),key=lambda x:x[1][0],reverse=True)

if __name__=='__main__':
    search_keys = ['科技']
    print(show(search_keys)[:30])
