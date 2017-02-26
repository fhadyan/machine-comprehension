import re
import csv
from ConvertData import convert
import math

def toString(q):
    data = []
    for idx,x in enumerate(q):
        for idy,y in enumerate(x[1:5]):
            for idz,z in enumerate(y[1:5]):
                temp=[]
                temp.append(y[0].split(': ')[1] + " "+ z)
                data.append(temp)
    return data

def story(q):
    store=[]
    for idx,x in enumerate(q):
                temp=[]
                temp.append(x[0])
                store.append(temp)
    return store

def calculate(data,stors):
    datay=[]
    for idx,x in enumerate(data):
        #idx = 0 #####
        #x = data[0] #####
        #stors=stori #####
        k = len(re.findall("[a-zA-Z_]+", str(x)))
        data1 = str(x[0])
        test = re.sub(r"[^a-zA-Z0-9\s\']",' ',data1)
        data2 = test.split(' ')
        data2 = [y for y in data2 if len(y)>0]
        stors1 = re.sub(r"[^a-zA-Z0-9\s\']",' ',str(stors[math.floor(idx / 16)][0]))
        stors1 = stors1.split('.')
        stors1 = [y.split(' ') for y in stors1]
        stors2 = []
        for j in stors1:
            stors2.extend(j)
        stors2 = [y for y in stors2 if len(y)>0]
                  
        panjang = len(stors2)
        swmin=0
        datax=[]
        for i in range(panjang - k):
            temp = stors2[i:k]
            icws = 0
            for s in data2:
                temp1 = temp.count(s)
                if (temp1==0):
                    icw=0
                else :
                    icw = math.log10(1 + (1 / temp1))
                icws += icw
            datax.append(icws)
        swmin = max(datax)
        datay.append(swmin)
    return datay

#==============================================================================
# qfpath = "data/train/mc500.train.tsv"
# afpath = "data/train/mc500.train.ans"
# question,answer=convert(qfpath,afpath)
# data=toString(question)
# stori=story(question)
# test = calculate(data,stori)
# 
# for i in range(1,4800):
#     print(test[i])
#==============================================================================
