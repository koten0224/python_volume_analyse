# -*- coding: utf-8 -*-
import sqlite3 as sql
import math
import random
import tools.koten_analyze
from db_functions import str_to_dic

db = sql.connect('test.db')
cursor = db.cursor()
'''
文章分析程式，判斷並回傳該文章所屬之領域
比如文章屬於政治、投資或生活、娛樂..等等
建基於事先爬好的關鍵字資料庫
'''
#讀取關鍵字列表
cursor.execute("select * from key_words where length(name)>1 order by val desc")
key_words = {res[0]:{'val':res[1],'types':str_to_dic(res[2])} for res in cursor.fetchall()}
for key in key_words:
    type_dic = key_words[key]['types']
    type_sum = sum(type_dic.values())
    for type_ in type_dic:
        type_dic[type_]=type_dic[type_]/type_sum

#讀取文章總數
cursor.execute("select val from variable where name = 'total_amount'")
total_amount = cursor.fetchone()[0]

#讀取url列表並打亂
cursor.execute("select * from urls")
result = cursor.fetchall()
type_dic = {i[0]:[] for i in result}
for i in result : type_dic[i[0]].append(i[1])
for key in type_dic : random.shuffle(type_dic[key])
    
def txt_class(txt):
    def log(x):
        return math.log(x,10)
    def importance(word):
        try:return log(total_amount/key_words[word]['val'])
        except KeyError:return 1
    result = {key:val for dic in koten_analyze.txt_analyze(txt)[1].values() for key,val in dic.items() if len(key)>1}
    total_words_amount = sum(result.values())
    txt_type = {key:0 for key in type_dic}
    for key,val in result.items():
        newval=val/total_words_amount*importance(key)
        result[key]=newval
        if key in key_words:
            key_types = key_words[key]['types']
            for i,v in key_types.items():
                txt_type[i]+=v*newval
    return sorted(txt_type,key=lambda x:txt_type[x])[:3]

if __name__=='__main__':
    while 1:
        txt=input('enter.')
        print(txt_class(txt))

