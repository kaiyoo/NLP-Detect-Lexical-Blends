# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 01:54:08 2019

@author: anonymous
"""
import process
import detect
import evaluate

if __name__ == "__main__":    
    processed = 'input/cands.txt'      
    outputfile = 'output/fcands.txt'
    cands = 'output/fcands.txt'
    answer = 'label/blends.txt' 
    process.process(processed) 
    detect.detect_blends(outputfile)    
    evaluate.evaluate(answer, cands)