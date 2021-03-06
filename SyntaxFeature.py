import re
import csv
import json
from ConvertData import convert
from ConvertData import toMatrix
from pycorenlp import StanfordCoreNLP
from corenlp_pywrap import pywrap

def first(arr):
    if len(arr)>0:
        arr=arr[0]
    else:
        arr=''
    return arr
    
def tes():
    print('generated statement')

def syntaxFeature(statement,d):
    nlp = StanfordCoreNLP('http://localhost:9000')
    #statement = dataStatement #####
    for ids,s_ in enumerate(statement):
        #ids=0 #####
        #s_=statement[ids] #####
        s=s_[2]
        sy=0
        prop = {'annotators': 'tokenize,ssplit,pos,depparse,parse,relation,lemma','outputFormat': 'json'}
        #print(str(ids)+' - '+str(ids%16))
        print(ids)
        if ids%16==0:
            #print('ok')
            ss = d[ids][0].split('. ')
            ss = [re.sub(r'\.','',x) for x in ss]
            ssdeps = []
            for x in ss:        
                ssnlp = nlp.annotate(x, properties=prop)
                ssdepedencies = ssnlp['sentences'][0]['enhancedDependencies']
                ssdeps.append(ssdepedencies)
        snlp = nlp.annotate(s, properties=prop)
        sdepedencies = snlp['sentences'][0]['enhancedDependencies']
        sys=[]
        for ssdep in ssdeps:
            sy=0
            #ssdep=ssdeps[0]
            s1 = [x['dependentGloss'] +' '+ x['governorGloss'] +' '+ x['dep'] for idx,x in enumerate(ssdep[1:])]
            s2 = [x['dependentGloss'] +' '+ x['governorGloss'] +' '+ x['dep'] for idx,x in enumerate(sdepedencies [1:])]
            ins = list(set(s1) & set(s2))
            sy=len(ins)
            sys.append(sy)
        msy = max(sys)
        d[ids].append(msy)
    return d
    
            

def generateStatement(data,nlp):
    #nlp = StanfordCoreNLP('http://localhost:9000')
    d = [[x[2],x[3]] for x in data]
    for idq,q in enumerate(d):
        #idq=12 #####
        print(idq)
        #q=data[idq] #####
        if idq%4==0:
            qs = q[0].lower()
        #qs = 'Who is the president?'.lower() #####
        ans = q[1].lower()
        #ans = 'Obama is'.lower() #####
        
        c=re.findall(r'who|what|how|where|when|why',qs)
        c=first(c)
        prop = {'annotators': 'tokenize,ssplit,pos,depparse,parse,relation,lemma','outputFormat': 'json'}
        qnlp = nlp.annotate(qs, properties=prop)
        anlp = nlp.annotate(ans, properties=prop)
        qdepedencies = qnlp['sentences'][0]['enhancedDependencies']
        adepedencies = anlp['sentences'][0]['enhancedDependencies']

        rq = qdepedencies[0]['dependentGloss']
        rqTokens = [x for x in qnlp['sentences'][0]['tokens'] if x['originalText']==rq]
        rqTokens = first(rqTokens)
        rqlemma = rqTokens['lemma']
        rqPos = rqTokens['pos']
        arcRqC = [x['dep'] for x in qdepedencies if x['governorGloss']==rq and x['dependentGloss']==c]
        arcRqC = first(arcRqC)        

        ra = anlp['sentences'][0]['enhancedDependencies'][0]['dependentGloss']
        raTokens = [x for x in anlp['sentences'][0]['tokens'] if x['originalText']==ra]
        raTokens = first(raTokens)
        raPos = raTokens['pos']
        
        if c=='what' and rqPos=='VB' and rq=='do' and arcRqC=='dobj':
            uq = [x['dependentGloss'] for x in qdepedencies if x['dep']=='nsubj' and x['governorGloss']==rq]
            uq=first(uq)
            ua = ''
            if(raPos[0:2]=='VB'):
                ua = [x['dependentGloss'] for x in adepedencies if x['dep']=='nsubj' and x['governorGloss']==ra]
                ua=first(ua)
            ansOut = re.sub(ua, '', ans)
            qOut = ' '.join(qs.split(' ')[2:])
            qOut = re.sub(rq, '', qOut)
            qOut = re.sub(uq, uq+' '+ansOut, qOut)
            out = re.sub(r'[^a-zA-Z0-9\s]+','',qOut)
            out = re.sub(r'\s{2}',' ',out)
                
        elif c=='what' and rqPos=='VB' and rq!='do' and arcRqC=='dobj':
            ua=''
            if(raPos[0:2]=='VB'):
                ua = [x['dependentGloss'] for x in adepedencies if x['dep']=='nsubj' and x['governorGloss']==ra]
                ua=first(ua)
            ansOut = re.sub(ua, '', ans)
            qOut = ' '.join(qs.split(' ')[2:])
            qOut = re.sub(rq, rq+' '+ansOut, qOut)
            out = re.sub(r'[^a-zA-Z0-9\s\’\']+','',qOut)
            out = re.sub(r'\s{2}',' ',out)
            
        elif c=='what' and rqPos=='NN' and arcRqC=='nsubj':
            ua=''
            ansOut=ans
            if(raPos[0:2]=='VB'):
                ua = [x['dependentGloss'] for x in adepedencies if x['dep']=='nsubj' and x['governorGloss']==ra]
                ua=first(ua)
                ansOut=ua
            qOut = re.sub(c, ansOut, qs)
            out = re.sub(r'[^a-zA-Z0-9\s\’\']+','',qOut)
            out = re.sub(r'\s{2}',' ',out)
            
        elif c=='where' and rqPos=='VB' and arcRqC=='advmod':
            uq = [x['dependentGloss'] for x in qdepedencies if x['dep']=='dobj' and x['governorGloss']==rq]
            uq=first(uq)
            qOut = ' '.join(qs.split(' ')[2:])
            if uq!='':
                qOut = re.sub(uq, uq+' '+ans,qOut)
            else:
                qOut = re.sub(rq, rq+' '+ans,qOut)
            out = re.sub(r'[^a-zA-Z0-9\s\’\']+','',qOut)
            out = re.sub(r'\s{2}',' ',out)
        elif c=='where' and rqlemma=='be' and arcRqC=='advmod':
            uq=''
            uq = [x['dependentGloss'] for x in qdepedencies if x['dep']=='nsubj' and x['governorGloss']==rq]
            uq=first(uq)
            qOut = ' '.join(qs.split(' ')[2:])
            qOut = re.sub(uq, uq+' '+rq, qOut)
            qOut = qOut+' '+ans
            out = re.sub(r'[^a-zA-Z0-9\s\’\']+','',qOut)
            out = re.sub(r'\s{2}',' ',out)
        #elif c=='who' and rqPos=='NN' and arcRqC=='nsubj':
        elif c=='who':
            rqToken=[x for x in qnlp['sentences'][0]['tokens'] if x['pos'] == 'NN']
            rqToken=first(rqToken)
            if rqToken!='':
                rqPos=rqToken['pos']
                rq=rqToken['word']
            else:
                rqPos=''
                rq=''
            ua = [x['dependentGloss'] for x in adepedencies if x['dep']=='nsubj' and x['governorGloss']==ra]
            ua=first(ua)
            qOut = re.sub(c, ua, qs)
            out = re.sub(r'[^a-zA-Z0-9\s\’\']+','',qOut)
            out = re.sub(r'\s{2}',' ',out)      
        else:
            qOut = qs + ' ' + ans
            out = re.sub(r'[^a-zA-Z0-9\s\’\']+','',qOut)
            out = re.sub(r'\s{2}',' ',out)  
            
        d[idq].append(out)
    return d

#==============================================================================
# qfpath = "data/train/mc500.train.tsv"
# afpath = "data/train/mc500.train.ans"
# 
# question,answer = convert(qfpath,afpath)
# data = toMatrix(question,answer)
# nlp = StanfordCoreNLP('http://localhost:9000')
# dataStatement = generateStatement(data)
# sf=syntaxFeature(dataStatement, data)
#==============================================================================
