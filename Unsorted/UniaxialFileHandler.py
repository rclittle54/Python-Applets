#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 23:25:56 2017


CSV File handler - Uniaxial Material Tests



Knock on wood:

Finished on Thu Oct 5 11:38:46 2017

@author: ryanlittle
"""


import matplotlib.pyplot as plt
import numpy as np
import math
from pathlib import Path
from os import listdir
import time

RUNMAIN = True



"""
    GetRawestData(fname): Gets the unaltered raw data out of fname.csv
"""
def GetRawestData(fname):
    DEBUG = False
    if DEBUG: print("=== INSIDE GetRawestData ===")
    rd = []
    f = open(fname,'r')
    i = 0
    for line in f:
        rd.append(line)
        if DEBUG:
           i += 1
           if i <= 20:
               print(line)
    f.close()
    return rd
"""
==============================================================================
"""

"""
    GetIntInput(prompt): Validates user input of an integer.
"""
def GetIntInput(prompt):
    isvalid = False
    while not isvalid:
        r = input(prompt)
        isvalid = True
        for i in r:
            if ord(i) not in range(48,58):
                isvalid = False
                
        if not isvalid:
            print(">>> ERROR: Invalid value.")
    return int(r)
"""
==============================================================================
"""

"""
    GetSIs(rd,data): Gets the strain stress indices out of raw data, by user
    input on what to plot on the x-axis and y-axis. 
"""
def GetSIs(rd,data):
    
    
    SIs = []
    DEBUG = 0
    
    
    if DEBUG:
        print("=== INSIDE GetSIs ===")
    
    i_labels = 0
    i_units = 0
    i = -1
    for basic in rd:
        i += 1
        if DEBUG:
            if i <= 20:
                print("%d\t%d\t%s\t%s"%(i,len(basic),basic[0],basic))
        
        if basic[0] == '(':
            i_units = i
            i_labels = i-1
            if len(rd[i_labels]) < 6:
                i_labels -= 1
            break
        
        
        
    labels = rd[i_labels].split(',')
    labels = [x.replace('\n','') for x in labels]
    units = rd[i_units].split(',')
    units = [x.replace('\n','') for x in units]
    
    if DEBUG == 2:
        print(labels)
        print(units)
        print(i_labels)
        print(i_units)
    
    
    
    
    # Printing labels and units
    for i in labels:
        print("%20s"%(i),end="")
    print('\n')
    for i in units:
        print("%20s"%(i),end="")
    print('\n')
    
    
        
    available_i = range(len(data[0]))
    
    # Printing column indices
    for i in available_i:
        print("%20d"%(i),end="")
    print("\n")
    
    
    # Printing first 20 rows from data
    for i in range(10):
        for d in data[i]:
            print("%20.4f"%(d),end="")
        print("\n")
 
    goodindices = 'n'
    while goodindices == 'n':
        print(">>> Available indices: ")
        print(available_i)
        s1 = -1
        while s1 not in available_i:
            s1 = GetIntInput("<<< Use which column index on x-axis?: ")
            
        s2 = -1
        while s2 not in available_i:
            s2 = GetIntInput("<<< Use which column index on y-axis?: ")
        print("Using %s on x, and %s on y."%(labels[s1],labels[s2]))
        goodindices = GetYesOrNo("<<< Use these indices? y/n: ")
    
    
    SIs = [s1,s2]
    
    return SIs
"""
==============================================================================
"""  

"""
    GetData(rawest_data): Looks through rawest_data and gets numerical values 
    as data from it
"""
def GetData(rd):
    
    DEBUG = False
    if DEBUG: print("=== INSIDE GetData ===")
    data = []
    
    
    i = -1
    
    #i_labels = 0
    #i_units = 0
    found_data = False
    
    for basic in rd:
        i += 1
        if DEBUG:
            if i <= 20:
                print("%d\t%d\t%s\t%s"%(i,len(basic),basic[0],basic))
        
        
            
        if not found_data and ord(basic[0]) in range(48,58):
            found_data = True
            continue
            
        elif basic[0] == '"' or found_data:
            longstring = basic
            new_longstring = longstring.replace('"',"")
            new_longstring = new_longstring.replace('\n',"")
            strings = new_longstring.split(',')
            
            
            # Convert it to floats
            raw_data = [float(x) for x in strings]
            
            data.append(raw_data)
            
            
     
        #i += 1
        
    if DEBUG: print("=== EXITING GetData with data length = %d==="%(len(data)))
    return data
"""
==============================================================================
"""

"""
    GetStrain(data,SIs): Gets array of 'strain' from 'data', utilizing column
    index for strain from SIs (StressStrain Indices)
"""
def GetStrain(data,SIs):
    strain = []
    for n in data:
        strain.append(n[SIs[0]])
    return strain
"""
==============================================================================
"""
"""
    GetStress(data,SIs): Gets array of 'stress' from 'data', utilizing column
    index for strain from SIs (StressStrain Indices)
"""
def GetStress(data,SIs):
    stress = []
    for n in data:
        stress.append(n[SIs[1]])
    return stress
"""
==============================================================================
"""

"""
    Derivative(xarr,yarr,smoothness=1): Returns an array of the slope of the
    combined [xarr,yarr]. Smoothness is used to alleviate noise, with a higher
    value being more smooth, and the lowest value (1) being completely accurate.
"""
def Derivative(xarr,yarr,smoothness=1):
    d_arr = []
    for n in xarr:
        i_0 = xarr.index(n)
        
        if i_0 < len(xarr)-smoothness:
            i_f = i_0 + smoothness
            
            dx = xarr[i_f] - xarr[i_0]
            dy = yarr[i_f] - yarr[i_0]
            
            if dx == 0:
                dx = np.spacing(1)
            
            d_arr.append(dy/dx)
        
    for n in range(smoothness):
        d_arr.append(d_arr[-1])
    
    
    return d_arr
"""
==============================================================================
"""

def GetFname(prompt):
    available_extensions = ['.jpg','.png','.jpeg','.pdf',
                            '.pgf','.raw','.rgba','.tif',
                            '.tiff','.svg']
    fname_in = str(input(prompt))
    extns_in = False
    for e in available_extensions:
        if e in fname_in:
            extns_in = True
            break
    while '.' in fname_in and not extns_in:
        print(">>> ERROR: Invalid filename.")
        fname_in = str(input(prompt))
        
    return fname_in
    


"""
    PlotStrainStress(data,SIs): Uses SIs to pull strain and stress data from data,
    and plots the two. Includes legend, and intelligent axes to focus on data. 
"""
def PlotStrainStress(data,SIs):
    stress = GetStress(data,SIs)
    strain = GetStrain(data,SIs)
        

    plt.plot(strain,stress)
    plt.axis([0,1.05*max(strain),0,1.05*max(stress)])
    
    plt.title("Stress Strain Curve",weight="bold",style="italic")
    plt.grid()
    plt.xlabel("Strain (mm/mm)",style="italic")
    plt.ylabel("Stress (MPa)",style="italic")
    
    return
"""
==============================================================================
"""

"""
    GetStrainStressDerivative(data,SIs): Utilizes the Derivative() function on 
    stress and strain, pulled from data using SIs. 
"""
def GetStrainStressDerivative(data,SIs):
    stress = GetStress(data,SIs)
    strain = GetStrain(data,SIs)
    
    
    
    
        
    dS = Derivative(strain,stress,50)
    return dS
"""
==============================================================================
"""

"""
    PlotStrainStressDerivative(data,SIs): Plots the rate of change of the stress
    strain relationship. 
"""
def PlotStrainStressDerivative(data,SIs):

    strain = GetStrain(data,SIs)        
    dS = GetStrainStressDerivative(data,SIs)
    
    plt.figure()
    plt.title("Derivative of Stress Strain Curve",weight='bold',style='italic')
    plt.grid()
    plt.xlabel("Strain $\epsilon$ (mm/mm)",style='italic')
    plt.ylabel(r"$\frac{d\sigma}{d\epsilon}$",style='italic',rotation=0,fontsize = 14)
    plt.axis([0,1.05*max(strain),-16000,16000])
    
    plt.plot(strain,dS)
    plt.legend([r"$\frac{d\sigma}{d\epsilon}$"])
    if GetYesOrNo("<<< Save strain stress derivative? y/n: ") == 'y':
        fname = GetFname("<<< Filename to save to?: ")
        fpath = '/users/ryanlittle/desktop/'
        plt.savefig(fpath+fname,bbox_inches='tight')
    plt.show()
    

    return
"""
==============================================================================
""" 
  
"""
    GetUTS(data,SIs): Gets the ultimate tensile strength, or overall maximum
    stress recorded from data. Returns the max value, as well as the index in 
    data that corresponds to it.
"""
def GetUTS(data,SIs):
    
    strain = GetStrain(data,SIs)
    stress = GetStress(data,SIs)
        
    max_stress = max(stress)
    i = stress.index(max_stress)
    corresponding_strain = strain[i]
    
    return (corresponding_strain,max_stress)
"""
==============================================================================
"""

"""
    GetIntersectIndex(trendline_y,stress): Gets the maximum index out of array
    of all intersection indeces between trendline and the stress strain curve.
    Max index is returned, as there may be multiple intersections before the 
    yield point is reached. 
"""
def GetIntersectIndex(trendline_y,stress):
    
    
    intersect_indeces = []
    d = []
    for i in range(len(trendline_y)):
        d.append(stress[i]-trendline_y[i])
        
    for i in range(len(d)-1):
        if d[i] == 0 or d[i] * d[i+1] < 0:
            intersect_indeces.append(i)
    
    return max(intersect_indeces)
"""
==============================================================================
"""

"""
    GetR2(data,SIs): Gets the R-squared coefficient for 'data' provided. This
    is utilized by GetTrendline(), where the data provided as an argument is 
    not the full dataset, but only some initial part. 
"""
def GetR2(data,SIs):
    x = GetStrain(data,SIs)
    y = GetStress(data,SIs)
    
    
    sum_a = 0
    sum_b = 0
    sum_c = 0
    sum_d = 0
    sum_e = 0
    n = len(x)
    
    for i in range(len(x)):
        sum_a += x[i]*y[i]
        sum_b += x[i]
        sum_c += y[i]
        sum_d += x[i]**2
        sum_e += y[i]**2
        
        numer = (n*sum_a - sum_b*sum_c)
        denom = math.sqrt((n*sum_d-sum_b**2)*(n*sum_e-sum_c**2))
        
        # Avoiding float division by zero
        if denom == 0:
            denom = 0.000001
    
    r = numer/denom
    
    return r**2
"""
==============================================================================
"""      

"""
    GetTrendline(data,SIs,plotdata=False,plotr2=False): Gets the slope and 
    y-intercept for the trendline representing the initial region of the curve.
    Returns [slope,y-intercept], and can plot the curve with the trendline
    overlaid, as well as the plot of R^2 value for increasing amount of data
    points used.
"""
def GetTrendline(data,SIs,plotdata=False,plotr2 = False):
    strain = GetStrain(data,SIs)
    stress = GetStress(data,SIs)
        
    r2s = []
    for i in range(int(0.5*len(strain))):
        ndata = data[0:i+2]
        r2 = GetR2(ndata,SIs)
        r2s.append(r2)
        
    r2s_no_dirt = r2s[int(0.02*len(r2s)):]
    max_r2 = max(r2s_no_dirt)
    i_c = r2s.index(max_r2)
    
    if plotr2:
        plt.plot(r2s_no_dirt)
        plt.title("$R^2$ Values for increasing linear range",style='italic',weight='bold')
        plt.xlabel("Length of data set",style='italic')
        plt.ylabel("$R^2$ value",style='italic')
        plt.grid()
        plt.legend(["$R^2$ Value"])
        if GetYesOrNo("<<< Save r2 figure? y/n: ") == 'y':
            fname = GetFname("<<< Filename to save to?: ")
            fpath = '/users/ryanlittle/desktop/'
            plt.savefig(fpath+fname,bbox_inches='tight')
        plt.show()
        
    
    xstrain = strain[0:i_c+2]
    ystress = stress[0:i_c+2]
    
    z = np.polyfit(xstrain,ystress,1)
    p = np.poly1d(z)
    
    if plotdata:
        plt.plot(strain,stress)
        plt.plot(strain,p(strain),"r--")
        plt.axis([0,1.05*max(strain),0,1.05*max(stress)])
        plt.grid()
        plt.title("Stress Strain Curve",style='italic',weight='bold')
        plt.xlabel("Strain $\epsilon$ (mm/mm)",style='italic')
        plt.ylabel("Stress $\sigma$ (MPa)",style='italic')
        plt.legend(["Stress Strain Curve","Hookean Region Trendline"])
        if GetYesOrNo("<<< Save trendline figure? y/n: ") == 'y':
            fname = GetFname("<<< Filename to save to?: ")
            fpath = '/users/ryanlittle/desktop/'
            plt.savefig(fpath+fname,bbox_inches='tight')
        plt.show()
        
            
        print(">>> y=%.6fx+(%.6f)"%(z[0],z[1]))
        print(">>> R value: %0.6f"%max_r2)
    
    #z[0] is slope, z[1] is y-intercept
    
    return z
"""
==============================================================================
"""  

"""
    rangeof(arr): Returns not the length of the array, but the total difference
    between values of the array. 
"""
def rangeof(arr):
    return abs(max(arr)-min(arr))
"""
==============================================================================
"""

"""
    GetYield(data,SIs): Returns [yield_strain,yield_stress] as calculated by 
    the 0.2% offset method, and can plot the curve as well. 
"""
def GetYield(data,SIs,plottrendline=False,plotoffset=False,plotr2=False): 
    
    strain = GetStrain(data,SIs)
    stress = GetStress(data,SIs)
    
    
    
    trendline = GetTrendline(data,SIs,plottrendline,plotr2)
    slope = trendline[0]
    y_int = trendline[1]
    offset = 0.002*max(strain)
    
    # Y = slope(x-offset)+y_int
    
    ys = [slope*(x-offset)+y_int for x in strain]
    
    yield_i = GetIntersectIndex(ys,stress)
    yield_strain = strain[yield_i]
    yield_stress = stress[yield_i]
    
    
    if plotoffset:
        
        
        
        plt.plot(strain,stress)
        plt.plot(strain,ys)
        plt.axis([min(strain)-0.025*rangeof(strain),1.15*strain[yield_i],min(stress)-0.15*rangeof(stress),1.15*stress[yield_i]])
        plt.grid()
        plt.title("Initial Region of Curve",weight='bold',style='italic')
        plt.xlabel("Strain $\epsilon$ (mm/mm)",style='italic')
        plt.ylabel("Stress $\sigma$ (MPa)",style='italic')
        plt.legend(["Stress Strain curve","0.2% Offset Line"])
        if GetYesOrNo("<<< Save initial region figure? y/n: ") == 'y':
            fname = GetFname("<<< Filename to save to?: ")
            fpath = '/users/ryanlittle/desktop/'
            plt.savefig(fpath+fname,bbox_inches='tight')
        plt.show()
        
        print(">>> Yield strain: %0.6f\n>>> Yield stress: %0.6f"%(yield_strain,yield_stress))
    
    
    
    return [yield_strain, yield_stress]
"""
==============================================================================
"""

"""
    mean(arr): Returns the average value of the array. 
"""
def mean(arr):
    total = 0
    for n in arr:
        total += n
    return total/len(arr)
"""
==============================================================================
"""
"""
    sign(a): Returns a positive or negative 1, depending on the sign of a. 
"""
def sign(a):
    if a < 0:
        return -1
    else:
        return 1
"""
==============================================================================
"""

"""
    GetDropIndices(data,SIs,threshold): Gets indeces where the values of stress
    change suddenly by the 'threshold' amount. 
"""
def GetDropIndices(data,SIs,threshold):
 
    stress = GetStress(data,SIs)
        
    drop_indices = []
    
    for i in range(len(stress)-1):
        a = stress[i]
        b = stress[i+1]
        
        if a-b > threshold:
            drop_indices.append(i)
    
    return drop_indices
"""
==============================================================================
"""

"""
    GetBreakPoint(data,SIs): Calculates where there is a sudden drop in stress
    values, *after* the UTS point has been reached, utilizing the GetDropIndices()
    function
"""
def GetBreakPoint(data,SIs):
    strain = GetStrain(data,SIs)
    stress = GetStress(data,SIs)
    
    threshold = rangeof(stress)/85                  # Experimentally determined the '85.'
    
    drops = GetDropIndices(data,SIs,threshold)
    uts = GetUTS(data,SIs)
    uts_i = stress.index(uts[1])
    
    break_index = 0
    for d in drops:
        if d > uts_i:
            break_index = d
            break
            
    return [strain[break_index],stress[break_index]]
"""
==============================================================================
"""

"""
    PlotAll(data,SIs,E,UTS,Yield,breakpoint): Plots all curves. 
"""
def PlotAll(data,SIs,E,UTS,Yield,breakpoint):
    strain = GetStrain(data,SIs)
    stress = GetStress(data,SIs)
    
    plt.figure()
    plt.plot(strain,stress)
    
    plt.plot(Yield[0],Yield[1],'ro')
    plt.plot(UTS[0],UTS[1],'r^')
    plt.plot(breakpoint[0],breakpoint[1],'rx')
        
    plt.axis([0,1.05*max(strain),0,1.05*max(stress)])
    
    plt.title("Stress Strain Curve",weight="bold",style="italic")
    plt.grid()
    plt.xlabel("Strain $\epsilon$ (mm/mm)",style="italic")
    plt.ylabel("Stress $\sigma$ (MPa)",style="italic")
    plt.legend(["Stress strain curve","Yield point","UTS point","Break point"])
    if GetYesOrNo("<<< Save stress strain figure? y/n: ") == 'y':
        fname = GetFname("<<< Filename to save to?: ")
        fpath = '/users/ryanlittle/desktop/'
        plt.savefig(fpath+fname,bbox_inches='tight')
    plt.show()
    
    
    
    PlotStrainStressDerivative(data,SIs)
    
    GetYield(data,SIs,plottrendline=True,plotoffset=True,plotr2=True)
    
    return
"""
==============================================================================
"""

"""
    Group of default menu-driven functions.
"""
def PrintMenu(ol, rl):
    for n in range(len(ol)):
        print(rl[n],"\t",ol[n])
        
    return
    
def GetMenuChoice(rl):
    r = str(input("<<< Choice: "))
    while r not in rl:
        print(">>> ERROR: Invalid selection")
        r = str(input("<<< Choice: "))
        
    return r

def GetYesOrNo(prompt):
    resp = str(input(prompt))
    while resp not in ['y','n']:
        print(">>> ERROR: Invalid response.")
        resp = str(input(prompt))
        
    return resp

def EnterToContinue():
    input("<<<  Hit enter to continue: ")
    return
"""
==============================================================================
"""

"""
    PWD(in_workingdir,workingdir): Prints the contents of the current working
    directory, as utilized by the FileSearch() function.
"""
def PWD(in_workingdir,workingdir):
    print("\n>>> Directories available in %s:\n"%(workingdir))
    for d in in_workingdir:
        if d[0] != '.':
            print(">>>\t%s"%(d))
    return
"""
==============================================================================
"""

"""
    FileSearch(): Allows the user to search through the directory of the hard
    drive, and selecting a file to be used by the program. 
"""
def FileSearch():
    
    ol = ['Open directory','Go up directory','Quit']
    rl = ['a','b','x']
    

    print(">>> Search for directory.")
    r1 = ''
    workingdir = ''
    in_workingdir = []
    
    
    while r1 != 'x':
        workingdir = workingdir.replace("//",'/')
        PWD(in_workingdir,workingdir)
        print('\n')
        PrintMenu(ol,rl)
        r2 = GetMenuChoice(rl)
        
        if r2 == 'a':
            r1 = str(input("Enter in directory or filepath, or x to quit: "))
            if r1 == 'x':
                break
            
            
            
            
            workingdir += r1
            
            if '.' in workingdir:
                my_file = Path(workingdir)
                if my_file.is_file():
                    print("Use %s as filename?"%(workingdir))
                    ryn = GetYesOrNo("<<< y/n: ")
                    if ryn == 'y':
                        return workingdir
                    else:
                        if workingdir.endswith(r1):
                            workingdir = workingdir[:-1(len(r1))]
                            continue
                else:
                    print(">>> ERROR: Invalid filename.")
                    if workingdir.endswith(r1):
                        workingdir = workingdir[:-1(len(r1))]
                        continue
            
            
            my_dir = Path(workingdir)
            
            if my_dir.is_dir():
                in_workingdir = listdir(workingdir)
        
            else:
                print(">>> ERROR: %s is not a valid directory."%(workingdir))
                if workingdir.endswith(r1):
                    workingdir = workingdir[:-len(r1)]
                continue
            
            
        elif r2 == 'b':
            if workingdir.endswith(r1):
                workingdir = workingdir[:-len(r1)]
                in_workingdir = listdir(workingdir)
            
            
        else:
            break

    return None
"""
==============================================================================
"""

"""
    SaveOutput(): Saves text output for material properties.
"""
def SaveOutput(E,UTS,Yield,breakpoint,fname2):
    
    name = str(input("<<< Filename to save as?: "))
    fpath = '/users/ryanlittle/desktop/'
    fname = fpath+name
    
    print(">>> Saving to %s"%(fname))
    
    s_arr = ["Elastic modulus E:","Trendline y-int:",
             "UTS Point Strain:","          Stress:",
             "Yield Strain:","      Stress:",
             "Breakpoint Strain:","           Stress:"]
    
    d_arr = [E[0],E[1],UTS[0],UTS[1],
             Yield[0],Yield[1],
             breakpoint[0],breakpoint[1]]
    
    u_arr = ['(MPa)','(MPa)',
             '(mm/mm)','(MPa)',
             '(mm/mm)','(MPa)',
             '(mm/mm)','(MPa)']
  
    
    f = open(fname,'w')
    
    f.write(">>> Data from %s\n\n"%fname2)
    
    for i in range(len(s_arr)):
        writestring = "%20s%10.4f%10s\n"%(s_arr[i],d_arr[i],u_arr[i])
        f.write(writestring)
    current_date = time.strftime("%m/%d/%Y")
    f.write('\n\n\n>>> Created using UniaxialFileHandler on %s'%current_date)
    
    f.close()
    
    return
"""
==============================================================================
"""






"""
    main(): Runs the program.
"""
def main():
    
    r = 'y'
    
    while r == 'y':
        
    
        fname = FileSearch()
        #fname = '/users/ryanlittle/documents/python3docs/materials files/aluminum1.csv'
        if fname == None:
            return
        print("\n>>> File:\t\t\t%s\n"%fname)
        
        data = GetData(GetRawestData(fname))
        rd = GetRawestData(fname)
        SIs = GetSIs(rd,data)

        E = GetTrendline(data,SIs)
        UTS = GetUTS(data,SIs)
        Yield = GetYield(data,SIs)
        breakpoint = GetBreakPoint(data,SIs)
        
        print(">>> Elastic modulus:\t\t%0.3f"%E[0])
        print(">>> Yield strain:\t\t%0.3f (mm/mm)\n>>> Yield Stress:\t\t%0.3f (MPa)"%(Yield[0],Yield[1]))
        print(">>> Ultimate Tensile Strength:\t%0.3f (MPa)"%UTS[1])
        print(">>> Break strain:\t\t%0.3f (mm/mm)\n>>> Break Stress:\t\t%0.3f (MPa)"%(breakpoint[0],breakpoint[1]))
        
        if GetYesOrNo("<<< Save output to file? y/n: ") == 'y': SaveOutput(E,UTS,Yield,breakpoint,fname)
        if GetYesOrNo("<<< Show data plots? y/n: ") == 'y': PlotAll(data,SIs,E,UTS,Yield,breakpoint)
        
        
        
        r = GetYesOrNo("<<< Run again for another file? y/n: ")
    
    return

"""
==============================================================================
"""

if RUNMAIN:
    main()
    
print(">>> Closing.")





