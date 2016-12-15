import re
import csv
import json
import numpy as np
from ConvertData import convert
from ConvertData import toMatrix
from pycorenlp import StanfordCoreNLP
from corenlp_pywrap import pywrap
from gensim.models import Word2Vec
import scipy.spatial.distance as dist

def wordEmbed(dat):
    out=[]
    for idd,d in enumerate(dat):
        #idd=0#####
        #d=data[idd]######
        print(idd)
        s = d[2]+' '+d[3]
        s=re.sub(r'[^a-zA-Z0-9\s\']+','',s)
        s=s.split()
        if idd%16==0:
            text=re.sub(r'\.','*',d[0])
            text=re.sub(r'[^a-zA-Z0-9\s\'\*]+',' ',text)
            text=re.sub(r'\s{2}',' ',text)
            text=text.split('*')
            text=[re.sub(r'^\s+','',x) for x in text]
            text=[x.split() for x in text if len(x)>0]
            model=Word2Vec(text, min_count=min_count, size=size, window=window)
        
        wes=[]
        for idts,ts in enumerate(text):
            idts=0
            ts=text[idts]
            vws=[]
            for idt,t in enumerate(ts):
                if t in model.vocab.keys():
                    w=model[t]
                    vws.append(w)
            vws=np.array(vws)
            vw=np.sum(vws,axis=0)
            
            vas=[]
            for idt,t in enumerate(s):
                if t in model.vocab.keys():
                    w=model[t]
                    vas.append(w)
            vas=np.array(vas)
            va=np.sum(vas,axis=0)
            wes.append(dist.cosine(vw,va))
        we=max(wes)
        out.append(we)
    return out
        
            
        

qfpath = "data/train/mc500.train.tsv"
afpath = "data/train/mc500.train.ans"
min_count = 1
size = 100
window = 10

question,answer = convert(qfpath,afpath)
data = toMatrix(question,answer)
nlp = StanfordCoreNLP('http://localhost:9000')
out = wordEmbed(data)

