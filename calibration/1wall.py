#!/usr/bin/python3
# coding: utf-8

import math

# -----------------------------------------------
# Main settings, adapt these values to your needs
# -----------------------------------------------

# center of the cube
center_x = 100.0
center_y = 100.0

# cube size
size = 20.0

# gap for the skirt
skirt_gap = 3

# areas of filament and nozzle to compute extrusion
filamentArea = pow(1.75 / 2, 2) * math.pi
nozzleArea = pow(0.35 / 2, 2) * math.pi

# print speed, keep it slow
speed = 20.0 * 60.0

# tool: 0 for right extruder, 1 for left extruder
tool = 1 

# temperature
temperature = 190

# -----
# code 
# -----

def extrude(x0, y0, x1, y1):
	dx = x0 - x1
	dy = y0 - y1
	len = math.sqrt(dx*dx + dy*dy)

	return (len * nozzleArea) / filamentArea

# Prolog
print('''
G28
G1 Z5 F600
G1 Z0 F600
M107
G90
M82

M104 T''' + str(tool) + ''' S''' + str(temperature) + 
'''
G92 E0

M109 T''' + str(tool) + ''' S''' + str(temperature) +
'''
T''' + str(tool) +
'''
M83
G1 E10 F100
M82
G92 E0

M117 One wall ...
G1 F1000 Z5
''')

e = 0.0

print("GO Z0.2")

# draw the skirt
for i in range(0, 6):
        gap = (size / 2) + skirt_gap + i

        print("G0 X{0} Y{1} F7200".format(center_x - gap, center_y - gap))

        e += extrude(center_x - gap, center_y - gap, center_x + gap, center_y - gap)
        print("G1 X{0:.1f} Y{1:.1f} E{2:.3f} F{3}".format(center_x + gap, center_y - gap, e, speed))
        
        e += extrude(center_x + gap, center_y - gap, center_x + gap, center_y + gap)
        print("G1 X{0:.1f} Y{1:.1f} E{2:.3f}".format(center_x + gap, center_y + gap, e))

        e += extrude(center_x + gap, center_y + gap, center_x - gap, center_y + gap)
        print("G1 X{0:.1f} Y{1:.1f} E{2:.3f}".format(center_x - gap, center_y + gap, e))

        e += extrude(center_x - gap, center_y + gap, center_x - gap, center_y - gap)
        print("G1 X{0:.1f} Y{1:.1f} E{2:.3f}".format(center_x - gap, center_y - gap, e))

# fan speed to max
print("M106 S255")

# draw the cube
print("G0 X{0} Y{1} F7200".format(center_x - (size / 2), center_y - (size / 2)))

extrLength = (size * nozzleArea) / filamentArea

for i in [x * 0.2 for x in range(1, 51)]:
	print("G0 Z{0:.3f}".format(i))

	print("G1 X{0:.1f} Y{1:.1f} E{2:.3f} F{3}".format(center_x + (size / 2), center_y - (size / 2), e, speed))
	e += extrLength

	print("G1 X{0:.1f} Y{1:.1f} E{2:.3f}".format(center_x + (size / 2), center_y + (size / 2), e))
	e += extrLength

	print("G1 X{0:.1f} Y{1:.1f} E{2:.3f}".format(center_x - (size / 2), center_y + (size / 2), e))
	e += extrLength

	print("G1 X{0:.1f} Y{1:.1f} E{2:.3f}".format(center_x - (size / 2), center_y - (size / 2), e))
	e += extrLength

print("")

# End gcode
print('''
G1 X200 Y200 Z130
M107
G91
T''' + str(tool) + 
'''
G1 E-1
M104 T''' + str(tool) + ''' S0

G90
G92 E0
M140 S0
M84
''')


