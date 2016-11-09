#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Sat Oct 15 17:17:30 2016

#@author: ryanlittle








# Any live cell with fewer than two live neighbours dies, as if caused by under-population.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by over-population.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.


import os
import time
import random
import matplotlib.pyplot as plt




def zeros(rows,cols):
    a = []
    for j in range(0,cols):
        b = []
        for i in range(0,rows):
            b.append(0)
        a.append(b)
    return a



def printscreen(a,dc,lc):
    cols = len(a)
    rows = len(a[0])
    print("\n")
    for j in range(0,cols):
        print('%3d' % (cols-j)," ",end="")
        for i in range(0,rows):
            if a[j][i] == 1:
                print(lc," ",end="")
            else:
                print(dc," ",end="")
            
        print("")
    print("   ",end="")
    for i in range(0,rows):
        print('%3d' % (i+1),end="")
    print("\n")
    return

#live_neighbors = a[ju][i]+a[ju][ir]+a[j][ir]+a[jd][ir]+a[jd][i]+a[jd][il]+a[j][il}+a[ju][il]
        
def GetNumLiveNeighbors(x,y,i,j,a):
    # Initial testcase: i = 20, j = 10
    # Here we pass:     x = 19, y = 0
    live_neighbors = 0
    ju = y - 1
    jd = y + 1
    ir = x + 1
    il = x - 1
    #for n in a:
        #print n
    #print "\nx = ",x," y = ",y," i = ",i," j = ",j
    #print "ju = ",ju," jd = ",jd," ir = ",ir," il = ",il,"\n"
    addlist = [0,0,0,0,0,0,0,0]
    if ju < 0 and il < 0:
        # Case of top left corner
        #print "Case top left corner"
        addlist[2] = a[y][ir]
        addlist[3] = a[jd][ir]
        addlist[4] = a[jd][x]
    elif ju < 0 and il >= 0 and ir < i:
        # Case of top row, not including corners
        #print "Case top row"
        addlist[2] = a[y][ir]
        addlist[3] = a[jd][ir]
        addlist[4] = a[jd][x]
        addlist[5] = a[jd][il]
        addlist[6] = a[y][il]
    elif ju < 0 and ir >= i:
        # Case top right corner
        #print "Case top right corner"
        addlist[4] = a[jd][x]
        addlist[5] = a[jd][il]
        addlist[6] = a[y][il]
    elif ir >= i and ju >= 0 and jd < j:
        # Case rightmost column, not including corners
        #print "Case right column"
        addlist[0] = a[ju][x]
        addlist[4] = a[jd][x]
        addlist[5] = a[jd][il]
        addlist[6] = a[y][il]
        addlist[7] = a[ju][il]
    elif ir >= i and jd >= j:
        # Case bottom right corner
        #print "Case bottom right corner"
        addlist[6] = a[y][il]
        addlist[7] = a[ju][il]
        addlist[0] = a[ju][x]
    elif jd >= j and il >= 0 and ir < i:
        # Case bottom row
        #print "Case bottom row"
        addlist[0] = a[ju][x]
        addlist[1] = a[ju][ir]
        addlist[2] = a[y][ir]
        addlist[6] = a[y][il]
        addlist[7] = a[ju][il]
    elif jd >= j and il < 0:
        # Case bottom left corner
        #print "Case bottom left corner"
        addlist[0] = a[ju][x]
        addlist[1] = a[ju][ir]
        addlist[2] = a[y][ir]
    elif il < 0 and ju <= 0 and jd < j:
        # Case leftmost column
        #print "Case left column"
        addlist[0] = a[ju][x]
        addlist[1] = a[ju][ir]
        addlist[2] = a[y][ir]
        addlist[3] = a[jd][ir]
        addlist[4] = a[jd][x]
    else:
        # Case anywhere in the middle, where none of the values are negative or outside bounds
        #print "Anywhere else"
        addlist[0] = a[ju][x]
        addlist[1] = a[ju][ir]
        addlist[2] = a[y][ir]
        addlist[3] = a[jd][ir]
        addlist[4] = a[jd][x]
        addlist[5] = a[jd][il]
        addlist[6] = a[y][il]
        addlist[7] = a[ju][il]
        
    #print "Addlist: "
    for n in addlist:
        #print n,
        live_neighbors += n
    #print "\nLive neighbors = ",live_neighbors
    return live_neighbors
        
# Returns 0 if it should die
# Returns 1 if it should stay alive
def StayAlive(x,y,a):
    cols = len(a)
    rows = len(a[0])
    num_live_neighbors = GetNumLiveNeighbors(x,y,rows,cols,a)
    #print x,y,rows,cols,"nln's = ",num_live_neighbors,
    alive = a[y][x]
    #print alive
    if alive == 1:
        # If cell at point (x,y) is alive
        if num_live_neighbors == 2 or num_live_neighbors == 3:
            return 1
        else:
            return 0
    else:
        if num_live_neighbors == 3:
            return 1
        else:
            return 0
        




def TwoDimMatrixEquality(a,b):
    cols = len(a)
    rows = len(a[0])
    equal = True
    for j in range(0,cols):
        for i in range(0,rows):
            if a[j][i] != b[j][i]:
                equal = False
    return equal

def MatrixAIntoB(a,b):
    cols = len(a)
    rows = len(a[0])
    #b = zeros(rows,cols)
    for j in range(0,cols):
        for i in range(0,rows):
            b[j][i] = a[j][i]
    return b



def NextGeneration(a):
    cols = len(a)
    rows = len(a[0])
    b = zeros(rows,cols)
    for j in range(0,cols):
        for i in range(0,rows):
            b[j][i] = StayAlive(i,j,a)
    for j in range(0,cols):
        for i in range(0,rows):
            a[j][i] = b[j][i]
    return a


def AlivesCounter(a):
    cols = len(a)
    rows = len(a[0])
    total = 0
    for j in range(0,cols):
        for i in range(0,rows):
            total += a[j][i]
    return total
    
    
    
def GameOfLife(a,n,t,dc,lc):
    stable_state = False
    oscillating_state = False
    ignore_repeating = False
    period = 0
    prev_a = []
    cols = len(a)
    rows = len(a[0])
    prev_a = zeros(rows,cols)
    MatrixAIntoB(a,prev_a)
    alives_history = []
    t0 = time.time()
    gens_counted = 0
    gens_to_print = 0
    pop_hist = []

    for i in range(0,n):
        alives_history.append(zeros(rows,cols))
    
    for i in range(0,n):
        
        pop_hist.append(AlivesCounter(a))
        if ignore_repeating == False:
            if stable_state:
                print("Stable state reached after ",i-1," generations.")
                tf = time.time()
                gens_to_print = gens_counted
                break
            if oscillating_state:
                tf = time.time()
                gens_to_print = gens_counted
                print("Oscillating state reached",end="")
                print("with a period of ",end="")
                print(period)
                continue_anyway = GetYesOrNo("Continue anyway? y/n: ")
                if continue_anyway == "y":
                    ignore_repeating = True
                else:
                    break
        
        print("Generation: ",i+1)
        MatrixAIntoB(a,prev_a) 
        NextGeneration(a)
        printscreen(a,dc,lc) 
        gens_counted += 1
        
        MatrixAIntoB(prev_a,alives_history[i])
        
        
        if ignore_repeating == False:
            if i > 0:
                
                for alive in alives_history:
                    #index_a = alives_history.index(alive)
                    if TwoDimMatrixEquality(a,alive):
                        # If the current living alives is equal to some historically alive
                        # The index if current living were to be appended to history = i + 1
                        # The equal historical population's index is...
                        index = alives_history.index(alive)
                        diff = i + 1 - index
                        
                        if diff == 1:
                            stable_state = True
                        else:
                            oscillating_state = True
                            period = diff
                            
                            
        
        clearname = ''
        if os.name == 'posix':
            clearname = 'clear'
        elif os.name == 'nt':
            clearname = 'cls'
        time.sleep(t)
        if i != n-1:
            if (stable_state == True or oscillating_state == True) and ignore_repeating == False:
                blah = 0
            else:
                os.system(clearname)
                print("")
        tf = time.time()
        gens_to_print = gens_counted
    
    
    dt = tf-t0
    avg_t_per_gen = dt/gens_to_print
    time_diff = abs(avg_t_per_gen - t)
    print("%.3f" % dt,"seconds for ",gens_to_print,"generations.")
    print("%.3f" % avg_t_per_gen,"seconds per generation.")
    print("%.3f" % time_diff,"seconds off expected time per generation.")
    viewplot = GetYesOrNo("View plot of population vs time? y/n: ")
    if viewplot == "y":
        plt.plot(pop_hist)
        plt.ylabel("Population")
        plt.xlabel("Generation")
        plt.show()
    
        
        
 
def GetCoord(prompt,maxindex):
    a = int(input(prompt))
    while a > maxindex or a < 0:
        print("ERROR: Invalid index.")
        a = int(input(prompt))
    return a

def GetAliveOrDead():
    print("0 - Dead\n1 - Alive")
    a = int(input("Choice: "))
    while a != 0 and a != 1:
        print("ERROR: Invalid value.")
        a = int(input("Choice: "))
    return a
    
def GetYesOrNo(prompt):
    resp = str(input(prompt))
    while resp != 'y' and resp != 'n':
        print("ERROR: Invalid response.")
        resp = str(input(prompt))
    return resp
        


def AlivesFiller(a,dc,lc):
    cols = len(a)
    rows = len(a[0])
    maxx = rows-1
    maxy = cols-1
    #print("Note: y starts at 0 at the top, and increases towards the bottom.")
    resp = 'y'
    print("Max x coord = ",maxx,end="")
    print("Max y coord = ",maxy)
    while resp == 'y':
        x_upload = GetCoord("x coord: ",maxx)
        x_upload -= 1
        y_upload = GetCoord("y coord: ",maxy)
        y_upload = cols - y_upload
        value = GetAliveOrDead()
        a[y_upload][x_upload] = value
        printscreen(a,dc,lc)
        print("(",x_upload+1,",",cols-y_upload,") = ",value)
        resp = GetYesOrNo("Change another cell? y/n: ")


def GetSideLen(prompt):
    l = int(input(prompt))
    while l < 0:
        print("ERROR: Invalid dimension.")
        l = int(input(prompt))
    return l


def GetMenuChoice(ol,rl):
    for option in ol:
        print(option)
    resp = str(input("Choice: "))
    while resp not in rl:
        print("ERROR: Invalid response.")
        resp = str(input("Choice: "))
    return resp


def FillAlivesWithRandom(a,seed):
    cols = len(a)
    rows = len(a[0])
    max_cells = cols*rows
    random.seed(seed)
    already_filled = []
    
    num_cells = int(input("Num cells: "))
    while num_cells < 0 or num_cells > max_cells:
        print("ERROR: Invalid number. ",end="")
        if num_cells > max_cells:
            print("Max cells = ",max_cells,end="")
        print("")
        num_cells = int(input("Num cells: "))
    
    for i in range(0,num_cells):
        x_rand = random.randint(0,rows-1)
        y_rand = random.randint(0,cols-1)
        
        # If (x_rand,y_rand) has already been used
        for a in already_filled:
            if [x_rand,y_rand] == a:
                # Run it one more time, and skip this current iteration
                num_cells += 1 
                continue
        
        a[y_rand][x_rand] = 1        
        
        
  
    
def GetNumGens():
    a = int(input("Number of generations?: "))
    while a < 0:
        print("ERROR: Number must be positive.")
        a = int(input("Number of generations?: "))
    return a  

def GetString(prompt):
    path = str(input(prompt))
    return path
    
   
    
     
      
       
        
         
          
def PrintAvailableFiles():
    stock_filepath = "/Users/ryanlittle/Desktop/Applets/PythonTextDocs/"
    list_filename = "GAME_OF_LIFE_FILENAMES.txt"
    f = open(stock_filepath+list_filename,'r')
    for line in f:
        print("\t",line)
    f.close()           
            
                                
              
               
                 
def LoadFile(rows,cols):
    a = []
    stock_filepath = "/Users/ryanlittle/Desktop/Applets/PythonTextDocs/"
    print("Stock containing folder: ",stock_filepath)
    use_this = GetYesOrNo("Use this? y/n: ")
    filepath = ""
    if use_this == 'y':
        filepath = stock_filepath
    else:
        filepath = GetString("Filepath of containing folder: ")
    PrintAvailableFiles()
    filename = GetString("Filename: ")
    
    
    f = open(filepath+filename,'r')
    
    a = []
    for j in range(0,cols):
        b = []
        print("\tOn j = ",j)
        for i in range(0,rows):
            print("\t\tOn i = ",i)
            inchar = f.read(1)
            inchar = int(inchar)
            b.append(inchar)
        a.append(b)
        junk = f.read(1)
    
    return a
    
    
    
    
    
    
    
    
def AddFilenameToList(name):
    stock_filepath = "/Users/ryanlittle/Desktop/Applets/PythonTextDocs/"
    list_filename = "GAME_OF_LIFE_FILENAMES.txt"
    f = open(stock_filepath+list_filename,'r+')
    names = []
    #for line in f:
     #   names.append(line)
    names.append(name)
    for filename in names:
        f.write(filename)
    return
    
    

    
    
    
def SaveFile(a):
    
    stock_filepath = "/Users/ryanlittle/Desktop/Applets/PythonTextDocs/"
    resp = GetYesOrNo("Save this population?: y/n: ")
    if resp == 'y':
        print("Stock containing folder: ",stock_filepath)
        use_this = GetYesOrNo("Use this? y/n: ")
        filepath = ""
        if use_this == 'y':
            filepath = stock_filepath
        else:
            filepath = GetString("Filepath of containing folder: ")
        filename = GetString("Filename: ")
        AddFilenameToList(filename)
        f = open(filepath+filename,'w')
        for j in a:
            for i in j:
                f.write(str(i)),
            f.write('\n')   
    return
    
    
    
    
def GetTime():
    a = float(input("How many seconds per generation? "))
    while a < 0:
        print("ERROR: Invalid length of time.")
        a = float(input("How many seconds per generation? "))
    #if a < 0.5:
        #print "Warning: Screen may be hard to see."
    return a
       
    
    
    
def GetDCandLC(dc,lc):
    print("Dead character: ",dc)
    print("Live character: ",lc)
    usethese = "n" #GetYesOrNo("Use these indicators? y/n: ")
    if usethese == "n":
        dc = str(input("Dead character: "))
        lc = str(input("Live character: "))
    return [dc,lc]



def PrintParameters(rows,cols,dc,lc,n_gens,time,seed):
    print("%-30s" % "Horizontal length: ","%5d" % rows)
    print("%-30s" % "Vertical length: ","%5d" % cols)
    print("%-30s" % "Dead character: ","%5s" % dc)
    print("%-30s" % "Live character: ","%5s"% lc)
    print("%-30s" % "# Generations: ","%5d" % n_gens)
    print("%-30s" % "Seconds per generation: ","%5.2f" % time)
    print("%-30s" % "Random's seed: ",seed)
    return


    
def SampleSituations():
    stock_filepath = "/Users/ryanlittle/Desktop/Applets/PythonTextDocs/"
    filename = "SampleSituations.txt"
    f = open(stock_filepath+filename,'r+')
    for line in f:
        print(line)
    AddLine = GetYesOrNo("Add situation? ")
    if AddLine == "y":
        inputstring = str(input("Text to add: "))     
        f.write("\n"+inputstring)
    
    



# =========================================================================================================
def main():
    
    # NOTE: rows and cols have the number of elements in each row and each column respectively
    cont = 'y'
    rows = 20
    cols = 20
    dc = "."
    lc = "@"
    
    num_gens = 1000
    t = 0.01
    
    seed = "00000"
    clearname = ""
    
    
    
    
    osname = os.name
    if osname == 'posix':
        clearname = 'clear'
    elif osname == 'nt':
        clearname = 'cls'
    
    while cont == 'y':
        
        
        #chars = GetDCandLC(dc,lc)
        #dc = chars[0]
        #lc = chars[1]
        #print "Screensize = ",rows,"x",cols
        #changesize = GetYesOrNo("Change size? y/n: ")
        #if changesize == 'y':
            #rows = GetSideLen("Horizontal dimension: ")
            #cols = GetSideLen("Vertical dimension: ") 
        
        alives = zeros(rows,cols)
        #printscreen(alives,dc,lc)
        
        
        
        ready_to_run = "n"
        
        while ready_to_run == "n":
            #os.system('clear')
            printscreen(alives,dc,lc)
            PrintParameters(rows,cols,dc,lc,num_gens,t,seed)
            print("\n\n\tOptions:\n")
            menu_options = ['a: Fill randomly',
                            'b: Fill manually',
                            'c: Load saved',
                            'd: Change dimensions (Clears living cells)',
                            'e: Change indicators',
                            'f: Change # generations',
                            'g: Change seconds per generation',
                            'h: Change seed',
                            'i: Save population',
                            'j: Display example situations',
                            'r: Run simulation',
                            'x: Quit']
            menu_responses = ['a','b','c','d','e','f','g','h','i','j','r','x']
            fillerchoice = GetMenuChoice(menu_options,menu_responses)
        
        
            if fillerchoice == 'a':
                FillAlivesWithRandom(alives,seed)
                #printscreen(alives,dc,lc)
                #SaveFile(alives)
                continue
        
            elif fillerchoice == 'b':
                AlivesFiller(alives,dc,lc)
                printscreen(alives,dc,lc)
                #SaveFile(alives)
                continue
        
            elif fillerchoice == 'c':
                alives = LoadFile(rows,cols)
                #printscreen(alives,dc,lc)
                continue
        
            elif fillerchoice == 'd':
                rows = GetSideLen("Horizontal dimension: ")
                cols = GetSideLen("Vertical dimension: ")
                alives = zeros(rows,cols)
                printscreen(alives,dc,lc)
                good_dims = GetYesOrNo("Is this a good size? y/n: ")
                while good_dims == "n":
                    rows = GetSideLen("Horizontal dimension: ")
                    cols = GetSideLen("Vertical dimension: ")
                    alives = zeros(rows,cols)
                    printscreen(alives,dc,lc)
                    good_dims = GetYesOrNo("Is this a good size? y/n: ")
                os.system(clearname)
                continue
        
            elif fillerchoice == 'e':
                chars = GetDCandLC(dc,lc)
                dc = chars[0]
                lc = chars[1]
                continue
        
            elif fillerchoice == 'f':
                num_gens = GetNumGens()
                continue
            
            elif fillerchoice == 'g':
                t = GetTime()
                continue
        
            elif fillerchoice == 'i':
                SaveFile(alives)
                continue
            
            elif fillerchoice == 'h':
                use_time_seed = GetYesOrNo("Use current time for seed? y/n: ")
                if use_time_seed == "y":
                    current_time = time.time()
                    seed = str(current_time)
                else:
                    seed = str(input("Seed: "))
                continue
            
            elif fillerchoice == 'j':
                SampleSituations()
                continue
            
            elif fillerchoice == 'r':
                GameOfLife(alives,num_gens,t,dc,lc)
                input("Hit enter to continue: ")
                os.system(clearname)
                continue
            else:
                break
                
                
            ready_to_run = GetYesOrNo("Add a continue statement dumbass? y/n: ")
        
        #original_alives = []
        #original_alives = alives
        #printscreen(alives,dc,lc)
        #num_gens = GetNumGens()
        #time = GetTime()
        #ready = GetYesOrNo("Run? y/n: ")
        #if ready == "y":    
            #GameOfLife(alives,num_gens,time,dc,lc)
        #SaveFile(original_alives)
        cont = GetYesOrNo("Start over? y/n: ")
    
    
    return
# =========================================================================================================    
    
    
main()
