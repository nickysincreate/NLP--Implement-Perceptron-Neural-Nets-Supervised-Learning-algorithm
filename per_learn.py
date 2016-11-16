import sys
import os
import re
import math
import random

#print("wats up nicky")
wordWeight={}
comdict={}

def getFileList(rootDir):
    comdict1={}
    wordWeight1={}
    fileName = []
    for root, dirs, files in os.walk(rootDir):
        for fn in files:
            if fn.endswith((".txt")):
                fnl=os.path.join(root,fn)
                words = open(fnl, "r", encoding="latin1").read()
                wordfreq = {}
                for word in words.split():
                    if word not in wordfreq:
                        wordfreq[word]=1
                    else:
                        wordfreq[word]=wordfreq.get(word)+1
                comdict1[fnl]=wordfreq
                for word in words.split():
                    if word not in wordWeight1:
                        wordWeight1[word]=0
    return (wordWeight1,comdict1)


#common calls
out=open("per_model.txt", "w", encoding="latin1")
fileName = sys.argv[1]
wordWeight,comdict=getFileList(fileName)

bias = 0
maxiter=20
for i in range(maxiter):
    folderName = "spam"
    shuffledItem=comdict.items()
    #random.shuffle(shuffledItem)
    #random.shuffle(list(comdict.keys()))
    random.shuffle(list(shuffledItem))
    for fname, fdetail in shuffledItem:
        addme = 0
        activation = 0
        r = fname.split('/')
        if (r[len(r) - 2] == folderName):
            y = 1
            for fword,fcount in fdetail.items():
                weight= wordWeight.get(fword)
                addme= addme + (weight*fcount)
            activation=addme + bias
            alpha= activation*y
            if (alpha <= 0):
                bias = bias + y
                for fword, fcount in fdetail.items():
                    wordWeight[fword]= wordWeight.get(fword) + (fcount*y)

        else:
            y = -1
            for fword,fcount in fdetail.items():
                weight= wordWeight.get(fword)
                addme= addme + (weight*fcount)
            activation=addme + bias
            alpha= activation*y
            if (alpha <= 0):
                bias= bias+y
                for fword, fcount in fdetail.items():
                    wordWeight[fword] = wordWeight.get(fword) + (fcount * y)

def createModelFile(bias,wordWeight):
    out.write("BiasN" + " " + str(bias) + "\n")
    for key, elem in wordWeight.items():
        out.write(key + " " + str(elem) + "\n")


createModelFile(bias,wordWeight)
