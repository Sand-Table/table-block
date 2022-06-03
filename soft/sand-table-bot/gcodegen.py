import math
import re
import copy
import sys
from pathlib import Path

# Polar Pre Processor

# Bart Dring
# @buildlog
# 8/2017 Open Source Creative Commons 4.0 Attribution Share Alike

# This converts regular cartesian gcode to polar coordinate gcode
# The gcode must be lines (G0, G1) only and not contain arcs (G2, G3)
# Usage...
#    Opt 1: Specify both input and output files
#       python PolarPreProcessor.py input_filename output_filename
#    Opt 2: Output file will be input file with "_polar" appended to it....  box.gcode to box_polar.gcode
#    python PolarPreProcessor.py input_filename


# configuration settings
float_format = "%0.3f"  # format used to output gcode numbers to file
min_segment_length = 1.0  # any cartesian move greater than this will be broken into smaller moves <= this value
inversion_compensation = -1  # This is used to correct for inverted output use 1 or -1 only for this value

# a class to represent a Cartesian point and some helper functions
class CartesianPt:
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z

    def dist_xy(self, to_x, to_y):
        return math.sqrt((self.X - to_x) ** 2 + (self.Y - to_y) ** 2)

    def dist_x(self, to_x):
        return to_x - self.X

    def dist_y(self, to_y):
        return to_y - self.Y


# a class to represent a Polar point and some helper functions
class PolarPt:
    def __init__(self, radius, angle):
        self.Radius = radius
        self.Angle = angle

    def set_from_cartesian(self, x, y, current_angle):

        next_angle = math.atan2(y, x) * 180.0 / math.pi
        next_angle = self.abs_angle(next_angle)  # convert to 0-359.99___

        delta = next_angle - self.abs_angle(current_angle)  # how far from the current angle are we?

        if math.fabs(delta) <= 180:  # is the move less than half a circle?
            next_angle = current_angle + delta
        else:  # since it is greater than half a circle it is a shorter move to go backwards
            if self.abs_angle(current_angle) > 180.0:  # Are we on the bottom of the circle, then crossing zero goes upwards
                delta = 360 + delta
                next_angle = current_angle + delta
            else:  # crossing zero goes downwards
                next_angle = current_angle - (360.0 - delta)

        self.Radius = math.sqrt(x ** 2 + y ** 2)
        self.Angle = next_angle


    # return the absolute, positive, 0-359.99___ angle on the polar grid
    # this corrects for angles above 360, so 370 would return 10
    # this corrects for negative angles so -10 would return 350 and -350 would retun 10
    def abs_angle(self, ang):
        return ang % 360

    # This calculates the distance in units to help with feed rate compensation
    # The controller thinks degrees are millimeters so feed rate is based on what the controller thinks the
    # linear distance is. If we compare this to the real world distance, we can apply a compensation factor
    def unit_distance(self, to_radius, to_angle):
        return math.sqrt((self.Radius - to_radius)**2 + (self.Angle - to_angle)**2 )


class MotionMode(enumerate):
    G0 = 0
    G1 = 1
    G2 = 2
    G3 = 3

# TODO: File Exists

if len(sys.argv) < 2:
    sys.exit("Error: Not enough parameters. Use... 'python PolarPreProcessor.py input_file [output_file]'")

input_filename = Path(sys.argv[1])
if not input_filename.is_file():
    sys.exit("Error: The input file %s does not exist" % input_filename)


if len(sys.argv) == 3:
    output_filename = sys.argv[2]
else:
    p = Path(input_filename)
    output_filename = str(p.parent) + '\\' + Path(input_filename).stem + "_polar" + Path(input_filename).suffix


f = open(input_filename, "r")

# initialize some variables
current_cartesian_location = CartesianPt(0, 0, 0)
next_cartesian_location = CartesianPt(0, 0, 0)
current_polar = PolarPt(0, 0)
next_polar = PolarPt(0, 0)
motionMode = MotionMode.G0
gcode_out_line = ""
gcode_out_list = []

for line in f:
    line.strip()  # remove whitespace at ends

    if line != "":
        line.upper()  # Make upper case so it is easier to parse

        #gcode_out_list.append("; --" + line)

        gWords = re.findall(r'G\d+', line)  # get all "G" works
        if 'G0' in gWords:
            motionMode = MotionMode.G0
        elif 'G1' in gWords:
            motionMode = MotionMode.G1
        # else leave it unchanged from previous occurrences

        # Parse the gcode words with values into a dict
        # key is the parameter
        # value = the value
        # X123.45 returns
        gWords = re.findall(r'([ABCIJKNPXYZFST])([+-]?\d*\.?\d+)', line)

        # create a dictionary
        gc_dict = {}
        for gc in gWords:
            gc_dict[gc[0]] = gc[1]

        if 'F' in gc_dict:  # If we have a feed rate save it, else the last feed rate remains in effect
            feed_rate = float(gc_dict['F'])

        if 'X' in gc_dict or 'Y' in gc_dict:  # We only need to do a conversion if there is X or Y data in the line
            if 'X' in gc_dict:
                next_cartesian_location.X = float(gc_dict['X']) * inversion_compensation

            if 'Y' in gc_dict:
                next_cartesian_location.Y = float(gc_dict['Y'])

            if 'Z' in gc_dict:
                next_cartesian_location.Z = float(gc_dict['Z'])

            if motionMode == MotionMode.G0:  # We don't need to break the move into segments in G0 (rapid) mode
                next_polar.set_from_cartesian(next_cartesian_location.X, next_cartesian_location.Y, current_polar.Angle)
                gcode_out_line = "G0"
                gcode_out_line += " X" + float_format % next_polar.Radius
                gcode_out_line += " Y" + float_format % next_polar.Angle
                gcode_out_line += " Z" + float_format % next_cartesian_location.Z
                gcode_out_list.append(gcode_out_line + "\n")

            else:  # This is a G1 move so we need to break long moves into multiple smaller moves
                xy_move_dist = current_cartesian_location.dist_xy(next_cartesian_location.X, next_cartesian_location.Y)
                if xy_move_dist > min_segment_length:
                    segments = math.floor(xy_move_dist / min_segment_length) + 1  # How many segments do we need
                    segment_length = xy_move_dist / segments  # What is the length of each segment
                    x_segment_length = current_cartesian_location.dist_x(next_cartesian_location.X) / segments
                    y_segment_length = current_cartesian_location.dist_y(next_cartesian_location.Y) / segments

                    for i in range(1, segments + 1):
                        # next_cartesian_location.X = current_cartesian_location.X + (x_segment_length * i)
                        next_polar.set_from_cartesian(current_cartesian_location.X + (x_segment_length * i),
                                                      current_cartesian_location.Y + (y_segment_length * i),
                                                      current_polar.Angle)

                        gcode_out_line = "G1"
                        gcode_out_line += " X" + float_format % next_polar.Radius
                        gcode_out_line += " Y" + float_format % next_polar.Angle
                        gcode_out_line += " F" + float_format % (360.0 / (next_polar.Radius * 2.0 * math.pi) * feed_rate)
                        gcode_out_list.append(gcode_out_line + "\n")

                        current_polar.Angle = next_polar.Angle

                else:
                    next_polar.set_from_cartesian(next_cartesian_location.X,
                                                  next_cartesian_location.Y,
                                                  current_polar.Angle)
                    gcode_out_line = "G1"
                    gcode_out_line += " X" + float_format % next_polar.Radius
                    gcode_out_line += " Y" + float_format % next_polar.Angle
                    gcode_out_line += " F" + float_format % (360.0 / (next_polar.Radius * 2.0 * math.pi) * feed_rate)
                    gcode_out_list.append(gcode_out_line + "\n")

            current_cartesian_location.X = next_cartesian_location.X
            current_cartesian_location.Y = next_cartesian_location.Y
            current_polar.Angle = next_polar.Angle

        else:
            gcode_out_list.append(line)

# output the new converted file
f = open(output_filename, "w")
for line in gcode_out_list:
    f.write(line)
f.close
print(output_filename)
print("done")

