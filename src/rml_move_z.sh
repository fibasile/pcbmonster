#!/usr/bin/python
import serial
import sys

print sys.argv

x = int(sys.argv[1]) * 40
y = int(sys.argv[2]) * 40
z = int(sys.argv[3]) * 40 
port = sys.argv[4] 

cmd="PA;PA;!VZ10;Z %d,%d,%d;!MC0;" % (x,y,z)

print cmd

if port.count('lp') >= 0:
  f= open(port,'w',0)
  f.write(cmd)
  f.close()
else:
  serial = serial.Serial(port, baudrate=9600, rtscts=True, timeout=0)
  serial.write(cmd)
  serial.close()
