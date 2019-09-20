# -*- coding: utf-8 -*-
"""
Spyder Editor
author: Hongsang Yoo

"""
from pyjarowinkler import distance
import time
import gensim.downloader as api
import utils
import search

def detect_blends(outputfile):    
    
    with open(outputfile, 'w') as out, open('input/cands.txt', 'r') as cands, open('input/dict.txt', 'r') as dicts, open('label/blends.txt', 'r') as blends:
        fdicts = dicts.readlines()
        #cands = cands.readlines()
        cands = cands.readlines()
        dicts, reversedicts = utils.makeDinctionary(fdicts)
        #prefixsim = 0#?
        #suffixsim = 0#?
        #wordsim=0#?  
        #model_arr = []
        model_result = model(cands, dicts, reversedicts)
        for result in model_result:
            out.write(result)
        #out.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(can, prefstr, suffstr, preSim, sufSim, sum1, sum2))
        

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
        iter_len = search.get_iterlen(len(can)) 
        cand_list=[None] * iter_len
        pref_list=[None]* iter_len
        low_pref_start = 0 
        high_suf_start = len(reversedicts[reverseAlpha])-1
        flag = False
        for i in range(iter_len): 
            preidx, sufidx = search.iter_condition(len(can),i)
            currCompPrefix = can[:preidx]
            currCompSuffix = can[sufidx:][::-1]
            idx_pref_end =-1
            idx_suf_end =-1
            #idx_end_suf2 = -1   #for case2 (not used here): i.e) botox
            ##for fast scan, set start index and end index to find in dictionary
            idx_pref_start, idx_pref_end, low, pre_mach_con  = search.get_index('p', dicts[alpha],currCompPrefix, low_pref_start)
            #low_pref_start = low
            idx_suf_start, idx_suf_end, high, suf_match_con = search.get_index('s', reversedicts[reverseAlpha],currCompSuffix,high_suf_start)
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
    


def get_preflist(wordvec, limiteddicts, pref_list, currCompPrefix):
    for src1 in limiteddicts:
        if src1 and src1.startswith(currCompPrefix):    
            prefixsim = distance.get_jaro_distance(currCompPrefix, src1,  winkler=True, scaling=0.07)
            if len(src1)<3 and prefixsim==1:
                continue
            if prefixsim>=0.87: #and prefixsim<=0.9:
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
            suffixsim = distance.get_jaro_distance(currCompSuffix, src2,  winkler=True, scaling=0.08 )
            if len(src2)<3 and suffixsim==1:
                continue
            if suffixsim>=0.9 and len(pref_list)>0:
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
                    if wordsim>0.6 and wordsim<1: 
                        if wordsim>cand_list[1][1]:
                            flag = True
                            cand_list[0]['prefix'][1] = pre_sim    #update prefix jw similarity     
                            cand_list[0]['prefix'][0] = pre_word   #update prefix str value
                            cand_list[0]['suffix'][1] = suffixsim    #update suffix jw similarity      
                            cand_list[0]['suffix'][0] = src2         #update suffix str value 
                            cand_list[1][0] = pre_sim+suffixsim      #update jw similarity sum
                            cand_list[1][1] = wordsim                #update word vector similarity
                            return cand_list, flag

    return cand_list, flag
                




