from phue_source import Bridge
from RGBtoHSV import *
import time
import ui
import dialogs
import appex



b = Bridge('192.168.86.103')

item_color = '#e1e1e1'


b.connect()
	
all_lights = b.lights
kitchen = []
living_room = []
bedroom = []

buttons = []
b_sliders = []
c_sliders = []


lit_lights = []


for l in all_lights:
	#print(l.name)
	lit_lights.append(l.on)
	if l.name[0] in ['L','S']:
		living_room.append(l)
	elif l.name[0] == 'K':
		kitchen.append(l)
	else:
		bedroom.append(l)


		
alls2 = []
for l in kitchen:
	alls2.append(l)
for l in living_room:
	alls2.append(l)
for l in bedroom:
	alls2.append(l)
all_lights = alls2
	
	



def ToggleOn(l):
	if l.on:
		l.on = False
	else:
		l.on = True


def LightsCheck(lights):
	for l in lights:
		print(l.name)
		ToggleOn(l)
		time.sleep(0.75)
		ToggleOn(l)
		
#LightsCheck(all_lights)

def Button_Light_Toggle(sender):
	lname = sender.title	
	for l in all_lights:
		if l.name == lname:
			ToggleOn(l)




def Light_On_Texture(l):
	if l.on:
		return 'iow:ios7_lightbulb_32'
	else:
		return 'iow:ios7_lightbulb_outline_32'



def Switch_Handler(sender):
	name = sender.title
	for l in all_lights:
		if l.name == name:
			ToggleOn(l)
			sender.image = ui.Image(Light_On_Texture(l))


def MasterSwitch(sender):
	switches = sender.superview.subviews
	
	for l in all_lights:
		l.on = sender.value
		time.sleep(0.2)
		switches[all_lights.index(l)].image = ui.Image(Light_On_Texture(l))



def Slider_Handler(sender):
	n = b_sliders.index(sender)
	all_lights[n].brightness = int(254*sender.value)

	
def Color_Handler(sender):
	n = c_sliders.index(sender)
	all_lights[n].hue = int(65535*sender.value)	
	
def Room_Toggle(sender):
	room = []
	if sender.title == 'KC':
		room = kitchen
	elif sender.title == 'LR':
		room = living_room
	elif sender.title == 'BR':
		room = bedroom
	
	#print(room)
	
	turn_on = True	
	for l in room:
		if l.on:
			turn_on = False
			break
	
			
	for l in room:
		if turn_on:
			l.on = True
		else:
			l.on = False
		sender.image = ui.Image(Light_On_Texture(l))	
		
	
	
def Create_Room_Button(v,l,label,a,x,y,m):
	n_lights = a
	lname = ''
	if l[0] in kitchen:
		lname = 'KC'
	elif l[0] in living_room:
		lname = 'LR'
	elif l[0] in bedroom:
		lname = 'BR'
	

	n = 0
	for a in l:
		if a.on:
			n = l.index(a)
			break
	
	button = ui.Button(image = ui.Image(Light_On_Texture(l[n])))
	button.title = lname
	button.action = Room_Toggle
	button.image = ui.Image(Light_On_Texture(l[n]))
	button.tint_color = '#ffffff'
	
	button.center = ((x/2)-3*label.width,(y/2)+(n_lights/2)-m*40)
	
	v.add_subview(button)
			
				
		
	

n_lights = len(all_lights)
	


view = ui.View()
view.name = 'PHue'
#view.background_color = '#5c8cab'
view.background_color = '#2e5167'

#item_color = '#e1e1e1'



ssize = ui.get_window_size()
x = ssize[0]
y = ssize[1]

pic = ui.ImageView()
pic.image = ui.Image('iow:lightbulb_256')
pic.center = (x/2,70)
view.add_subview(pic)




a = 0
print('LOADING:')
for n in range(n_lights):
	
	print('\t%i: '%n,end="")
	label = ui.Label()
	label.text=all_lights[n].name
	label.text_color = item_color
	print(label.text,end="\t")
	if n < 7:
		print('',end="\t")
	elif n == 8:
		print('',end="\t")
	
	#label.center = ((x/2)-2*label.width,(y/2)+(n_lights/2)-n*40)
	(lcx,lcy) = ((x/2)-2*label.width,(y/2)+(n_lights/2)-n*40)
	label.center = (lcx,lcy)
	#label.flex = ''
	
	view.add_subview(label)
	print('.',end="")
	
	
	button = ui.Button(image = ui.Image(Light_On_Texture(all_lights[n])))
	button.title = all_lights[n].name
	button.action = Switch_Handler
	#button.image = ui.Image(Light_On_Texture(all_lights[n]))
	#print(button.image)
	button.tint_color = item_color
	
	button.center = ((x/2)-1*label.width,(y/2)+(n_lights/2)-n*40)
	
	view.add_subview(button)
	buttons.append(button)
	#a = -n
	print('.',end="")
	
	
	slider = ui.Slider()
	slider.title = all_lights[n].name #'brightness' + str(n)
	slider.continuous = True
	
	slider.center = ((x/2)+0*label.width,(y/2)+(n_lights/2)-n*40)
	
	slider.width = label.width
	slider.enabled = lit_lights[n]
	slider.action = Slider_Handler
	slider.value = all_lights[n].brightness/254
	slider.tint_color = item_color
	view.add_subview(slider)
	b_sliders.append(slider)
	print('.',end="")
	
	color = ui.Slider()
	color.title = all_lights[n].name
	color.continuous = True
	
	color.center = ((x/2)+1*label.width+0.05*label.width,(y/2)+(n_lights/2)-n*40)
	
	color.width = 1.5*label.width
	#color.enabled = lit_lights[n]
	color.action = Color_Handler
	color.value = all_lights[n].hue/65535
	color.tint_color = item_color
	view.add_subview(color)
	c_sliders.append(color)
	print('.',end="")
	
	
	l = all_lights[n]
	if l == kitchen[0]:
		Create_Room_Button(view,kitchen,label,n_lights,x,y,n)
	
	if l == living_room[0]:
		Create_Room_Button(view,living_room,label,n_lights,x,y,n)
	
	if l == bedroom[0]:
		Create_Room_Button(view,bedroom,label,n_lights,x,y,n)
		
	print('Done')
	
	
	
	
a = -n_lights/2
master_label = ui.Label()
master_label.text = 'Master'
master_label.alignment = ui.ALIGN_CENTER
master_label.center = ((x/2),(y/2)+(n_lights/2)-a*40)
a += 1
master_label.text_color = item_color
view.add_subview(master_label)

master_switch = ui.Switch()
master_switch.value = False
for l in lit_lights:
	if l:
		master_switch.value = True
		break
master_switch.center = ((x/2),(y/2)+(n_lights/2)-a*40)
master_switch.action = MasterSwitch
view.add_subview(master_switch)
view.present('')


w = 150
h = 110
wv = ui.View(frame=(0,0,w,h))
button = ui.Button(title='Foo',flex='rwh')
button.frame = (0, 0, w/2, h)
wv.add_subview(button)

"""
for l in all_lights:
	print(l.name,l.colormode)

#appex.set_widget_view(wv)
"""


def rgb_slider_action(sender):
	v = sender.superview
	r = v['rs'].value
	g = v['gs'].value
	b = v['bs'].value
	# Create the new color from the slider values:
	v['RGB_View'].background_color = (r, g, b)
	
	hsv = RGB_to_HSV(r,g,b)
	v['clabel'].text = '%f, %f, %f' % (hsv[0],hsv[1],hsv[2])
	v['clabel'].size_to_fit()
	
	kitchen[0].hue = int(65535*(hsv[0]/360))
	
	return

#l = kitchen[0]
rgbview = ui.View(name='RGB_View',height = 20, width = 20,background_color='#ffffff')
cval = True
rs = ui.Slider(name = 'rs',continuous = cval,action = rgb_slider_action)
gs = ui.Slider(name = 'gs',continuous = cval,action = rgb_slider_action)
bs = ui.Slider(name = 'bs',continuous = cval,action = rgb_slider_action)
clabel = ui.Label(name = 'clabel',text_color = item_color)


rgbviews = [rgbview,rs,gs,bs,clabel]
n = len(rgbviews)
for i in range(n):
	v = rgbviews[i]
	v.center = (x/2, (y*0.7)+i*40)
	if v.name == 'clabel':
		v.center = (x/2,(y*0.7)+(i+1)*40)
	view.add_subview(v)











