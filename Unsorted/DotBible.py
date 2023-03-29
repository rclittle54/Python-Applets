
import math, sys
from math import *

dotslist = []
cont = "y"

n = 1
while cont == "y":
	print("Dot #", n, ": ")
	stepsfromline = input("How many steps from the yardline are you? (only the number part) ")
	stepsfromline = float(stepsfromline)
	inorout = input("Inside or outside? (in / out) ")
	yardline = input("From which yardline? ")
	yardline = int(yardline)
	side = input("Which side? (1 / 2) ")
	fronttoback = input("What's your front to back? (number value) ")
	fronttoback = float(fronttoback)
	fob = input("Front or behind? (f / b) ? ")
	freference = input("From which reference? (bsl, bh, fh, fsl) ")
	numsteps = "-"
	tempo = "-"
	if n != 1:
		numsteps = int(input("How many steps do you so this in? "))
		tempo = float(input("What tempo are your feet moving "))


	firstdot = [stepsfromline, inorout, yardline, side, fronttoback, fob, freference, numsteps, tempo]
	dotslist.append(firstdot)
	n = n + 1
	print(firstdot)
	cont = input("Add another set? (y/n) ")
	print("=" * 40)


# dotslist[n][v]
# (n+1) is each set
# v is indices of each set

#Dot index:         0: Steps from the line
#                   1: in/out
#                   2: Yardline
#                   3: Side
#                   4: Front to back
#                   5: Front of or behind
#                   6: Front to back reference

# ===== / =====


ydlists1 = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

ydlists2 = [50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 0]

ftbdict = {'bsl': 0, 'bh': 32, 'fh': 52, 'fsl': 84}

def dottocoord(dot):
	dot1xcoord = 0.0
	if dot[3] == "1":
		if dot[1] == "in":
			dot1xcoord = ((ydlists1.index(dot[2]))*8) + dot[0]
		elif dot[1] == "out":
			dot1xcoord = ((ydlists1.index(dot[2]))*8) - dot[0]
	elif dot[3] == "2":
		if dot[1] == "in":
			dot1xcoord = (80 + (ydlists2.index(dot[2]))*8) - dot[0]
		elif dot[1] == "out":
			dot1xcoord = (80 + (ydlists2.index(dot[2]))*8) + dot[0]

	dot1ycoord = 0.0
	if dot[5] == "f":
		dot1ycoord = ftbdict[dot[6]] + dot[4]
	elif dot[5] == "b":
		dot1ycoord = ftbdict[dot[6]] - dot[4]

	return (dot1xcoord, dot1ycoord)

def vectorcalc(dot1, dot2):
	return ((dot2[0]-dot1[0]), (dot2[1]-dot1[1]))


def vectorlength(v):
	return ((v[0]**2)+(v[1]**2))**0.5

def todegrees(angle):
	return angle*(180/pi)

def vectorangle(v):
	if v[0] != 0:
		return todegrees(atan((v[1])/v[0]))
	else:
		return 90

def vectormult(v, s):
	return (v[0]*s, v[1]*s)


def dotplusvector(dot, v):
	return ((dot[0]+v[0]),(dot[1]+v[1]))





def subvectorcalc(dot, vector, numsteps):
	stepcoordlist = []
	for n in range(0, numsteps+1):
		stepcoordlist.append((((n*vector[0]/numsteps)+dot[0]), ((n*vector[1]/numsteps)+dot[1])))
	return stepcoordlist


def coordtodot(x, y):
	outdot = []
	x -= 80
	if x < 0:
		side = 1
	elif x > 0:
		side = 2
	else:
		side = "-"
	x = math.fabs(x)
	x_yards = 50 - (x * 5.0/8.0)
	yd = int((math.floor(x_yards / 5.0))*5.0)
	yd_offset = x_yards-yd
	if yd_offset > 2.5:
		yd += 5
		yd_offset -= 5
	# OLD -- xr = math.fabs(yd_offset*(8.0/5.0))
	xr = yd_offset*(8.0/5.0)
	if xr == 0:
		x_io = "on"
	if xr > 0:
		x_io = "in"
	elif xr < 0:
		x_io = "out"
	xr = math.fabs(xr)


	print("\t", end=' ')
	if x_io == "in" and yd == 50:
		x_io = "out"
	if xr != 0:
		print(xr, x_io, yd, "Side ", side)
		outdot.append(xr)
		outdot.append(x_io)
		outdot.append(yd)
		outdot.append(side)
	else:
		print("on", yd, "Side", side)
		outdot.append(xr)
		outdot.append("in")
		outdot.append(yd)
		outdot.append(side)
		outdot.append("-")
		outdot.append("-")

	yfob = ""
	y_off = 9999
	for k, v in ftbdict.items():
		if abs(y-v) < abs(y_off):
			y_off = y-v
			yref = k
	if y_off < 0: yfob = "b"
	elif y_off > 0: yfob = "f"
	else: yfob = "on"
	y_off = abs(y_off)
	print("\t", y_off, yfob, yref)
	outdot.append(y_off)
	outdot.append(yfob)
	outdot.append(yref)
	return outdot


def subset(dot1, dot2, ratio):
	dot1 = dottocoord(dot1)
	dot2 = dottocoord(dot2)
	v = vectorcalc(dot1, dot2)
	v = vectormult(v, ratio)
	sub = dotplusvector(dot1, v)
	coordtodot(sub[0], sub[1])




totalcoordslist = []
for dot in dotslist:
	if dotslist.index(dot) < len(dotslist)-1:
		dot1 = dot
		dot2 = dotslist[(dotslist.index(dot1))+1]
		dot1num = dotslist.index(dot1)+1
		dot2num = dotslist.index(dot2)+1
		numsteps = dot2[7]
		dot1 = dottocoord(dot1)
		dot2 = dottocoord(dot2)
		vector = vectorcalc(dot1, dot2)
		lengthofdrill = vectorlength(vector)
		substeps = subvectorcalc(dot1, vector, numsteps)
		totalcoordslist.append(substeps)


		print("            From dot #", dot1num, " to dot #", dot2num, ": ")

		standardratio = float(lengthofdrill / numsteps)
		print(standardratio, "times an 8 to 5 step")
		inchesperstep = standardratio*22.5
		print(inchesperstep, "inches per step.")
		ntofive = float(8.0 / standardratio)
		print(ntofive, "to five step.")
		if ntofive < 4.8:
			print("You should probably jazz run this.")

		mileslength = lengthofdrill*(0.000355113636)

		minutestime = float(numsteps/tempo)
		hourstime = minutestime/60.0

		speed = mileslength/hourstime

		print(speed, "mph.")


		print("Vector: ", vector)
		angle = vectorangle(vector)
		if vector[0] < 0:
			angle = -angle
		print(angle, "degrees")
		for n in substeps:
			a = ""
			if substeps.index(n) == len(substeps)/2:
				a = "\t\t\t-- Midset --"
			print("\nStep #", substeps.index(n), ": ", a)
			coordtodot(n[0], n[1])




		print("=" * 40)

#print "Function List: dottocoord(dot) coordtodot(x,y) vectorlength(v), vectorcalc(dot1, dot2), vectormultiplier(dot, vector, scalar)"
functionsprinter = ["dottocoord(dot)","coordtodot(x,y)","vectorlength(v)","vectorcalc(dot1,dot2)","vectormultiplier(dot,vector,scalar)"]

print("Functions List: ")
for n in functionsprinter:
	print("\t",n)

