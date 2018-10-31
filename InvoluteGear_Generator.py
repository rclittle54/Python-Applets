# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 19:16:07 2018

This program exports the points that define the profile for an involute spur gear.

@author: ryanlittle
"""
import matplotlib.pyplot as plt
import numpy as np




# This function exports a dataset D to the filename fname.
def exportD(D,fname):
    try:
        f = open(fname,'w')
        for p in D:
            x,y = p[0],p[1]
            writestr = "%f %f %f\n"%(x,y,0)
            f.write(writestr)
            
        f.close()
        print("File exported!")
        
    except IOError:
        print("ERROR: Invalid file name.")
        print("File NOT exported.")
        
    return
 
    


# This function, primarily for debugging, plots a circle, centered at the origin, of radius r.
def plotcircle(r,plotargs=''):
    c_r = r
    theta = np.linspace(0,2*np.pi,200)
    cx = []
    cy = []
    for t in theta:
        c_x = c_r*np.cos(t)
        c_y = c_r*np.sin(t)
        cx.append(c_x)
        cy.append(c_y)
    plt.plot(cx,cy,plotargs)
    plt.hold
    
# This function returns the radial distance from the origin of point p.
def radius(p):
    return np.sqrt(p[0]**2 + p[1]**2)

# This function returns the angle, measured counterclockwise from the +x-axis of point p.
def angle_rad(p):
    return np.arctan(p[1]/p[0])

# This function returns true if the point p has a greater angle than the given theta.
def point_outside_theta(p,theta):
    if np.abs(angle_rad(p)) > np.abs(theta): 
        return True
    else:
        return False

# This function returns the angle span that the dataset D covers.
def segment_anglespan(D):
    return np.abs(angle_rad(D[0])-angle_rad(D[-1]))

# This function returns the linear distance between p1 and p2.
def lindist(p1,p2):
    x1,y1 = p1[0],p1[1]
    x2,y2 = p2[0],p2[1]
    
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)










# This function returns the index of the list X, with the value closest to V.
def I_Closest_To_Value(X,V):
    mins = []
    for x in X:
        mins.append(np.abs(x-V))
    m = min(mins)
    m_i = mins.index(m)
    return m_i
    



# This function returns the intersection of D and a circle of radius R
def D_Intersect_At_R(D,R):
    point_radii = [radius(p) for p in D]
    min_d_index = I_Closest_To_Value(point_radii,R)
    pA = D[min_d_index]
    
    if radius(pA)-R < 0:
        p1 = D[min_d_index]
        p2 = D[min_d_index+1]
    else:
        p1 = D[min_d_index-1]
        p2 = D[min_d_index]
    
    R1 = radius(p1)
    R2 = radius(p2)
    x1,y1 = p1[0],p1[1]
    x2,y2 = p2[0],p2[1]
    t = (R-R1)/(R2-R1)
    
    x_out = x1+(x2-x1)*t
    y_out = y1+(y2-y1)*t
    
    return [x_out,y_out]










    

# This function mirrors the point p about the line drawn at angle theta from the origin.
def mirror_point(p,theta):
    #m = np.tan(np.deg2rad(theta))
    m = np.tan(theta)
    c = 0
    # y = mx + c
    x1, y1 = p[0], p[1]
    d = (x1+(y1-c)*m)/(1+m**2)
    x2 = 2*d - x1
    y2 = 2*d*m - y1 + 2*c
    return (x2,y2)


# This function returns a new point P, having added the angle dtheta to it. 
def rotate_point(p,dtheta):
    x,y = p[0],p[1]
    r = np.sqrt(x**2 + y**2)
    theta = angle_rad(p)
    nt = theta + dtheta
    nx,ny = r*np.cos(nt), r*np.sin(nt)
    return ((nx,ny))
    
    
    




# Creates an involute curve between r0 and rf, at an angle offset a0.
def involute_segment(r0,rf,a0,orientation='ccw'):
    dt = 0.03
    DATA = []
    t = 0
    delta = -1
    
    if orientation=='ccw':
        s = 1
    else:
        s = -1
    
    while delta <= 0:
        x = r0*(np.cos(a0+t) + t*np.sin(a0+t))
        y = s*r0*(np.sin(a0+t) - t*np.cos(a0+t))
        current_r = np.sqrt(x**2 + y**2)
        delta = current_r - rf
        DATA.append((x,y))
        
        if delta > 0:
            DATA = DATA[:-1]
        
        t += dt
        
    return DATA



# This function returns the dataset for a fillet segment.
def fillet_segment(Rb,Rd,a0,direction='cw',startin=True):
    
    NUMPOINTS = 15
    
    if direction == 'cw':
        tf0, tff = a0+np.pi/2, a0+np.pi
    elif direction == 'ccw':
        tf0, tff = a0+np.pi, a0 + 3*np.pi/2
    x0,y0 = Rb*np.cos(a0), Rb*np.sin(a0)
    r_f = Rb-Rd
    ai = a0-np.pi/2
    
    xi = r_f*np.cos(ai)+x0
    yi = r_f*np.sin(ai)+y0
    
    
    DATA = []
    
    # Reverse theta_f0 and theta_ff
    if startin:
        theta_f0, theta_ff = tff, tf0
    else:
        theta_f0, theta_ff = tf0, tff
    
    T = np.linspace(theta_f0,theta_ff,NUMPOINTS)
    for t in T:
        x = r_f*np.cos(t)+xi
        y = r_f*np.sin(t)+yi
        DATA.append((x,y))
    
    return DATA
    



# This function returns the dataset for a circumferential segment.
def circumfrence_segment(r,t0,tf,direction='ccw'):
    T = np.linspace(t0,tf,10)
    if direction == 'cw':
        T = np.linspace(tf,t0,20)
    
    DATA = []
    for t in T:
        x = r*np.cos(t)
        y = r*np.sin(t)
        DATA.append((x,y))
    return DATA



# This function checks the distances between points for every point in dataset D.
# If any distance is 0, it will let the user know, and possibly plot it according to DOPLOT.
def Analyze_Distances(D,DOPLOT):
    dists = []
    for d in D[:-1]:
        i = D.index(d)
        d_up = D[i+1]
        dist_up = lindist(d,d_up)
        dists.append(dist_up)
        
    print("Minimum distance between points is:")
    mindist = min(dists)
    min_i = dists.index(mindist)
    print("Min: %f, at i=%d"%(mindist,min_i))
    print("Plotting.")
    
    if mindist == 0:
        print("WARNING WARNING WARNING")
    
    badpoint = D[min_i]
    if DOPLOT: plt.plot(badpoint[0],badpoint[1],'r+',markersize=20)
    
    return
        
        
# This function returns the dataset defining the involute spur gear profile given N, P, and alpha.
def Gear(N,P,alpha):
    # N = Number of teeth
    # P = Pitch
    # alpha = Pressure angle, probably 14.5 or 20
    alpha = np.deg2rad(alpha) # Convert to radians to make life easier
    D = N/P # Diameter of pitch circle
    D_B = D*np.cos(alpha) # Diameter of the base circle
    #a = 1/P # Addendum
    #b = 1.25/P # Dedendum
    D_O = (N+2)/P # Outside diameter
    D_R = (N-2.5)/P # Innermost diameter
    # Note: The following two parameters are NOT ANGLESPANS
    t = 1.5708/P # Circular thickness of the tooth. This is an arc.
    p = np.pi/P # Circular pitch, this is the distance of equivalent points along the 'wave.' This is also an arc. 
    
    # Converting to radius for dedendum, base, pitch, and addendum
    Rd = D_R/2
    Rb = D_B/2
    Rp = D/2
    Ra = D_O/2
    
    # Establishing the centerline angle for each tooth profile
    available_anglespan = 2*np.pi/N # We have 2pi/Nteeth radians available for each tooth.
    centerline_angles = np.linspace(0,2*np.pi,N+1) # Establish angles to create each tooth on
    centerline_angles = centerline_angles[:-1] # Remove the last one to not create a duplicate at 0 radians
    
    # Creating dummy geometry to determine anglespan constants and pitch-arcs.
    # For the involute segment:
    dummy_inv = involute_segment(Rb,Ra,0) # Creating an unused involute segment.
    inv_anglespan = segment_anglespan(dummy_inv) # Determing anglespan.
    inv_pitch_arc = inv_anglespan*Rp # Pitch arc length is the anglespan * pitch radius
    
    inv_pitch_point = D_Intersect_At_R(dummy_inv,Rp) # Calculates the point the involute intersects the pitch circle
    mid_theta = angle_rad(inv_pitch_point) # Angle of the pitch point
    end_theta = angle_rad(dummy_inv[-1]) # Angle of the last point of the involute
    inv_outer_anglespan = end_theta-mid_theta # The anglespan is the difference between the two
    inv_outer_pitch_arc = inv_outer_anglespan*Rp # The pitch arc is the anglespan * the pitch radius
    
    # For the outer circumfrential segment:
    co_pitch_arc = (t/2) - inv_outer_pitch_arc
    co_anglespan = co_pitch_arc/Rp # anglespan * Rp = arc -> anglespan = arc/Rp
    
    # For the fillet segment:
    dummy_fillet = fillet_segment(Rb,Rd,0)
    fillet_anglespan = segment_anglespan(dummy_fillet)
    fillet_pitch_arc = fillet_anglespan*Rp
    
    # For the inner circumfrential segment:
    ci_pitch_arc = (p/2) - co_pitch_arc - inv_pitch_arc - fillet_pitch_arc
    ci_anglespan = ci_pitch_arc/Rp
    
    
    
    
    
    # Creating the first tooth, to be rotated later:
    # Inner circumfrential segment
    ci_theta0 = 0 - available_anglespan/2 # Centered initially about 0, with the anglespan splitting the 0
    ci_thetaf = ci_theta0 + ci_anglespan # Initial angle + the span
    ci = circumfrence_segment(Rd,ci_theta0,ci_thetaf) # Creating D for inner circumfrential segment
    
    # Fillet segment:
    f_a0 = ci_thetaf + fillet_anglespan # Initial angle for the fillet's positioning
    f_af = ci_thetaf + fillet_anglespan # Determining final angle
    f = fillet_segment(Rb,Rd,f_a0) # Creating D for fillet segment
    f = f[:-1] # Removing the final element of D, to avoid overlapping points
    
    # Iterating the fillet to remove chunks outside the good zones
    while point_outside_theta(f[0],available_anglespan/2):
        #print(angle_rad(f[0]))
        #print("Snipping!")
        f = f[1:]
    
    # Involute segment:
    inv = involute_segment(Rb,Ra,f_af) # Creating D for involute segment
    #inv_thetaf = f_af + inv_anglespan # Determining final angle of the involute segment
    
    # Outer circumfrential segment:
    co_theta0 = 0 - co_anglespan # It will be ending at the 0 radian line
    co = circumfrence_segment(Ra,co_theta0,0)
    co = co[4:] # Excluding the first 2 elements of D to smooth out the tooth.
    
    
    
    
    
    # Creating the total D for the initial tooth:
    D_bot = ci + f + inv + co # D for the clockwise, 'bottom' segment
    D_bot = f + inv + co
    D_top = [mirror_point(p,0) for p in D_bot] # D for the ccw, 'top' segment, by mirroring the points
    D_top.reverse() # Reverse the points to ensure continuity
    D_top = D_top[1:] # Ignore the first element to avoid overlapping points
    
    
    
    
    
    D_init = D_bot + D_top # Total initial D is the sum of both D's
    D_init = D_init[1:-1] # Ignore the first and last point to avoid overlapping points
    
    
    # Creating D_total, by rotating each point in D_init by the centerline_angles:
    D_tot = []
    for theta in centerline_angles:
        D_rotated = [rotate_point(x,theta) for x in D_init] # Rotate each point by theta
        D_tot += D_rotated # Add the rotated D to the final D
    
    return D_tot
    

# This function plots the dataset D.
def plotD(D,plotargs=''):
    x = [i[0] for i in D]
    y = [i[1] for i in D]
    plt.plot(x,y,plotargs)
    plt.grid()
    







# This function serves to get a yes or no response.
def GetYesOrNo(prompt):
    resp = str(input(prompt))
    while resp not in ['y','n']:
        print(">>> ERROR: Invalid response.")
        resp = str(input(prompt))
        
    return resp





# This is the main execution function.
def main():

    cont = 'y'
    
    while cont != 'n':
    
        N = input("# Teeth: ")
        P = input("Pitch: ")
        alpha = input("Pressure angle: ")
        
        try:
            N = int(N)
            P = float(P)
            alpha = float(alpha)
        except ValueError:
            print("ERROR: Invalid value for one or more parameters.")
            continue
        D = Gear(N,P,alpha)
        plt.figure(figsize=(6,6))
        plotD(D)
        
        
        doexport = GetYesOrNo("Export to file? y/n: ")
        if doexport == 'y':
            userfname = input("Filepath and name: ")
            exportD(D,userfname)
        else:
            print("Not exporting.")
            
        cont = GetYesOrNo("Run again? y/n: ")
        

    return



if __name__ == '__main__':
    main()























