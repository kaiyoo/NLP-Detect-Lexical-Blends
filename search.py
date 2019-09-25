# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 01:57:13 2019

@author: anonymous
"""

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
          #print('error')
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
        sufidx = int(length)-4  #3
    elif length<13: 
        preidx = 3
        sufidx = int(length)-5 #3
    elif length<14:         
        preidx = 4   #3
        sufidx = int(length)-5  #5
    else:
        preidx = 5
        sufidx = int(length)-6 
        
    return preidx, sufidx

            