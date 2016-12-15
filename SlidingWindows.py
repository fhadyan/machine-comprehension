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

def calculate(data,story):
    data1=[]
    data2=[]
    for idx,x in enumerate(data):
        store = story[math.floor(idx/16)]
        k = len(re.findall("[a-zA-Z_]+", str(x)))

        for i in range(len(store)-k):
            temp = store[i:k]
            icw=0
            for s in data:
                temp1 = temp.count(s)
                sw = math.log10(1+ (1/temp1))
                icw+=sw
            data1.append(icw)
        if (len(data1)==0):
            swmin=0
        else :
            swmin=min(data1)
        data2.append(swmin)
    return data2

qfpath = "data/train/mc500.train.tsv"
afpath = "data/train/mc500.train.ans"
question,answer=convert(qfpath,afpath)
data=toString(question)
story=story(question)
test=calculate(data,story)