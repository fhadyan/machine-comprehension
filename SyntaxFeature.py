import re
import csv
from ConvertData import convert

def sf(question):
    


qfpath = "data/train/mc500.train.tsv"
afpath = "data/train/mc500.train.ans"

question,answer = convert(qfpath,afpath)
