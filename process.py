# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 01:54:39 2019

@author: hongsangy
"""
import utils
import search
import os

def process(processed):    
    if  not os.path.isfile(processed) :        
        with open(processed, 'w') as out, open('input/candidates.txt', 'r') as cands, open('input/dict.txt', 'r') as dicts, open('label/blends.txt', 'r') as blends:
            fdicts = dicts.readlines()
            cands = cands.readlines()
            blends = blends.readlines()
            #cand_arr = []
            filtered_arr = []
            dicts, reversedicts = utils.makeDinctionary(fdicts)
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
                    idx_pref_start, low_param = search.search_startidx('p', dicts[alpha],can[:2], low_start)
                    low_start = idx_pref_start
                    idx_suf_start, low_param = search.search_startidx('p', reversedicts[reverseAlpha],can[-2:][::-1], 0)
                    
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