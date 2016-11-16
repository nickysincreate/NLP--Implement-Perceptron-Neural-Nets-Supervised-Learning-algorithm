import sys
import os
import re
import math
import random

wordWeight={}
comdict={}
avgWeight={}

def getFileList(rootDir):
    comdict1 = {}
    wordWeight1 = {}
    avgWeight1={}
    fileName = []
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
                for word in words.split():
                    if word not in wordWeight1:
                        wordWeight1[word] = 0
                    if word not in avgWeight1:
                        avgWeight1[word]=0
    return (wordWeight1, avgWeight1, comdict1)

#common calls
out=open("per_model.txt", "w", encoding="latin1")
fileName = sys.argv[1]
wordWeight,avgWeight,comdict=getFileList(fileName)


bias = 0
avgbias=0
counter=1
maxiter=30
for i in range(maxiter):
    folderName = "spam"
    shuffledItem = comdict.items()
    #random.shuffle(list(comdict.keys()))
    random.shuffle(list(shuffledItem))
    for fname, fdetail in shuffledItem:
        addme = 0
        activation = 0
        r = fname.split('/')
        if (r[len(r) - 2] == folderName):
            y = 1
            counter = counter + 1
            #print(counter)
            for fword, fcount in fdetail.items():
                weight = wordWeight.get(fword)
                addme = addme + (weight * fcount)
            activation = addme + bias
            alpha = activation * y
            if (alpha <= 0):
                bias = bias + y
                avgbias=avgbias + (y*counter)
                for fword, fcount in fdetail.items():
                    wordWeight[fword]= wordWeight.get(fword) + (fcount*y)
                    avgWeight[fword]=avgWeight.get(fword) + ((y*fcount)*counter)

        else:
            y = -1
            counter = counter + 1
            #print(counter)
            for fword, fcount in fdetail.items():
                weight = wordWeight.get(fword)
                addme = addme + (weight * fcount)
            activation = addme + bias
            alpha = activation * y
            if (alpha <= 0):
                bias = bias + y
                avgbias=avgbias + (y*counter)
                for fword, fcount in fdetail.items():
                    wordWeight[fword]= wordWeight.get(fword) + (fcount*y)
                    avgWeight[fword]=avgWeight.get(fword) + ((y*fcount)*counter)

def getFavgWeight(wordWeight,avgWeight,bias,avgbias,counter):
    #print(wordWeight)
    #print(bias)
    #print(avgWeight)
    #print(avgbias)
    #print(counter)
    avgbias= bias - ((1/counter) * avgbias)
    for fname, fdetail in comdict.items():
        for fword, fcount in fdetail.items():
            avgWeight[fword]=wordWeight.get(fword) - ((1/counter)* avgWeight.get(fword))
    return (avgbias,avgWeight)


def createModelFile(bias,avgWeight):
    out.write("BiasN" + " " + str(bias) + "\n")
    for key, elem in avgWeight.items():
        out.write(key + " " + str(elem) + "\n")


finalbias,finalWeight=getFavgWeight(wordWeight,avgWeight,bias,avgbias,counter)
createModelFile(finalbias,finalWeight)
