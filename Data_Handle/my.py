# -*- coding: utf-8 -*-
import jieba
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
txt = open("time4.csv", "r").read()
words = jieba.lcut(txt)     # 使用精确模式对文本进行分词
counts = {}     # 通过键值对的形式存储词语及其出现的次数
ii=0            #评论中所有的次数
jj = sum(1 for line in open("time4.csv", "r")) #所有的评论数
for word in words:
    if (u'\u4e00' <= word <= u'\u9fff'):
        if len(word) == 1: # 单个词语不计算在内
            ii=ii+1
            continue
        else:
            ii=ii+1
            counts[word] = counts.get(word, 0) + 1    # 遍历所有词语，每出现一次其对应的值加 1

items = list(counts.items())
items.sort(key=lambda x: x[1], reverse=True)    # 根据词语出现的次数进行从大到小排序

for i in range(20):
    word, count = items[i]
    print("{0:<5}{1:>5}    {2:<5}     {3}".format(word, count,count/ii,math.log(jj/count+1)))
    filename = 'time4.txt'
    with open(filename, 'a',encoding="UTF-8") as file_object:
        file_object.write("{0:<5}{1:>5}    {2:<5}     {3}\n".format(word, count,count/ii,math.log(jj/count+1)))



