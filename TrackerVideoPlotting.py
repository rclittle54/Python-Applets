#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 14:02:46 2018

Tracker VideoAnalysis Plotting

@author: ryanlittle
"""

import numpy as np
import matplotlib.pyplot as plt

#testfname = '/Users/ryanlittle/Desktop/181024J2_181029_Trial1_Corrected.txt'


def Get_TX(fname):
    try:
        f = open(fname)
        rawest_data = [line for line in f]
        f.close()
    except IOError:
        print("ERROR: Invalid filename %s"%(fname))
        print("Closing.")
        return
    
    
    raw_data = rawest_data[2:]
    data_strings = [x.split('\t') for x in raw_data]
    data_split = []
    for d in data_strings:
        temp_d = []
        for num in d:
            temp_d.append(num.split('E'))
        data_split.append(temp_d)
        
    data_floats = []
    for d in data_split:
        temp_d = []
        for num in d:
            a = float(num[0])
            b = float(num[1])
            temp_d.append(a*10**b)
        data_floats.append(temp_d)
        
        
    T = [x[0] for x in data_floats]
    X = [x[1] for x in data_floats]
    
    return T,X



def PrintVoltageLengths(times,voltages,T,X):
    if len(times) != len(voltages):
        print("ERROR: Mismatch between number of times and number of voltages.")
        return
    
    lengths = []
    for time in times:
        #print(time)
        use_xs = []
        for t in T:
            if np.floor(t) == time:
                use_xs.append(X[T.index(t)])
                
        lengths.append(np.mean(use_xs))
    #print(lengths)
    print("%10s|%10s|%10s"%("Time (s)","Volts (kV)","Length (mm)"))
    print("%s|%s|%s"%(10*'-',10*'-',10*'-'))
    for i in range(len(times)):
        print("%10.0f|%10.1f|%10.2f"%(times[i],voltages[i],1000*lengths[i]))
        
    return lengths
        
    
def GetYesOrNo(prompt):
    resp = str(input(prompt))
    while resp not in ['y','n']:
        print(">>> ERROR: Invalid response.")
        resp = str(input(prompt))
        
    return resp


def ProcessLoop():
    
    #times = [14,29,44,59,74,89]
    #volts = [0.5,1,1.5,2,2.5,3]
    
    
    # Getting a good filepath
    goodpath = 'n'
    print("Enter the filepath. Ex: /Users/ryanlittle/Desktop/")
    while goodpath == 'n':
        fp = input("Path: ")
        goodpath = GetYesOrNo("Is this correct? y/n: ")
      
        
    
    # Getting good filenames
    GoodFname = 'n'
    while GoodFname == 'n':
        fnames = []
        inname = ''
        counter = 1
        print("Enter the individual filenames. Enter 'x' when done.")
        while inname != 'x':
            inname = input("Filename #%d: "%(counter))
            if inname == 'x':
                break
            else:
                try:
                    f = open(fp+inname,'r')
                    f.close()
                    fnames.append(fp+inname)
                    counter += 1
                except IOError:
                    print("ERROR: Invalid filename.")
        print(fnames)
        GoodFname = GetYesOrNo("Is this a good list of filenames? y/n: ")
                
        
    
    # Getting good voltages
    GoodVolts = 'n'
    while GoodVolts == 'n':
        volts = []
        involt = 0
        counter = 1
        print("Enter the voltage levels of this experiment.\nEnter 'x' to quit.")
        while involt != 'x':
            involt = input("Voltage #%d: "%(counter))
            if involt == 'x':
                break
            else:
                try:
                    involt = float(involt)
                    volts.append(involt)
                    counter += 1
                except ValueError:
                    print("ERROR: Invalid value.")
        print(volts)
        GoodVolts = GetYesOrNo("Is this a good list of voltages? y/n: ")
        
    
    
    # Getting good times
    GoodTimes = 'n'
    while GoodTimes == 'n':
        times = []
        intime = 0
        counter = 1
        print("Enter the timestamps you want to evaluate those voltages at.\nEnter 'x' to quit.")
        while intime != 'x':
            intime = input("Time #%d: "%(counter))
            if intime == 'x':
                break
            else:
                try:
                    intime = float(intime)
                    times.append(intime)
                    counter += 1
                except ValueError:
                    print("ERROR: Invalid value.")
        print(times)
        GoodTimes = GetYesOrNo("Is this a good list of times? y/n: ")
        
    
    # Prints and plots the output
    print("\n\n\n%s Output %s"%(20*'=',20*'='))
    for f in fnames:
        T,X = Get_TX(f)
        plt.figure(1)
        plt.plot(T,X)
        #plt.show()
        
        print("\n%s"%(f))
        lengths = PrintVoltageLengths(times,volts,T,X)
        plt.figure(2)
        plt.plot(lengths,volts,'^-')
        
        
        
    
    # Formats the output plots
    leg = ["Series %d"%(i+1) for i in range(len(times))]
    
    plt.figure(1)
    plt.title("Video Analysis")
    plt.xlabel("Time (s)")
    plt.ylabel("Length (m)")
    plt.grid()
    plt.legend(leg)
    
    plt.figure(2)
    plt.title("Length vs Voltage")
    plt.ylabel("Voltage (kV)")
    plt.xlabel("Length (m)")
    plt.grid()
    plt.legend(leg)
    
    plt.show()
        
    # Waits for the user to continue
    #docontinue = input("Press enter to continue: ")
    
    return








def main():
    DO_CONTINUE = 'y'
    while DO_CONTINUE == 'y':
        ProcessLoop()
        DO_CONTINUE = GetYesOrNo("Run again? y/n: ")
    return




if __name__ == '__main__':
    main()

















