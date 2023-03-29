#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 11:00:30 2017

@author: ryanlittle

"""
import itertools
import time
from numpy import mean





def Run_Stress_Test(N):
    
    t_start = time.time()
    
    n_cols = 10
    
    n_items = N
    dts = []

    print(">>> Starting test with N = %d"%(N))
    
    for n in range(n_cols):
        
      
        
            
        t0 = time.time()
        stuff = range(n_items)
        combos = itertools.permutations(stuff)
        all_combos = []
        for i in combos:
            all_combos.append(i)
        tf = time.time()
        dt = tf-t0
        dts.append(dt)
        
        print(">>>\t%0.2f percent complete after %0.4f s"%((100*(n+1)/n_cols), tf-t_start))
        
    print(">>> Finished test with N = %d"%(N))
  
    
    outstring = "%d"%(N)
    for n in range(n_cols):
        outstring += "\t%f"%(dts[n])
    outstring += "\t%f"%(mean(dts))
    
    
    return outstring


max_arr_size = 10

print("Please enter file path + filename to write output file to.")
write_filename = str(input("Path + name: "))
f = open(write_filename,'w')
for n in range(max_arr_size):
    f.write(Run_Stress_Test(n+1))
    print('\n')
    f.write('\n')
f.close()
    
    
    











