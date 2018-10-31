#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 17:40:33 2018

This program will automatically generate the points for the upper and lower airfoil curves.


@author: ryanlittle
"""


USE_GUI = True



"""
These variables are what go on your individual computer! Set these yourself or you'll have to re-enter them every time, manually.

"""

default_fname1 = "Upper.pts"
default_fname2 = "Lower.pts"


import os








import numpy as np
#import matplotlib.pyplot as plt

import matplotlib
if USE_GUI: matplotlib.use('TkAgg')
from matplotlib.backends.backend_agg import FigureCanvasAgg

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler

from matplotlib.figure import Figure











# This function generates the x coordinates for the airfoil profile, separated into 'front' and 'back.'
def Generate_X(npoints,p,c):
    x_step = c/npoints
    x_init = np.arange(0,p*c,x_step).tolist()
    x_back = np.arange(p*c + x_step, c, x_step).tolist()
    return x_init,x_back

# This function returns the y coordinates for the camber line.
def Y_c(X,m,p,c):
    xs = X[0]
    Y_init = []
    for x in xs:
        y_init = (m/(p**2))*(2*p*(x/c) - (x/c)**2)
        Y_init.append(y_init)
    
    xs = X[1]
    Y_back = []
    for x in xs:
        y_back = (m/((1-p)**2))*((1-2*p) + 2*p*(x/c) - (x/c)**2)
        Y_back.append(y_back)
    
    Yc = Y_init+Y_back
    
    return Yc

# This function returns the y coordinates for the thickness profile.
def Y_t(X,t):
    xs = X[0]+X[1]
    Yt = []
    for x in xs:
        Yt_i = 5*t*(0.2969*x**0.5 - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1015*x**4)
        Yt.append(Yt_i)
    
    return Yt

# This function returns the y coordinates for the derivative with respect to x.
def dYcdx(X,m,p,c):
    xs = X[0]
    dy_init = []
    for x in xs:
        dy = (2*m/(p**2))*(p-x/c)
        dy_init.append(dy)
        
    xs = X[1]
    dy_back = []
    for x in xs:
        dy = (2*m/((1-p)**2))*(p-x/c)
        dy_back.append(dy)
    
    dy = dy_init + dy_back
    
    return dy
    
    
# This function calculates the coordinate points for the airfoil profile, given the 4 digit parameters and the X coordinates.
def Get_UL(X,m,p,c,t):
    
    x = X[0]+X[1]
    yt = Y_t(X,t)
    yc = Y_c(X,m,p,c)
    dy = dYcdx(X,m,p,c)
    
    XU = []
    XL = []
    
    YU = []
    YL = []
    
    for i in range(len(yt)):
        x_i = x[i]
        yt_i = yt[i]
        yc_i = yc[i]
        dy_i = dy[i]
        th_i = np.arctan(dy_i)
        
        xU = x_i - yt_i*np.sin(th_i)
        xL = x_i + yt_i*np.sin(th_i)
        
        yU = yc_i + yt_i*np.cos(th_i)
        yL = yc_i - yt_i*np.cos(th_i)
        
        XU.append(xU)
        XL.append(xL)
        YU.append(yU)
        YL.append(yL)
        

    return [[XU,YU],[XL,YL]]


# This function exports the data as one combined file.
def ExportToFile_Combined(Data,plane,fname1,fname2,s):
    
    D_Up, D_Down = Data[0],Data[1]
    N = len(D_Up[0])
        
    data = []
    for i in reversed(range(N)):
        data.append([D_Up[0][i],D_Up[1][i]]) # Iterating backwards, to create one curve??
        
    for j in range(N):
        data.append([D_Down[0][j],D_Down[1][j]])
            
    writedata = []
    i = 0
    N = len(data)
    
    if plane == "xz": # Y is constant!
        for i in range(N):
            writedata.append([data[i][0],0,data[i][1]])
            
    elif plane == "xy": # Z is constant!
        for i in range(N):
            writedata.append([data[i][0],data[i][1],0])
            
    elif plane=="yz": # X is a constant!
        for i in range(N):
            writedata.append([0,data[i][0],data[i][1]])
        
        
    try:     
        f = open(fname1,'w')
        print("%s opened."%(fname1))
        for wd in writedata:
            writestr = "%f%s%f%s%f\n"%(wd[0],s,wd[1],s,wd[2])
            f.write(writestr)
        f.close()
        print("%s closed."%(fname1))
    except IOError:
        print("< ERROR: File unable to be opened.")
        return False
        

    return True


# This function exports Data in a certain plane, to fname1 and fname2. 
def ExportToFile(Data,plane,fname1, fname2,s):
    
    COUNTER = 1
   
    for data in Data: # Going across Data_Upper and Data_Lower
    
        N = len(data[0])
    
        writedata = []
        if plane == "xz": # Y is constant!
            for i in range(N):
                writedata.append([data[0][i],0,data[1][i]])
        
        elif plane == "xy": # Z is constant!
            for i in range(N):
                writedata.append([data[0][i],data[1][i],0])
                
        elif plane == "yz": # X is constant!
            for i in range(N):
                writedata.append([0,data[0][i],data[1][i]])
                
        if COUNTER == 1:
            fname = fname1
        else:
            fname = fname2

        try:
            f = open(fname,'w')
            
            print("%s opened."%(fname))
            for wd in writedata:
                writestr = "%f%s%f%s%f\n"%(wd[0],s,wd[1],s,wd[2])
                f.write(writestr)
                    
            f.close()
            print("%s closed."%(fname))
            print("< Export complete.")
        
            COUNTER  += 1
            
        except IOError:
            print("< ERROR: Could not open file.")
            return False

    return True



# This function gets a yes or no input from the user.
def GetYesOrNo(prompt):
    resp = str(input(prompt))
    while resp not in ['y','n']:
        print("< ERROR: Invalid response.")
        resp = str(input(prompt))
        
    return resp


# This function waits for the user to hit enter to quit.
def EnterToContinue():
    input("< Hit enter to quit.")
    return


# This is the main execution function.
def main():
    # Parameters are m,p,c,t, plane, fname1, and fname2. 
    
    
    if os.name == 'nt':
        default_filepath = "C:\\Users\\Bear\\Desktop\\"
    elif os.name == 'posix':
        default_filepath = "/Users/ryanlittle/Desktop/"
    else:
        default_filepath = ""
    
    
    continue_running = True
    
    while continue_running:
    
        print("\n\n========================================")
        print("NACA 4 Digit Airfoil .pts file generator")
        print("========================================\n\n")
        print("Example: NACA-2412\n")
        print("\tm = 0.02.............Max Camber, 1st digit")
        print("\tp = 0.40.............Position of max camber, 2nd digit")
        print("\tt = 0.12.............Max thickness as a % of the chord length, 3rd & 4th digits")
        print("\tc = 1.00.............Chord length, usually set to 1 and scale CAD model.\n\n")
        
        print("Enter in your values of these coefficients.")
        
        try:
            m = float(input("> m = "))
            p = float(input("> p = "))
            t = float(input("> t = "))
            c = float(input("> c = "))
        except ValueError:
            print("< ERROR: Invalid input. Restarting.")
            continue
        
        print("Plane entry must be either xy, yz, or xz.")
        plane = input("> plane = ")
        
        
        print("Please enter the number of points the curve will be comprised of.")
        try:
            N = int(input("> N = "))
        except ValueError:
            print("< ERROR: Invalid input. Restarting.")
            continue
        
        
        use_default = GetYesOrNo("Use default file pathway? y/n: ")
        if use_default == 'n':
            default_filepath = input("Please enter file pathway: ")
        
        
        print("Please input the filenames for the upper coordinates\nand the lower coordinates to be saved into.\nInclude full directory pathway.")
        print("Extension should be .pts")
        fname1 = input("> Upper coords filename: ")
        fname2 = input("> Lower coords filename: ")
        
        fname1 = default_filepath + fname1
        fname2 = default_filepath + fname2
        
        X = Generate_X(N,p,c)
        Data = Get_UL(X,m,p,c,t)
        
        print("Values can be separated by space or comma.")
        separator = input("> Separator: ")
        
        if not ExportToFile(Data,plane,fname1,fname2,separator): print("< Export unsuccessful.")
        
        DoContinue = GetYesOrNo("> Run again? y/n: ")
        
        if DoContinue == 'n': continue_running = False
        
        
    EnterToContinue()
    
    return









"""

Here's where the GUI coding happens. If you do not have tkinter installed, it's best to comment this entire section out.

"""


from tkinter import *


class NACA_GUI:
    def __init__(self,master):
        self.master = master
        master.title("NACA Airfoil GUI")
        
        
        
        
        
        
        
        self.m_entry_label = Label(text="Enter value for m")
        #self.m_entry_label.pack()
        self.m_entry_label.grid(row=0,column=0)

        self.m_entry_str = StringVar()
        self.m_entry_str.set("0.05")
        
        self.m_entry = Entry(master,text=self.m_entry_str)
        #self.m_entry.pack()
        self.m_entry.grid(row=0,column=1)
        
        
        self.p_entry_label = Label(text="Enter value for p")
        #self.p_entry_label.pack()
        self.p_entry_label.grid(row=1,column=0)

        self.p_entry_str = StringVar()
        self.p_entry_str.set("0.35")
        
        self.p_entry = Entry(master,text=self.p_entry_str)
        #self.p_entry.pack()
        self.p_entry.grid(row=1,column=1)
        
        
        self.c_entry_label = Label(text="Enter value for c")
        #self.c_entry_label.pack()
        self.c_entry_label.grid(row=2,column=0)

        self.c_entry_str = StringVar()
        self.c_entry_str.set("1.00")
        
        self.c_entry = Entry(master,text=self.c_entry_str)
        #self.c_entry.pack()
        self.c_entry.grid(row=2,column=1)
        
        
        self.t_entry_label = Label(text="Enter value for t")
        #self.t_entry_label.pack()
        self.t_entry_label.grid(row=3,column=0)

        self.t_entry_str = StringVar()
        self.t_entry_str.set("0.15")
        
        self.t_entry = Entry(master,text=self.t_entry_str)
        #self.t_entry.pack()
        self.t_entry.grid(row=3,column=1)
        
        self.xstep_entry_label = Label(text="# of points")
        #self.xstep_entry_label.pack()
        self.xstep_entry_label.grid(row=4,column=0)

        self.xstep_entry_str = StringVar()
        self.xstep_entry_str.set("200")
        
        self.xstep_entry = Entry(master,text=self.xstep_entry_str)
        #self.xstep_entry.pack()
        self.xstep_entry.grid(row=4,column=1)
        
        
        
        
        self.plane_entry_label = Label(text="Plane for curve")
        #self.plane_entry_label.pack()
        self.plane_entry_label.grid(row=5,column=0)

        self.plane_entry_str = StringVar()
        self.plane_entry_str.set("xz")
        
        self.plane_entry = Entry(master,text=self.plane_entry_str)
        #self.plane_entry.pack()
        self.plane_entry.grid(row=5,column=1)
        
        
        if os.name == 'nt':
            default_filepath = "C:\\Users\\Bear\\Desktop\\"
        elif os.name == 'posix':
            default_filepath = "/Users/ryanlittle/Desktop/"
        else:
            default_filepath = ""
        
  
        self.filepath_entry_label = Label(text="File path")
        self.filepath_entry_label.grid(row=6,column=0)
    
        self.filepath_entry_str = StringVar()
        self.filepath_entry_str.set(default_filepath)
        self.filepath_entry = Entry(master, text=self.filepath_entry_str)
        self.filepath_entry.grid(row=6,column=1)
        
        
        self.fname1_entry_label = Label(text="Filename for top datapoints")
        #self.fname1_entry_label.pack()
        self.fname1_entry_label.grid(row=7,column=0)

        self.fname1_entry_str = StringVar()
        self.fname1_entry_str.set(default_fname1)
        
        self.fname1_entry = Entry(master,text=self.fname1_entry_str)
        #self.fname1_entry.pack()
        self.fname1_entry.grid(row=7,column=1)
        
        
        self.fname2_entry_label = Label(text="Filename for bottom datapoints")
        #self.fname2_entry_label.pack()
        self.fname2_entry_label.grid(row=8,column=0)

        self.fname2_entry_str = StringVar()
        self.fname2_entry_str.set(default_fname2)
        
        self.fname2_entry = Entry(master,text=self.fname2_entry_str)
        #self.fname2_entry.pack()
        self.fname2_entry.grid(row=8,column=1)
        
        
        
        
        
        
        """
        self.usedefaultpath_checkvar = IntVar()
        self.usedefaultpath_checkvar.set(1)
        self.usedefaultpath_cb = Checkbutton(master, text="Use default filepath", variable=self.usedefaultpath_checkvar, onvalue=1, offvalue=0)
        self.usedefaultpath_cb.grid(row=8,column=1)
        """
        
        self.separation_var = StringVar()
        self.separation_var.set(" ")
        self.ssv_rb = Radiobutton(master,text="Space Separated", var=self.separation_var, value=" ")
        self.ssv_rb.grid(row=9,column=0)
        
        self.csv_rb = Radiobutton(master,text="Comma separated", var=self.separation_var, value=",")
        self.csv_rb.grid(row=9,column=1)
        
        
        
        self.plotbutton = Button(master, text="Plot", command=self.PlotButton)
        #self.plotbutton.pack()
        self.plotbutton.grid(row=10,column=0)
        
        
        
        self.exportbutton = Button(master, text="Export points", command=self.ExportButton)
        #self.exportbutton.pack()
        #)
        self.exportbutton.grid(row=11,column=0)
        
        
        
        self.combinedexport_checkvar = IntVar()
        self.combinedexport_checkvar.set(0)
        self.combinedexport_cb = Checkbutton(master, text="Combined Data File", variable= self.combinedexport_checkvar, onvalue = 1, offvalue = 0)
        self.combinedexport_cb.grid(row=11,column=1)
        
        
        
        self.f = Figure(figsize=(10,2), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.grid()
        

        
        self.canvas = FigureCanvasTkAgg(self.f, master=master)
        self.canvas.show()
        self.canvas._tkcanvas.grid(row=0,column=2,rowspan=9, columnspan=11)
        
        
     
        
    def PlotButton(self):
        
        try:
            m = float(self.m_entry_str.get())
            p = float(self.p_entry_str.get())
            c = float(self.c_entry_str.get())
            t = float(self.t_entry_str.get())
            
            npoints = float(self.xstep_entry_str.get())
            
            plane = self.plane_entry_str.get()
            fname1 = self.fname1_entry_str.get()
            fname2 = self.fname2_entry_str.get()
            
            
            X = Generate_X(npoints,p,c)
            Data = Get_UL(X,m,p,c,t)
            
            D_up, D_dn = Data[0], Data[1]
            
            
            self.a.clear()
            self.a.grid()
    
            self.a.plot(D_up[0],D_up[1], 'r')
            #plt.hold()
            self.a.plot(D_dn[0],D_dn[1], 'b')
            
            self.canvas.show()
            
            print("Airfoil successfully plotted.")
            
        except ValueError:
            print("ERROR: Invalid value for parameter. Airfoil not plotted.")
        
        
        return


    def ExportButton(self):
        
        try:
            m = float(self.m_entry_str.get())
            p = float(self.p_entry_str.get())
            c = float(self.c_entry_str.get())
            t = float(self.t_entry_str.get())
            
            xstep = float(self.xstep_entry_str.get())
            
            plane = self.plane_entry_str.get()
            
            fname1 =  self.filepath_entry.get() + self.fname1_entry_str.get()
            fname2 = self.filepath_entry.get() + self.fname2_entry_str.get()
            
            
            
            X = Generate_X(xstep,p,c)
            Data = Get_UL(X,m,p,c,t)
            
            
            print(np.shape(Data[0]), np.shape(Data[1]))
            
            s = self.separation_var.get()
            
            
            if  not self.combinedexport_checkvar.get():
                ExportToFile(Data,plane,fname1,fname2,s)
            else:
                ExportToFile_Combined(Data,plane,fname1,fname2,s)
                
            print("%s, %s export successful."%(fname1,fname2))
            
            
        except ValueError:
            print("ERROR: Invalid value for parameter. Coordinates not exported.")
            
        
        return







""" Running Block (Leave this uncommented!)"""
if USE_GUI:
    root = Tk()
    my_gui = NACA_GUI(root)
    root.mainloop()
else:
    main()










