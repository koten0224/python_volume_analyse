import pandas as pd
import requests
from requests_html import HTML
import re


# 檢視資料結構
ID = '231030181'
url = 'https://www.dcard.tw/_api/posts/' + ID
# 透過request套件抓下這個網址的資料
requ = requests.get(url)
# 初步檢視抓到的資料結構
requ.json()

# 將抓下來的資料轉為DataFrame
ID = '231030181'
url = url = 'https://www.dcard.tw/_api/posts/' + ID
requ = requests.get(url)
rejs = requ.json()
pd.DataFrame(
    data=
    [{'ID':rejs['id'],
      'title':rejs['title'],
      'content':rejs['content'],
      'excerpt':rejs['excerpt'],
      'forumName':rejs['forumName'],
      'forumAlias':rejs['forumAlias'],
      'topics':rejs['topics']}],
    columns=['ID','title','content','excerpt','forumName','forumAlias','topics'])

# 撰寫簡單的函數，透過輸入文章ID，就輸出文章的資料
def Crawl(ID):
    link = 'https://www.dcard.tw/_api/posts/' + str(ID)
    requ = requests.get(link)
    rejs = requ.json()
    return(pd.DataFrame(
        data=
        [{'ID':rejs['id'],
          'title':rejs['title'],
          'content':rejs['content'],
          'excerpt':rejs['excerpt'],
          'createdAt':rejs['createdAt'],
          'updatedAt':rejs['updatedAt'],
          'forumName':rejs['forumName'],
          'forumAlias':rejs['forumAlias'],
          'gender':rejs['gender'],
          'topics':rejs['topics']}],
        columns=['ID','title','content','excerpt','createdAt','updatedAt','forumName','forumAlias','gender','topics']))

# 嘗試使用撰寫出的函數，抓取編號231673959的文章
Crawl(231673959)

# 一次讀取100篇最熱門的文章
url = 'https://www.dcard.tw/_api/posts?popular=true&limit=100'
resq = requests.get(url)
rejs = resq.json()
df = pd.DataFrame()
for i in range(len(rejs)):
    df = df.append(Crawl(rejs[i]['id']),ignore_index=True)
print(df.shape)
df

