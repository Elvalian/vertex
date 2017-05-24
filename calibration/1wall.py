#!/usr/bin/python3
# coding: utf-8

import math

x=100.0
y=100.0

delta=20.0
deltaSkirt = delta + 10

filamentArea = pow(1.75 / 2, 2) * math.pi
nozzleArea = pow(0.35 / 2, 2) * math.pi

speed = 20.0 * 60.0

def extrude(x0, y0, x1, y1):
	dx = x0 - x1
	dy = y0 - y1
	len = math.sqrt(dx*dx + dy*dy)
	return (len * nozzleArea) / filamentArea

# Start gcode
print('''
G28
G1 Z5
G1 Z0
M107
G90
M82

M104 T1 S190
G92 E0

M109 T1 190
T1
M83
G1 E10 F100
M82
G92 0

M117 One wall ...
G1 F1000 Z5
''')

extrLength = (delta * nozzleArea) / filamentArea
e = 0.0

print("GO Z0.2")

for i in range(0, 6):
	print("G0 X{0} Y{1} F7200".format(x - (deltaSkirt + i), y - (deltaSkirt + i)))

	e += extrude(x - (deltaSkirt + i), y - (deltaSkirt + i), x + (deltaSkirt + i), y - (deltaSkirt + i))
	print("G1 X{0:.1f} Y{1:.1f} E{2:.3f} F{3}".format(x + (deltaSkirt + i), y - (deltaSkirt + i), e, speed))
        
	e += extrude(x + (deltaSkirt + i), y - (deltaSkirt + i), x + (deltaSkirt + i), y + (deltaSkirt + i))
	print("G1 X{0:.1f} Y{1:.1f} E{2:.3f}".format(x + (deltaSkirt + i), y + (deltaSkirt + i), e))

	e += extrude(x + (deltaSkirt + i), y + (deltaSkirt + i), x - (deltaSkirt + i), y + (deltaSkirt + i))
	print("G1 X{0:.1f} Y{1:.1f} E{2:.3f}".format(x - (deltaSkirt + i), y + (deltaSkirt + i), e))

	e += extrude(x - (deltaSkirt + i), y + (deltaSkirt + i), x - (deltaSkirt + i), y - (deltaSkirt + i))
	print("G1 X{0:.1f} Y{1:.1f} E{2:.3f}".format(x - (deltaSkirt + i), y - (deltaSkirt + i), e))
        
print("M106 S255")
print("G0 X{0} Y{1} F7200".format(x, y))

for i in [x * 0.2 for x in range(1, 51)]:
	print("G0 Z{0:.3f}".format(i))

	print("G1 X{0:.1f} Y{1:.1f} E{2:.3f} F{3}".format(x-20, y, e, speed))
	e += extrLength

	print("G1 X{0:.1f} Y{1:.1f} E{2:.3f}".format(x-20, y-20, e))
	e += extrLength

	print("G1 X{0:.1f} Y{1:.1f} E{2:.3f}".format(x, y-20, e))
	e += extrLength

	print("G1 X{0:.1f} Y{1:.1f} E{2:.3f}".format(x, y, e))
	e += extrLength

print("")

# End gcode
print('''
G1 X200 Y200 Z130
M107
G91
T1
G1 E-1
M104 T1 S0

G90
G92 E0
M140 S0
M84
''')


