#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  PyPortalTurret.py
#  
#  Copyright 2017 NullByte4532 <nullbyte4532@nullbyte4532-Lenovo-G510>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import sys
import time
import os
import cv2
import random
from usb_launcher import *
import subprocess

LOST_TIMEOUT=4
FOUND_TIMEOUT=4
SLEEP_TIMEOUT=40
FIRE_TIMEOUT=4
PING_TIMEOUT=4
sleep_s=[]
wakeup_s=[]
find_s=[]
fire_s=[]
search_s=[]
def find_sounds():
	for file in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sounds/sleep")):
		sleep_s.append(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sounds/sleep"), file))
	for file in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sounds/wakeup")):
		wakeup_s.append(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sounds/wakeup"), file))
	for file in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sounds/find")):
		find_s.append(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sounds/find"), file))
	for file in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sounds/fire")):
		fire_s.append(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sounds/fire"), file))
	for file in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sounds/search")):
		search_s.append(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sounds/search"), file))
def playSnd(f):
	subprocess.Popen(["play", f])
def do_sleep():
	instance.send_move(instance.RIGHT, 5200)
	instance.send_move(instance.LEFT, 2700)
	playSnd("sounds/Turret_retract.wav")
	playSnd(random.choice(sleep_s))
def do_wakeup():
	playSnd("sounds/Turret_deploy.wav")
	playSnd(random.choice(wakeup_s))
	
def do_loose():
	playSnd(random.choice(search_s))
def do_find():
	playSnd(random.choice(find_s))
def do_fire():
	playSnd(random.choice(fire_s))
def do_ping():
	playSnd("sounds/Turret_ping.wav")
print 'Creating instance'
instance = Armageddon()
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(1)
i_fnum=0
i_noface=0
i_face=0
state=0
i_acquired=0
find_sounds()
while True:
    # Capture frame-by-frame
  ret, frame = video_capture.read()
  i_fnum+=1
  
  if i_fnum>=2:
    i_fnum=0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=7,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    if faces!=():
	 i_face+=1
	 i_noface=0
	 if i_face>=FOUND_TIMEOUT:
	  if state==2:
		  do_find()
	  if state==3:
		  do_wakeup()
	  
	  state=1
	 if state==1:
		x, y, w, h = faces[0]
		cx=x+w/2
		cy=y+h/2
		height, width = gray.shape
		print str(height)+'x'+str(width)+' ('+str(cx)+','+str(cy)+')'
		if height/2-cy>height/10:
			instance.send_move(instance.UP, 30)
		if cy-height/2>height/10:
			instance.send_move(instance.DOWN, 30)
		if width/2-cx>width/12:
			instance.send_move(instance.LEFT, 30)
		if cx-width/2>width/12:
			instance.send_move(instance.RIGHT, 30)
		if (height/2-cy<=height/9 and cy-height/2<=height/9 and width/2-cx<=width/10 and cx-width/2<=width/10):
			i_acquired+=1
			if i_acquired>=FIRE_TIMEOUT:
				do_fire();
		else:
			i_acquired=0
    else:
		i_noface+=1
		i_face=0
		if i_noface>=LOST_TIMEOUT and state<2:
			state=2
			do_loose()
		if state==2 and i_noface%PING_TIMEOUT==2:
			do_ping()
		if i_noface>=SLEEP_TIMEOUT and state<3:
			state=3
			do_sleep()
			
	
# When everything is done, release the capture
video_capture.release()

