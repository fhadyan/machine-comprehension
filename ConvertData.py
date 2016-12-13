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

qfpath = "data/train/mc500.train.tsv"
afpath = "data/train/mc500.train.ans"

question,answer=convert(qfpath,afpath)
print(question)