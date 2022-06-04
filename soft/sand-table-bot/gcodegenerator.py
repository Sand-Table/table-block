import math

# file = open('sandify.gcode', 'r')
# lines = file.readlines()
# for line in lines:
#    print(line)


resolution = 50
scale_x = 250
scale_y = 85
offset_x = 150
max_x = 200


def convert(x, y):
    r = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
    if x == 0:
        x = 0.0001
    a = math.atan(y / x) * scale_y
    return r, a


def convert_all(points):
    converted_points = list()
    for point in points:
        converted_points.append(convert(*point))
    return converted_points


def get_eq(x1, y1, x2, y2):
    slope = (y2 - y1) / (x2 - x1)
    offset = y1 - slope * x1
    return slope, offset


def get_points_for_list(points):
    all_points = list()
    for i in range(len(points)):
        all_points.extend(get_points(points[i][0], points[i][1], points[(i + 1)%len(points)][0], points[(i + 1)%len(points)][1]))
    return all_points


def get_points(x1, y1, x2, y2):
    points = list()
    slope, offset = get_eq(x1, y1, x2, y2)
    print("hey")
    for i in range(resolution):
        x = x1 + (i / resolution) * (x2 - x1)
        y = slope * x + offset
        points.append((x, y))
    return points


def square():
    points = list()
    points.append((0, 1))
    points.append((1, 0))
    points.append((0, -1))
    points.append((-1, 0))
    return points


def adapt(points: list, scale=1, tilt=0):
    points_converted = list()
    for point in points:
        points_converted.append((point[0] * scale, point[1] * scale))
    return points_converted


def write_circle_gcode(size):
    file = open('grbl.gcode', 'w')
    file.write("G91 X" + str(size) + " Y" + str(0) + "\n")
    file.write("G91 X" + str(0) + " Y" + str(scale_y) + "\n")
    file.write("G91 X" + str(-size) + " Y" + str(0) + "\n")
    file.write("G91 X" + str(0) + " Y" + str(-scale_y) + "\n")
    file.close()


def write_concentric_circles_gcode(amount):
    clockwise = True
    step_x = max_x / amount
    file = open('grbl.gcode', 'w')
    for i in range(amount):
        file.write("G91 X" + str(step_x) + " Y" + str(0) + "\n")
        y = scale_y
        if not clockwise:
            y = -y
        file.write("G91 X" + str(0) + " Y" + str(y) + "\n")
        clockwise = not clockwise
    file.write("G91 X" + str(-step_x*amount) + " Y" + str(0) + "\n")
    if not clockwise:
        file.write("G91 X" + str(0) + " Y" + str(-scale_y) + "\n")


def write_gcode(points: list):
    file = open('grbl.gcode', 'w')
    for point in points:
        # print("G91 X" + str(point[0]) + " Y" + str(point[1]))
        file.write("G90 X" + str(point[0]+offset_x) + " Y" + str(point[1]) + "\n")
    file.close()


#print(adapt(get_points_for_list(square())))
#write_gcode(convert_all(adapt(get_points_for_list(square()),150)))
write_circle_gcode(150)