import re
import csv

def convert(qfpath, afpath):
    qf = open(qfpath, 'r+', encoding="utf-8")
    qftext = csv.reader(qf, delimiter='\t')

    dataq=[]
    for line in qftext:
        temp=[]
        temp.append(line[2])
        for i in range(0,4):
            temp.append(line[3+(i*5):8+(i*5)])
        dataq.append(temp)

    af = open(afpath, 'r+', encoding="utf-8")
    aftext = csv.reader(af, delimiter='\t')
    dataa=[]
    for line in aftext:
        l=[ord(x)-64 for x in line]
        dataa.append(l)
    return dataq,dataa

def toMatrix(q, ans):
    data = []
    for idx,x in enumerate(q):
        for idy,y in enumerate(x[1:5]):
            for idz,z in enumerate(y[1:5]):
                temp=[]
                temp.append(x[0])
                temp.append(y[0].split(': ')[0])
                temp.append(y[0].split(': ')[1])
                temp.append(z)
                temp.append(0)
                data.append(temp)
        for ida,a in enumerate(ans[idx]):
            data[(a-1)+((ida*4)+(idx*16))][4]=1
    return data
    

qfpath = "data/train/mc500.train.tsv"
afpath = "data/train/mc500.train.ans"


question,answer=convert(qfpath,afpath)
data=toMatrix(question,answer)