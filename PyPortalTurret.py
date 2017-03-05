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
import subprocess
FIFO_PATH = '/tmp/launcher_control'
class Armageddon:
	DOWN = "DOWN"
	UP = "UP"
	LEFT = "LEFT"
	RIGHT = "RIGHT"
	FIRE = "FIRE"

	def send_move(self, cmd, duration):
		open(FIFO_PATH, 'w+').write(cmd+' '+str(duration)+'\n')
	def send_cmd(self, cmd):
		open(FIFO_PATH, 'w+').write(cmd+' \n')
LOST_TIMEOUT=28
FOUND_TIMEOUT=3
SLEEP_TIMEOUT=100
FIRE_TIMEOUT=5
PING_TIMEOUT=14
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
	instance.send_move(instance.RIGHT, 5400)
	time.sleep(5.6)
	instance.send_move(instance.LEFT, 2800)
	time.sleep(3.0)
	playSnd("sounds/Turret_retract.wav")
	playSnd(random.choice(sleep_s))
	instance.send_move(instance.DOWN, 2800)
	time.sleep(3.0)
	instance.send_move(instance.UP, 300)
	time.sleep(0.3)
def do_wakeup():
	playSnd("sounds/Turret_deploy.wav")
	playSnd(random.choice(wakeup_s))
	
def do_loose():
	playSnd(random.choice(search_s))
def do_find():
	playSnd(random.choice(find_s))
def do_fire():
	instance.send_cmd(instance.FIRE)
	time.sleep(0.1)
	playSnd(random.choice(fire_s))
def do_ping():
	playSnd("sounds/Turret_ping.wav")
print 'Creating instance'
instance = Armageddon()
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
profileFaceCascade = cv2.CascadeClassifier("haarcascade_profileface.xml")
bodyCascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")
upperBodyCascade = cv2.CascadeClassifier("haarcascade_upperbody.xml")
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

  if i_fnum>=7:
    i_fnum=0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=7,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    if faces==():
		faces = profileFaceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=7,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
    if faces==():
		faces = bodyCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=7,
        minSize=(80, 80),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
    if faces==():
		faces = upperBodyCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=7,
        minSize=(80, 80),
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
		cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0, 0),2)
		cv2.imshow('feed',frame)
		ch = 0xFF & cv2.waitKey(1)
		if ch == 27:
			break
		cx=x+w/2
		cy=y+h/2
		height, width = gray.shape
		print str(height)+'x'+str(width)+' ('+str(cx)+','+str(cy)+')'+' '+str(w)+'x'+str(h)
		moved_v=(290*abs(height/2-cy))/height
		moved_h=(350*abs(width/2-cx))/width
		if height/2-cy>height/10:
			instance.send_move(instance.UP, moved_v)
			time.sleep(moved_v/1000.0+0.13)
		if cy-height/2>height/10:
			instance.send_move(instance.DOWN, moved_v)
			time.sleep(moved_v/1000.0+0.13)
		if width/2-cx>width/12:
			instance.send_move(instance.LEFT, moved_h)
			time.sleep(moved_h/1000.0+0.13)
		if cx-width/2>width/12:
			instance.send_move(instance.RIGHT, moved_h)
			time.sleep(moved_h/1000.0+0.13)
		if (height/2-cy<=height/9 and cy-height/2<=height/9 and width/2-cx<=width/10 and cx-width/2<=width/10):
			i_acquired+=1
			if i_acquired>=FIRE_TIMEOUT:
				do_fire();
				time.sleep(3.7)

		else:
			i_acquired=0
    else:
		cv2.imshow('feed',frame)
		ch = 0xFF & cv2.waitKey(1)
		if ch == 27:
			break
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

