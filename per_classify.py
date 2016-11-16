import sys
import os
import re
import math


wordWeight={}
bias=[]

#fil = open('per_model.txt', "r", encoding="latin1").read()
#print(fil)


def mainDict(rootDir):
    comdict1={}
    for root, dirs, files in os.walk(rootDir):
        for fn in files:
            if fn.endswith((".txt")):
                fnl = os.path.join(root, fn)
                words = open(fnl, "r", encoding="latin1").read()
                wordfreq = {}
                for word in words.split():
                    if word not in wordfreq:
                        wordfreq[word] = 1
                    else:
                        wordfreq[word] = wordfreq.get(word) + 1
                comdict1[fnl] = wordfreq
    #print(comdict1)
    return comdict1

def fianlValueCheck(wordWeight,comdict):
    for fname, fdetail in comdict.items():
        addme = 0
        activation = 0
        for fword, fcount in fdetail.items():
            if fword in wordWeight:
            	weight = wordWeight.get(fword)
            	addme = addme + (weight * fcount)
        activation = addme + bias
        if (activation > 0):
            out.write("spam" + " " +fname + "\n")
        else:
            out.write("ham" + " " +fname + "\n")

#main calls for program execution


with open('per_model.txt' ,"r",encoding="latin1") as fil:
    for f in fil:
        if "BiasN" in f:
            val = f.strip().split(' ')
            bias=float(val[1])
        else:
            val2=f.strip().split(' ')
            wordWeight[val2[0]] = (float)(val2[1])
                    
fileName = sys.argv[1]
#out=open("output.txt", "w", encoding="latin1")
outputFile = sys.argv[2]
out=open(outputFile, "w", encoding="latin1")
comdict=mainDict(fileName)
fianlValueCheck(wordWeight,comdict)
