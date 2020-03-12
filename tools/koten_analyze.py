# -*- coding: utf-8 -*-
import re
from math import log
from tools.basic import exception
level=8

@exception
def start(txt):
    return cleaner(*txt_analyze(txt))

class phrase:
    def __init__(self,length):
        self.body = ''
        self.length = length
    @exception
    def put(self,val):
        if type(val)!=str:return
        self.body+=val
        if len(self.body)>self.length:
            self.body = self.body[1:]
        if len(self.body)==self.length:
            return self.body

class counter:
    def __init__(self):
        self.dic={}
        self.length = 0
    @exception
    def word_dissociate(self,txt):
        phrases = [phrase(i+1) for i in range(level+1)]
        txt = re.sub('[的啊哈啦]+','',txt)
        for s in txt:
            self.length += 1
            for e in phrases:
                word = e.put(s)
                if word:
                    if word in self.dic:
                        self.dic[word]+=1
                    else:self.dic[word]=1
                    
@exception
def txt_analyze(txt):
    count_dic = counter()
    for sentence in re.split('[\Wa-zA-Z0-9_]+',txt):
        count_dic.word_dissociate(sentence)
    dic = count_dic.dic
    del_list = set()
    for word,val in dic.items():
        if len(word)==1:continue
        if len(word)==level+1:del_list.add(word)
        for nextword in [word[1:],word[:-1]]:
            if nextword in dic and abs(dic[nextword]-val)/val<=0.01:
                del_list.add(nextword)
                #del because it's a child
    for word in del_list:
        del dic[word]
        #delcount+=1
    return count_dic.length,dic

@exception
def cleaner(length,dic):
    var_clean = int(log(length,1.59))-11
    var_output = int(log(length,11.22))-1
    var_output = var_output if var_output > 1 else 1
    del_list = set()
    for word,val in dic.items():
        if val<=var_clean:del_list.add(word)
    for word in del_list:del dic[word]
    return {key:var_output for key in dic}

if __name__=='__main__':
    with open('fate-hunter.txt','r') as file:
        txt=file.read()
    dic = start(txt)
    
