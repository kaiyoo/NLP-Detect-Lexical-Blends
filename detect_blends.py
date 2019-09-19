# -*- coding: utf-8 -*-
"""
Spyder Editor
author: Hongsang Yoo

"""
import os.path
from pyjarowinkler import distance
import time
import gensim.downloader as api

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

def process(processed):    
    
    if  not os.path.isfile(processed) :        
        with open(processed, 'w') as out, open('input/candidates.txt', 'r') as cands, open('input/dict.txt', 'r') as dicts, open('label/blends.txt', 'r') as blends:
            fdicts = dicts.readlines()
            cands = cands.readlines()
            blends = blends.readlines()
            #cand_arr = []
            filtered_arr = []
            dicts, reversedicts = makeDinctionary(fdicts)
            cnt = 0
            flag = False
            low_start = 0
            for can in cands:
                can= can.strip()
                alpha = can[0]
                reverseAlpha = can[-1]                  
                if flag:
                    flag = False
                flag = processflagging(can, flag)
                if not flag:     
                    idx_pref_start, low_param = search_startidx('p', dicts[alpha],can[:2], low_start)
                    low_start = idx_pref_start
                    idx_suf_start, low_param = search_startidx('p', reversedicts[reverseAlpha],can[-2:][::-1], 0)
                    
                    if idx_pref_start == -1 or idx_suf_start == -1:
                        cnt += 1
                        print(can)
                    else:                                            
                        filtered_arr.append(can)
                else:
                    continue
                
            for elem in filtered_arr:
                fmt = "{}\n".format(elem)
                out.write(fmt)
                #fmt = "{}\n".format(can)
                #out.write(fmt)
      
    return 0

def processflagging(can, flag):
    cons = 'bcdfghjklmnpqrtvwxz'
    tmpstr = ''
    accepted = ['ght','lyn', 's', 'y', 'ch' ]

    can = can.rstrip()
    if (len(can) > 15):
        flag=True
        return flag
    
    if (len(can)<= 2):                
        flag=True
        return flag

    if len(can) > 2:
        count1 =0
        count2 =0
        count3 =0

        if (can[0] in 'jkwyz' and can[0]== can[1]) or (can[-1] in 'vw' and can[-1]== can[-2]):
            flag=True
            return flag
            
        for i, c in enumerate(can):
            cond1 = i>0 and can[i - 1] == can[i]
            cond2 = i>1 and can[i - 2] == can[i]
            cond3 = c in cons
            if cond1 or cond2 or cond3:                             
                if cond1:     
                    count1+=1
                if cond2:                            
                    count2+=1
                if cond3:                             
                    tmpstr += c
                    count3 +=1
                if count1>1 or count2>1 or (count3>3 and tmpstr not in accepted and tmpstr[-2:]!='ch' ) :
                    flag = True
                    return flag
                    #break
            else:       
                count1 = 0
                count3 =0
                tmpstr = ''
                continue
        return flag

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

def get_preflist(wordvec, limiteddicts, pref_list, currCompPrefix):
    for src1 in limiteddicts:
        if src1 and src1.startswith(currCompPrefix):    
            prefixsim = distance.get_jaro_distance(currCompPrefix, src1,  winkler=True, scaling=0.07)
            if len(src1)<3 and prefixsim==1:
                continue
            if prefixsim>=0.75: #and prefixsim<=0.9:
                try:
                    #wordvec.similarity(src1, src1)
                    #pref_list[i]=[['',0]]
                    pref_list.append([src1,prefixsim])
                except:
                    1==1                       
    return pref_list

def get_candlist(wordvec, limiteddicts, pref_list, cand_list, currCompSuffix, suf_match_con, flag):

    for src2 in limiteddicts: 
        if src2 and src2.startswith(suf_match_con):  #currCompSuffix[:len(currCompSuffix)-1]

            
            suffixsim = distance.get_jaro_distance(currCompSuffix,src2,  winkler=True, scaling=0.08 )
            if len(src2)<3 and suffixsim==1:
                continue
            if suffixsim>=0.75 and len(pref_list)>0:
                try:
                    wordvec.similarity(src2[::-1], src2[::-1])
                except:
                    continue
                for pre in pref_list:
                    pre_word = pre[0]
                    pre_sim = pre[1]
                    try:
                        wordsim = wordvec.similarity(src2[::-1], pre_word)
                    except:
                        continue
                    #wordsim = 0.7
                    #except:
                    #    continue
                    if wordsim>0.2 and wordsim<1: 
                        if wordsim>cand_list[1][1]:
                            flag = True
                            cand_list[0]['prefix'][1] = pre_sim    #update prefix jw similarity     
                            cand_list[0]['prefix'][0] = pre_word   #update prefix str value
                            cand_list[0]['suffix'][1] = suffixsim    #update suffix jw similarity      
                            cand_list[0]['suffix'][0] = src2         #update suffix str value 
                            cand_list[1][0] = pre_sim+suffixsim      #update jw similarity sum
                            cand_list[1][1] = wordsim                #update word vector similarity
                            if wordsim>0.5:
                                return cand_list, flag

    return cand_list, flag
                
            
    
def model(cands, dicts, reversedicts):
    model_result = []
    load_start = time.time()
    # load gensim twitter word vectors        
    wordvec = api.load("glove-twitter-25")
    #wordvec = 0
    load_end = time.time() 
    print("loaded: ", load_end - load_start)
    detect_start = time.time()
    ## case1: prefix of the blendword: prefix of the source word1 && suffix of the blendword: suffix of the source word2 
    ## case2: prefix of the blendword: prefix of the source word1 && suffix of the blendword: prefix of the source word2
    ## ==> case2 was not considered in this ("jarowinkler+wordvector similarity model") to reduce processing time
    for z, can in enumerate(cands):
        flag = False
        #can = can.split()[0]
        can = can.strip()

        if len(can)==2:
            continue

        if z%100==0:
            progress = int(z/len(cands)*100)
            print(can," :", progress," %")    
        alpha = can[0]            
        reverseAlpha = can[-1]
        #prefixsim=0 ??
        #suffixsim=0 ??
        #preidx = 0 ??
        #sufidx=  0 ??
        iter_len = get_iterlen(len(can)) 
        cand_list=[None] * iter_len
        pref_list=[None]* iter_len
        low_pref_start = 0 
        high_suf_start = len(reversedicts[reverseAlpha])-1
        flag = False
        for i in range(iter_len): 
            preidx, sufidx = iter_condition(len(can),i)
            currCompPrefix = can[:preidx]
            currCompSuffix = can[sufidx:][::-1]
            idx_pref_end =-1
            idx_suf_end =-1
            #idx_end_suf2 = -1   #for case2 (not used here): i.e) botox
            ##for fast scan, set start index and end index to find in dictionary
            idx_pref_start, idx_pref_end, low, pre_mach_con  = get_index('p', dicts[alpha],currCompPrefix, low_pref_start)
            #low_pref_start = low
            idx_suf_start, idx_suf_end, high, suf_match_con = get_index('s', reversedicts[reverseAlpha],currCompSuffix,high_suf_start)
            if idx_pref_start == -1 or idx_pref_end == -1 or idx_suf_start == -1 or idx_suf_end == -1  :
                break
            #if idx_suf_end == 0:
            #    idx_suf_end = high_suf_start
            #high_suf_start = high + 1
            cand_list[i] = [{'prefix':['',0], 'suffix':['',0]},[0,0]]
            pref_list[i]=[]
            pref_list[i] = get_preflist(wordvec, dicts[alpha][idx_pref_start:idx_pref_end], pref_list[i], currCompPrefix)
            if len(pref_list[i])<1:
                continue
            
            cand_list[i], flag = get_candlist(wordvec, reversedicts[reverseAlpha][idx_suf_start:idx_suf_end], 
                                                 pref_list[i], cand_list[i], currCompSuffix, suf_match_con, flag)

        ##case2 code here was removed
        ######### cand_list data structure: list[0] = [dict (prefix1:[str,val],suf:[str,val]), sum]
        if flag:        
            #maxrow = max(cand_list, key=lambda x:(x[1][0]+x[1][1]))   # get the row with the highest word vector similarity
            maxrow = cand_list[i]
            prefstr = maxrow[0]['prefix'][0]
            suffstr = maxrow[0]['suffix'][0][::-1]
            preSim = maxrow[0]['prefix'][1]
            sufSim = maxrow[0]['suffix'][1]
            sum1 = maxrow[1][0]
            sum2 = maxrow[1][1]

            if prefstr and suffstr and (sum1>=1.3 ) :  #if it passes the threshold for jw similarity
                fmt = "{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(can, prefstr, suffstr, preSim, sufSim, sum1, sum2)
                model_result.append(fmt)
            #print("can: ", can, " pref idx: ", idx_pref_start, idx_pref_end, " suf idx: ", idx_suf_start, idx_suf_end, "preflist size: ", len(pref_list))
            #xx = 1
    
    detect_end = time.time() 
    print("finished : ", detect_end - detect_start)        
    return model_result
    
            
def get_index(flag, dic, compinfix, low_start):
     ##for fast scan, set start index and end index to find in dictionary
    idx_start, low_param = search_startidx(flag, dic,compinfix, low_start)
    low_start = idx_start #for next search(i+1), start searching from (low) the current index
    ##maybe +! to idx_end?
    idx_end, match_con = 0, ''
       
    #if len(compinfix)==4:   
    #    compinfix = compinfix[:-1]
    #elif len(compinfix)>4:
    #    compinfix = compinfix[:-2]
    
    if len(compinfix) != 1:                    # not (flag=='s' and low_start != len(dic)-1) 
        idx_end = search_endidx(dic, compinfix, low_param )

    return idx_start, idx_end, low_start, compinfix   

    #currCompSuffix2 = currCompSuffix[::-1]
    #suffixPreAlpha = currCompSuffix2[0]
    
    #idx_start_suf2, low_param3 = search_startidx(dicts[suffixPreAlpha],currCompSuffix2 )
    #if len(currCompSuffix2) != 1:   case2                 
    #    idx_end_suf2 = search_endidx(dicts[suffixPreAlpha],currCompSuffix2, low_param3 )
    
def detect_blends(outputfile):    
    
    with open(outputfile, 'w') as out, open('input/cands.txt', 'r') as cands, open('input/dict.txt', 'r') as dicts, open('label/blends.txt', 'r') as blends:
        fdicts = dicts.readlines()
        #cands = cands.readlines()
        cands = cands.readlines()
        dicts, reversedicts = makeDinctionary(fdicts)
        #prefixsim = 0#?
        #suffixsim = 0#?
        #wordsim=0#?  
        #model_arr = []
        model_result = model(cands, dicts, reversedicts)
        for result in model_result:
            out.write(result)
        #out.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(can, prefstr, suffstr, preSim, sufSim, sum1, sum2))
        
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


def search_startidx(flag, input, key, highlow):
   low = high = 0
   if flag =='p':
       low = highlow
       high = len(input)-1
   else:
       low = 0  
       high = highlow+1
       if len(key)==4:   
           key = key[:-1]
       elif len(key)>4:
           key = key[:int(len(key)/2)+1]        
   
   tmpLow = -1
   while low <= high:
      mid = int((low + high)/2)
     
      try:
          test = input[mid]
      except:
          print('error')
          return (-1,-1)
      if test >= key:    
      #if input[mid].startswith(key):          
         if mid ==0:
             tmpLow = tmpLow if input[tmpLow].startswith(key) else mid 
             return (mid, tmpLow)
         if tmpLow == -1:
             tmpLow = mid
         if input[mid] >= key and input[mid-1] < key:
             tmpLow = tmpLow if input[tmpLow].startswith(key) else mid 
             return (mid-1, tmpLow)
         else:              
             high = mid - 1    
      else:            
         low = mid + 1
   return (-1,-1)

def search_endidx(input, key, lowidx):
   low = lowidx
   high = len(input)-1

   while low <= high:
      mid = int((low + high)/2)
      midstr = input[mid]
      if (mid != len(input)-1):
          midplus1str =input[mid+1]
      
      if mid==len(input)-1:
          return mid
      if midstr>= key:
          if input[mid-1]<key or input[mid-1].startswith(key):  
             if mid ==0:
                 return mid
             if not midstr.startswith(key):
                 return mid
             else: 
                 low = mid + 1
          else:
              high = mid - 1
      else:
         low = mid + 1
         
   return -1   

def get_iterlen(length):
    iter_len = 1
    
    #if length<5: 
    #    iter_len = 1    
    #elif length<14: 
    #    iter_len = 2
    #else:
    #    iter_len = 3   
        
    return iter_len

def iter_condition(length, i):
    preidx = 0
    sufidx = 0
    #half = length  
    
    if length==3:
        preidx = 2
        sufidx = 1
    elif length==4:
        preidx = 1
        sufidx = 1
    elif length<7:
        preidx = 2 
        sufidx = int(length)-3
    elif length<11: 
        preidx = 3
        sufidx = int(length)-3
    elif length<13: 
        preidx = 3
        sufidx = int(length)-4
    elif length<14:         
        preidx = 3   
        sufidx = int(length)-5
    else:
        preidx = 5
        sufidx = int(length)-6 
        
    return preidx, sufidx

            
if __name__ == "__main__":    
    processed = 'input/cands.txt'      
    outputfile = 'output/fcands.txt'
    cands = 'output/fcands.txt'
    answer = 'label/blends.txt' 
    #process(processed) 
    detect_blends(outputfile)    
    evaluate(answer, cands)