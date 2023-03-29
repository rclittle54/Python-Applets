#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 16:17:32 2017

Tkinter Test


@author: ryanlittle
"""
from tkinter import Entry, W, StringVar, Button, Label, Tk
import matplotlib.pyplot as plt
from numpy import arange, sin, cos, pi, arctan

# Valar MohrGUI-is
class MohrGUI:
    def __init__(self, master):
        self.master = master
        master.title("Mohr's Circle")
        
        # Adding sig_xx text label
        self.sig_xx_label = Label(master, text="Normal Stress in X")
        self.sig_xx_label.grid(columnspan=2, sticky=W)
        
        # Adding sig_xx text entry
        self.sig_xx_entry_str = StringVar()
        self.sig_xx_entry_str.set("0")
        self.sig_xx_entry = Entry(master, textvar=self.sig_xx_entry_str)
        self.sig_xx_entry.grid(row=1, sticky=W)
        
        # Adding sig_yy text label
        self.sig_yy_label = Label(master, text="Normal Stress in Y")
        self.sig_yy_label.grid(row=2, sticky=W)
        
        # Adding sig_yy text entry
        self.sig_yy_entry_str = StringVar()
        self.sig_yy_entry_str.set("0")
        self.sig_yy_entry = Entry(master, textvar=self.sig_yy_entry_str)
        self.sig_yy_entry.grid(row=3, sticky=W)
        
        # Adding sig_xy text label
        self.sig_xy_label = Label(master, text="Shear Stress XY")
        self.sig_xy_label.grid(row=4, sticky=W)
        
        # Adding sig_xy text entry
        self.sig_xy_entry_str = StringVar()
        self.sig_xy_entry_str.set("0")
        self.sig_xy_entry = Entry(master,textvar=self.sig_xy_entry_str)
        self.sig_xy_entry.grid(row=5, sticky=W)
        
        # Adding rot_angle text label
        self.rot_angle_label = Label(master, text="Rotation Angle")
        self.rot_angle_label.grid(row=6, sticky=W)
        
        # Adding rot_angle text entry
        self.rot_angle_entry_str = StringVar()
        self.rot_angle_entry_str.set("0")
        self.rot_angle_entry = Entry(master,textvar=self.rot_angle_entry_str)
        self.rot_angle_entry.grid(row=7, sticky=W)
        
        
        # Adding run button
        self.run_button = Button(master,text="Run", command=self.run_mohrs)
        self.run_button.grid(row=10)
        
        
    # Function to get 'coordinates' of A' and B', given A, B, and rot angle theta
    def Get_A1_B1(self,A,B,theta):
        x_m = 0.5*(A[0]+B[0])
        r = (((A[0]-B[0])/(2))**2 + (B[1])**2)**0.5
        
        dx = A[0]-x_m
        dy = A[1]
        
        # Avoiding float division by zero
        if dx == 0:
            if dy > 0:
                theta0 = pi/2
            else:
                theta0 = -pi/2
        else:
            theta0 = arctan(dy/dx)
            
        thetaf = theta0 + theta
        
        # Calculating polar-wise from average sigma_ii
        A1 = [x_m+r*cos(thetaf),r*sin(thetaf)]
        B1 = [x_m+r*cos(thetaf+pi),r*sin(thetaf+pi)]
        
        return [A1,B1]
        
    # Function to get the maximum normal and shear stress values
    def Get_Max_Stress(self,A,B):
        x_m = 0.5*(A[0]+B[0])
        r = (((A[0]-B[0])/(2))**2 + (B[1])**2)**0.5
        
        # Simply the rightmost and topmost points of the Circle
        sig_max = [x_m+r,0]
        tau_max = [x_m,r]
        
        return [sig_max, tau_max]
    
    
    # Function to get the principal angles of stress, given A and B
    def Get_Principal_Angles(self,A,B):
        x_m = 0.5*(A[0]+B[0])
        r = (((A[0]-B[0])/(2))**2 + (B[1])**2)**0.5
        
        
        dx = A[0]-x_m
        dy = A[1]
        
        # Avoiding float division by zero
        if dx == 0:
            if dy > 0:
                theta0 = pi/2
            else:
                theta0 = -pi/2
        else:
            theta0 = arctan(dy/dx)
           
        # Converting to degrees    
        two_theta_p = theta0 * 180/pi
        two_theta_s = two_theta_p + 90
        
        return [two_theta_p, two_theta_s]
    
    # Plots the Mohr's Circle
    def plot_d(self,stress,theta):
        
        # Gets A and B from stress tensor
        A = [stress[0],stress[1]]
        B = [stress[3],stress[2]]
        
        # Calculates average normal stress, and radius
        x_m = 0.5*(A[0]+B[0])
        r = (((A[0]-B[0])/(2))**2 + (B[1])**2)**0.5
        
        
        
       
        # Visual constants
        axlim = 1.125
        annosize = 12
        
        # Creates circle
        circle = plt.Circle((x_m,0), r, color='k', fill=False)
        
        # Creates axis to plot on
        ax = plt.gca()
        ax.cla()
        ax.set_title("Mohr's Circle",size=16, weight='bold')
        ax.set_xlabel(r'$\sigma_{i i}$', size=14)
        ax.set_ylabel(r'$\tau_{i j}$', rotation=0, size=14)
        ax.set_xlim((x_m-axlim*r, x_m+axlim*r))
        ax.set_ylim((-axlim*r, axlim*r))
        ax.grid()
        
        # Plot the circle itself
        ax.add_artist(circle)
        
        # Plot the points A and B
        ax.plot(A[0],A[1],'ro')
        ax.annotate('A', xy=A, size=annosize)
        ax.plot(B[0],B[1],'bo')
        ax.annotate('B', xy=B, size=annosize)
        
        # Plot the line between A and B
        ax.plot([A[0],B[0]],[A[1],B[1]], 'k--', linewidth=0.5)
        
        # Gets A' and B' from function
        d1 = self.Get_A1_B1(A,B,theta)
        A1, B1 = d1[0], d1[1]
        
        # Adds A' and B' to plot
        ax.plot(A1[0],A1[1],'r^')
        ax.annotate("A'", xy=A1, size=annosize)
        ax.plot(B1[0],B1[1],'b^')
        ax.annotate("B'", xy=B1, size=annosize)
        ax.plot([A1[0],B1[0]],[A1[1],B1[1]], 'k--', linewidth=0.5)
        
        # Gets maximum stresses from function
        d2 = self.Get_Max_Stress(A,B)
        sig_max, tau_max = d2[0], d2[1]
        
        # Adds sig_max and tau_max to plot
        ax.plot(sig_max[0], sig_max[1], 'g*')
        ax.annotate(r'$\sigma_{max}$', xy=sig_max, size=annosize)
        ax.plot(tau_max[0], tau_max[1], 'g*')
        ax.annotate(r'$\tau_{max}$', xy=tau_max, size=annosize)
        
        
        
        
        
        
    # What happens when you hit the run button
    def run_mohrs(self):
        #print(">>> Running")
        
        # Get stress values from text entry fields
        sig_xx = float(self.sig_xx_entry.get())
        sig_xy = float(self.sig_xy_entry.get())
        sig_yy = float(self.sig_yy_entry.get())
        
        # Combine them into one stress tensor
        stress = [sig_xx, -sig_xy, sig_xy, sig_yy]
        
        # Get rotation angle from text entry field
        theta = float(self.rot_angle_entry.get()) 
        
        # Convert to radians
        theta *= pi/180
        
        # Separate tensor into A and B
        A = [stress[0],stress[1]]
        B = [stress[3],stress[2]]
        
        # Print tensor
        print(">>> Stress Tensor (MPa):")
        print("\t%4.2f\t%4.2f\n\t%4.2f\t%4.2f\n"%(stress[0], stress[1], stress[2], stress[3]))
        
        # Plot the circle
        self.plot_d(stress,theta)
        
        # Get values for results
        
        d1 = self.Get_A1_B1(A,B,theta)
        A1, B1 = d1[0], d1[1]
        
        d2 = self.Get_Max_Stress(A,B)
        sig_max, tau_max = d2[0], d2[1]
        
        d3 = self.Get_Principal_Angles(A,B)
        two_t_p, two_t_s = d3[0], d3[1]
        
        # Print results
        
        print(">>> Sigma x'x': %4.2f\n>>> Sigma y'y': %4.2f\n>>> Sigma x'y': %4.2f\n"%(A1[0],B1[0],B1[1]))
        print(">>> Max Normal Stress: %4.2f\n>>> Max Shear Stress: %4.2f\n"%(sig_max[0],tau_max[1]))
        print(">>> 2*theta_p: %4.2f\n>>> 2*theta_s: %4.2f"%(two_t_p, two_t_s))
        


# Run the GUI
root = Tk()
my_gui = MohrGUI(root)
root.mainloop()











