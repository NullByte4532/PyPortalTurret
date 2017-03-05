from usb_launcher import *
import sys
import time
import os
FIFO_PATH = '/tmp/launcher_control'
if os.path.exists(FIFO_PATH):
    os.unlink(FIFO_PATH)
if not os.path.exists(FIFO_PATH):
    os.mkfifo(FIFO_PATH)
    os.chmod(FIFO_PATH, 0666)
    #ct_fifo = open(FIFO_PATH, 'r')
instance = Armageddon()
while True:
	time.sleep(0.1)
	cmd=open(FIFO_PATH, 'r').readline()
	while cmd!='':
	 try:
		print cmd
		l=cmd.split(" ")
		if l[0]=="LEFT":
			instance.send_move(instance.LEFT, int(l[1]))
		elif l[0]=="RIGHT":
			instance.send_move(instance.RIGHT, int(l[1]))
		elif l[0]=="UP":
			instance.send_move(instance.UP, int(l[1]))
		elif l[0]=="DOWN":
			instance.send_move(instance.DOWN, int(l[1]))
		elif l[0]=="FIRE":
			instance.send_cmd(instance.FIRE)
	 except:
		 print "Something went wrong."
	 cmd=open(FIFO_PATH, 'r').readline()
			
