# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 01:58:23 2019

@author: hongsangy
"""


def makeDinctionary(fdicts):
    dicts = {}        
    reversedicts = {}        
    ### in case of preventing key error
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for letter in alphabet:
        dicts[letter] = []
    for letter in alphabet:
        reversedicts[letter] = []    

    key = None
    reverseKey = None
    for line in fdicts:        

        line = line.strip()            
        key = line[0] 
        reverseKey = line[-1] 

        if not line:
            key = None
            reverseKey = None
        elif not key or not key in dicts:
            dicts[key] = []
        if not reverseKey or not reverseKey in reversedicts: 
            reversedicts[reverseKey] = []            
                
        dicts[key].append(line)   
        reversedicts[reverseKey].append(line[::-1])     

    for key in dicts:
        dicts[key].sort()
    
    for key in reversedicts:
        reversedicts[key].sort()

    return dicts, reversedicts

def jarowinkler(can,dic):
  
    s= ''
    l= ''
    m = 0
    pf=0
    trans=0
    simw=0
    winsize = 0
        
    if len(can)>len(dic):
        s = dic
        l =can 
    else:
        s = can
        l =dic

    winsize= int(max((len(l)/2)-1, 0))
    for i, word in enumerate(s):                
        if s[i] == l[i]:
            m+=1
            if i<4:
                pf+=1
                
        start = max(i-winsize, 0)
        end = min(i+winsize, len(l))
        for j in range(start, end):
            if(i==j and s[i] == l[i]):
                continue                        
            if s[i] == l[j]:
                trans+=1;
                break;
               
    if(m!=0):
        trans = trans/2
        simj = 1/3 * (m/len(l) + m/len(s) + (m-trans)/m)
        simw = simj + pf*0.1*(1- simj)

    return simw

