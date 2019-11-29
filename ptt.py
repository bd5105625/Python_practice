import requests
from bs4 import BeautifulSoup
import numpy as np
import urllib3

# class ptt():
# url = "https://www.ptt.cc/bbs/"
# board = "beauty"
# url = url + board + "/index.html"
# article_url = []
# article_push = []   #推文數(包含爆)

def get_all_href(url ,):
    payload = {
        # 'from' : url , 
        'yes' : 'yes'
    }
    rs = requests.session()
    r = rs.post('https://www.ptt.cc/ask/over18' , verify = False , data=payload)
    r = rs.get(url , verify = False)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.select("div.nrec")
    for item in results:
        num = item.text
        if num == "爆":
            article_push.append(100)
        elif num == '':
            article_push.append(0)
        elif num == 'X1' or num == 'X2' or num == 'X3' or num == 'X4' or num == 'X5' or num == 'X6' or num == 'X7' or num == 'X8' or num == 'X9' or num == 'XX':
            article_push.append(-1)
        elif num:
            article_push.append(int(num))
    results = soup.select("div.title")
    for item in results:
        a_item = item.select_one("a")
        if a_item:  #確認該文章未被刪除
            href = 'https://www.ptt.cc'+ a_item.get('href')
            article_url.append(href)
        else:
            article_push.pop(len(article_url) - len(article_push))  #若該連結失效(文章被刪除) 把該文的推文數也pop

############################start here############################
url = "https://www.ptt.cc/bbs/"
board = "beauty"
url = url + board + "/index.html"
article_url = []
article_push = []   #推文數(包含爆)
urllib3.disable_warnings()
# logging.captureWarnings(True)
get_all_href(url)

# print(url)
# print(article_url)
# print(article_push)
temp = article_push
article_push = []
for i in range(0 , 12):
    article_push.append(temp[i])


temp = article_url
article_url = []
for i in range(0 , 12):
    article_url.append(temp[i])
# print(article_url)

for page in range(1,2):
    payload = {
        'from' : url , 
        'yes' : 'yes'
    }
    rs = requests.session()
    r = rs.post('https://www.ptt.cc/ask/over18' , verify = False , data=payload)
    r = rs.get(url , verify = False)
    soup = BeautifulSoup(r.text,"html.parser")
    btn = soup.select('div.btn-group > a')
    up_page_href = btn[3]['href']
    next_page_url = 'https://www.ptt.cc' + up_page_href
    url = next_page_url
    get_all_href(url = url)

max = 0
temp = []

for i in range(0 , len(article_push)):
    temp.append(article_push[i])
print(temp)
article_push_list = []
for i in range(0 , 5):  #二維list 共五組 每組第一個為推文數 第二個為index位子(即第幾篇文章的index)
    article_push_list.append([])    
for j in range(0 , 5):
    max = 0
    for i in range(0 , len(article_push)):
        num = article_push[i]
        if num > max:
            max = num
            index = i
    article_push[index] = 0
    article_push_list[j].append(max)
    article_push_list[j].append(index)


article_push = temp     #取回原本的push


print(len(article_push))
print(article_push_list)
# print(article_url[article_push_list[0][1]])
# print(article_url[article_push_list[1][1]])
# print(article_url[article_push_list[2][1]])
# print(article_url[article_push_list[3][1]])
# print(article_url[article_push_list[4][1]])

# print(len(article_push_list))
article_hot_url = []    #存取前幾熱門的文章網址
for i in range(0 , 5):
    article_hot_url.append(article_url[article_push_list[i][1]])
    print(article_url[article_push_list[i][1]])