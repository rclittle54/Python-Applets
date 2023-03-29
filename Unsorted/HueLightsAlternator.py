#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 20:50:22 2017


Hue Light Basic Control



@author: ryanlittle
"""

from phue import Bridge
import random
import time


b_ip = '192.168.86.103'
b = Bridge(b_ip)
b.connect()

random.seed(00000)


LivingRoom = ['Lamp Up','Lamp Down','Side Table']
Bedroom = ['Ryans Side','Megans Side']
Kitchen = ['Kitchen 1', 'Kitchen 2', 'Kitchen 3', 'Kitchen 4']

testlist = LivingRoom + Kitchen

lights = b.lights




lightslist = b.get_light_objects('name')
#print(lightslist)



#b.set_light('Ryans Side', 'hue',15000)

n_minutes = 30
n_seconds = n_minutes*60 + 1

for light in lights:
    light.transitiontime = 2



while n_seconds > 0:
    
    
    hue1 = random.random()*65000
    hue2 = random.random()*65000
    hue3 = random.random()*65000
                        
                        
    UTD_hues = [26636,6661]
                        
                        
    #b.set_light('Ryans Side','hue',hue1)
    #b.set_light('Megans Side','hue',hue2)
    #b.set_light(['Lamp Up','Lamp Down','Side Table'],'hue',hue3)
       
    
    for light in lights:
        if light.name in LivingRoom or light.name in Kitchen:
            light.hue = UTD_hues[n_seconds%2]
            #print(n_seconds%1)
        elif light.name == 'Ryans Side':
            light.hue = UTD_hues[(n_seconds+1)%2]
        elif light.name == 'Megans Side':
            light.hue = UTD_hues[(n_seconds+0)%2]
    
    
    
    
    
    
    time.sleep(1)
    n_seconds -= 1
    print(n_seconds)
    if n_seconds % 60 == 0:
        print(n_seconds/60,' minutes remaining.')


print("Done.")