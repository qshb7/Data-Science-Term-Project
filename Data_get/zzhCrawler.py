# time   2021.1
# author zzh
import requests
from bs4 import BeautifulSoup
import json
import re
import time
import pandas as pd
import csv
#设置请求头
header = {
            "cookie": "_T_WM=59961081357; SCF=Ag-Uv5ha-Z4yrVbTXlN1dZpN0oqFTo6I3ZADk-LqeZWGSGRhZ58S6F8fYd-_WPBOqt8TFy6aSCieLQ76h487t7Y.; SUB=_2A25ND7_sDeRhGedN6FoQ8SbEzz6IHXVu88GkrDV6PUNbktAfLUbekW1NWtYvXJjgL02NRaLyik3-IoK4kj5lli21; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W52Qo65qLkjDbkx0lil5.6O5JpX5KMhUgL.Fo20e0npeKnRShz2dJLoIpqLxK-L1hqLBo5LxKnL1KeL1-xodcxL; ALF=1613978812",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
        }
#向每一页的首页发送请求
url_model='https://weibo.cn/1699432410/profile?keyword=%E7%96%AB&hasori=0&haspic=0&starttime=20191228&endtime=20200220&advancedfilter=1&page={}'
path_name="xhgd4.txt"#写入地址
with open('xhgd4.csv','a',encoding='utf-8') as csvfile:
     #设置表头
    csvdata1 = [("url", "ID", "nickname", "comment", "like", "time")]
    csvdata2 = pd.DataFrame(csvdata1)
    csvdata2.to_csv('xhgd4.csv', header=False, index=False, mode='a+')
for i in range(24):#主函数：确定要爬多少页
    #第一步，获取每页的url和html文件
    url=url_model.format(i+1)#每页的url
    response = requests.get(url, headers=header)#向该页发送请求，得到html文件
    response.encoding = 'utf-8'#utf-8格式解码
    soup = BeautifulSoup(response.text, features="lxml")#调用bs处理
    # 第二步，根据第一步得到的html文件获取次级页面所需url
    tags = re.findall('M_[a-zA-Z0-9]+', response.text)#找到变量
    hot_url = []  #热评url界面
    for tag in tags:
        tag = tag.replace("M_", '')
        base_url = 'https://weibo.cn/comment/hot/{}?rl=2'
        url = base_url.format(tag)#拼接变量和热评url模板
        hot_url.append(url)#保存所有热评的url
    for everyurl in hot_url:
        response2 = requests.get(everyurl, headers=header)#对热评的url发送访问请求
        response2.encoding = 'utf-8'#utf-8格式解码
        # 现在我们已经获得了一个html文件,需要解析获取的评论页面
        soup = BeautifulSoup(response2.text, 'lxml')#将文件传入bs中
        tags2 = soup.find_all('div', class_='c', id=re.compile(r'C_.+'))#找到所有评论所在区域
        commentlist = []
        # 获取所有评论的信息
        for tag in tags2:
            item = {}
            item["url"]=everyurl#来自网页
            item["ID"] = re.sub(r'.*/', '', tag.a['href'])#获取ID
            item["nickname"] = tag.a.text#获取用户名
            item["comment"] = tag.find_all('span', 'ctt')[0].text#获取评论内容
            item["like"] = tag.find_all('span', 'cc')[0].text.replace("赞[", "").replace("]", "")#获取点赞数
            item["time"] = tag.find_all('span', 'ct')[0].text.replace(" 来自网页","")  # 获取时间
            commentlist.append(item)#加入列表中
            csvdata1=[(item["url"],item["ID"],item["nickname"],item["comment"],item["like"],item["time"])]
            csvdata2=pd.DataFrame(csvdata1)
            csvdata2.to_csv('xhgd4.csv',header=False,index=False,mode='a+')
        for comment in commentlist:
            with open(path_name, "a", encoding="UTF-8") as f:
                f.write(json.dumps(comment, ensure_ascii=False, indent=2))
                f.write("\n")
        print("我好了")
        time.sleep(1)
        #一条微博处理完毕
print("芜湖起飞")