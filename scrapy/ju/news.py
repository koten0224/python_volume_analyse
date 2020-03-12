# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import json
from bs4 import BeautifulSoup
import re
import pandas


commenturl='https://comment.sina.com.cn/page/info?version=1&format=json' \
           '&channel=gn&newsid=comos-{}&group=undefined&compress=0&' \
           'ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread' \
           '=1&callback=jsonp_1543748934208'
# 獲取評論數
def getCommentCounts(newsurl):
    #獲取沒則新聞的編號（正則表示式）
    m = re.search('doc-i(.*).shtml', newsurl)
    newsid = m.group(1)
    #格式化連結中的的大括號
    comments = requests.get(commenturl.format(newsid))
    #把加了js外套的json變成標準json
    jd = json.loads(comments.text.strip('jsonp_1543748934208()'))
    #獲取評論數
    return jd['result']['count']['total'];

# 提取每則新聞的內文
def getNewsDetail(newsurl):
    # 定義一個字典儲存資訊
    result = {}
    rsp = requests.get(newsurl)
    rsp.encoding = 'utf-8'
    soup = BeautifulSoup(rsp.text,'html.parser')
    # 獲取標題
    result['source'] = soup.select('.source')[0].text
    # 獲取內容
    result['comment']=getCommentCounts(newsurl)
    return result

# 獲取分頁連結
def parseListLinks(url):
    newsdetails = []
    rsp = requests.get(url)
    # 把加了js外套的json變成標準json
    jsonUrl = '{' + str(rsp.text.lstrip('try{feedCardJsonpCallback(').rstrip(') ;}catch(e){};')) + '}}'
    jd=json.loads(jsonUrl)
    # 獲取每頁的新聞連結
    for ent in jd['result']['data']:
        newsdetails.append(getNewsDetail(ent['url']))
    return newsdetails

url='https://feed.sina.com.cn/api/roll/' \
    'get?pageid=121&lid=1356&num=20&versionNumber=1.2.4' \
    '&page={}&encode=utf-8&callback=feedCardJsonpCallback&_'
news_total = []
for i in range(1,3):#爬取的頁數自己設定
    # 格式化連結中的大括號
    newsurl = url.format(i)
    newsary = parseListLinks(newsurl)
    news_total.extend(newsary)
# 使用pandas模組使爬取到的資訊格式化
df = pandas.DataFrame(news_total)
# 儲存為xlsx檔案
df.to_excel('news.xlsx')
