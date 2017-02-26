from ConvertData import convert
from nltk.corpus import stopwords
from ConvertData import toMatrix
from SyntaxFeature import generateStatement
from SyntaxFeature import syntaxFeature
from SyntaxFeature import first
from pycorenlp import StanfordCoreNLP
import re
import numpy as np
from corenlp_pywrap import pywrap
from gensim.models import Word2Vec
import scipy.spatial.distance as dist
from WordEmbedding import wordEmbed
from DistanceFeature import distanceFeature
import math
from SlidingWindows import toString
from SlidingWindows import story
from SlidingWindows import calculate
import neurolab as nl
import scipy
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

def learn(inp,tar, col):
    mint = np.amin(inp, axis=0)
    maxt = np.amax(inp, axis=0)
    maxmin = [[x, maxt[i]] for i,x in enumerate(mint[:-1])]
    net = nl.net.newff(maxmin, [12, 1])
    err = net.train(inp[:,0:col], tar, show=100, goal=0.002)
    return net

def testing(model, dat,text, test=[], label=[]):
    if test==[]:
        test = [[x[5],x[6],x[7],x[8]] for x in dat]
    res = model.sim(test)
    maxans=[]
    temp=[]
    for i,x in enumerate(res):
        temp.append(x[0])
        if((i+1)%4==0):
            maxans.append(temp.index(max(temp)))
            temp=[]
    pred=[]
    for x in maxans:
        temp=[0,0,0,0]
        temp[x]=1
        pred.extend(temp)
    if label==[]:
        testlabel = [int(x[4]) for x in dat]    
    else:
        testlabel = label
    result= confusion_matrix(testlabel, pred)
    acc = (result[0,0]+result[1,1])/result.sum()
    report = classification_report(testlabel, pred).split()

    print("\n"+text)
    print("accuracy : " + str(acc*100) + "%")
    f=float(report[11])*100
    print("f1 : " + str(f) + "%")
    
def extract(qpath, apath):
    nlp = StanfordCoreNLP('http://localhost:9000')
    question,answer = convert(qpath,apath)
    dat = toMatrix(question,answer)
    
    # Syntax Feature
    statement = generateStatement(dat,nlp)
    f = syntaxFeature(statement , dat)
    # Word Embedding
    we = wordEmbed(dat)
    # Distance Feature
    df = distanceFeature(question)
    # Sliding WIndow
    swData=toString(question)
    swStory=story(question)
    sw = calculate(swData,swStory)
    
    f=np.column_stack((f,we))
    f=np.column_stack((f,df))
    f=np.column_stack((f,sw))
    return f
    
        
qfpath = "data/train/mc500.train.tsv"
afpath = "data/train/mc500.train.ans"
nlp = StanfordCoreNLP('http://localhost:9000')

### extract train feature
tquestion,tanswer = convert(qfpath,afpath)
traind = toMatrix(tquestion,tanswer)

# Syntax Feature
dataStatement = generateStatement(traind,nlp)
trainf = syntaxFeature(dataStatement, traind)
# Word Embedding
we = wordEmbed(traind)
# Distance Feature
df = distanceFeature(tquestion)
# Sliding WIndow
swData=toString(tquestion)
swStory=story(tquestion)
sw = calculate(swData,swStory)

trainf=np.column_stack((trainf,we))
trainf=np.column_stack((trainf,df))
trainf=np.column_stack((trainf,sw))


### extract def feature
dqfpath = "data/dev/mc500.dev.tsv"
dafpath = "data/dev/mc500.dev.ans"
dquestion,danswer = convert(dqfpath,dafpath)
devd = toMatrix(dquestion,tanswer)

# Syntax Feature
dataStatement = generateStatement(devd,nlp)
devf = syntaxFeature(dataStatement, devd)
# Word Embedding
we = wordEmbed(devd)
# Distance Feature
df = distanceFeature(dquestion)
# Sliding WIndow
swData=toString(dquestion)
swStory=story(dquestion)
sw = calculate(swData,swStory)

devf=np.column_stack((devf,we))
devf=np.column_stack((devf,df))
devf=np.column_stack((devf,sw))

### extract test feature
tqfpath = "data/test/mc500.test.tsv"
tafpath = "data/test/mc500.test.ans"
testf = extract(tqfpath,tafpath)

### learning main
train = trainf #####
train = [[x[5],x[6],x[7],x[8],x[4]] for x in train]
target = [[x[4]] for x in train]
target = np.array(target,dtype='int32')
train = np.array(train,dtype='f')
model = learn(train,target,4)

### learning baseline
train = trainf #####
train = [[x[7],x[8],x[4]]for x in train]
target = [[x[4]] for x in trainf]
target = np.array(target,dtype='int32')
train = np.array(train,dtype='f')
modelbase = learn(train,target,2)

### learning system base + sy
train = trainf #####
train = [[x[5],x[7],x[8],x[4]]for x in train]
target = [[x[4]] for x in trainf]
target = np.array(target,dtype='int32')
train = np.array(train,dtype='f')
model2 = learn(train,target,3)

### learning system base + we
train = trainf #####
train = [[x[6],x[7],x[8],x[4]]for x in train]
target = [[x[4]] for x in trainf]
target = np.array(target,dtype='int32')
train = np.array(train,dtype='f')
model3 = learn(train,target,3)

# test on main system
print("+ssy+wd system\n")
testing(model,trainf,"testing on train data")
testing(model,devf,"testing on dev data")
testing(model,testf,"testing on test data")

# test on baseline
print("baseline system\n")
test = [[x[7],x[8]] for x in trainf]
label = [int(x[4]) for x in trainf]
testing(modelbase,trainf,"testing on train data",test,label)
test = [[x[7],x[8]] for x in devf]
label = [int(x[4]) for x in devf]
testing(modelbase,devf,"testing on dev data",test,label)
test = [[x[7],x[8]] for x in testf]
label = [int(x[4]) for x in testf]
testing(modelbase,testf,"testing on test data",test,label)

# test on baseline+sy
print("baseline+sy system\n")
test = [[x[5],x[7],x[8]] for x in trainf]
label = [int(x[4]) for x in trainf]
testing(model2,trainf,"testing on train data",test,label)
test = [[x[5],x[7],x[8]] for x in devf]
label = [int(x[4]) for x in devf]
testing(model2,devf,"testing on dev data",test,label)
test = [[x[5],x[7],x[8]] for x in testf]
label = [int(x[4]) for x in testf]
testing(model2,testf,"testing on test data",test,label)

# test on baseline+we
print("baseline+we system\n")
test = [[x[6],x[7],x[8]] for x in trainf]
label = [int(x[4]) for x in trainf]
testing(model3,trainf,"testing on train data",test,label)
test = [[x[6],x[7],x[8]] for x in devf]
label = [int(x[4]) for x in devf]
testing(model3,devf,"testing on dev data",test,label)
test = [[x[6],x[7],x[8]] for x in testf]
label = [int(x[4]) for x in testf]
testing(model3,testf,"testing on test data",test,label)





