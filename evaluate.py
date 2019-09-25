# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 01:55:59 2019

@author: anonymous
"""

def evaluate(fanswer, fcands):
    with open(fanswer, 'r') as fanswer, open('input/cands.txt', 'r') as fdata, open(fcands, 'r') as fcands:
        fanswer = fanswer.readlines()
        fcands = fcands.readlines()
        fdata = fdata.readlines()
        label=[]
        dataList=[]
        candList = []

        for answer in fanswer:                                        
            label.append(answer.split()[0].strip())
            
        for d in fdata:       
            dataList.append(d.strip())
            
        tp=fp=tn=fn=0
        
        for cand in fcands:
            blend_cand = cand.split()[0].strip()
            candList.append(blend_cand)
            if blend_cand in label:
                tp += 1
            else:
                fp += 1
        
        for data in dataList:
            if data not in label and data not in candList:
                tn += 1
            elif data in label and data not in candList:
                fn += 1

        accuracy = (tp+tn)/(tp+fp+fn+tn)        
        precision= tp/len(candList)
        recall= tp/len(label)               

        print("accuracy\t{} ({}/{})".format(accuracy, tp+tn, tp+fp+fn+tn))
        print("precision\t{} ({}/{})".format(precision, tp, len(candList)))
        print("recall\t{} ({}/{})".format(recall, tp, len(label)))
    return 0
