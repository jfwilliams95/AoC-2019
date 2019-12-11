# Day 11 - Advent of Code 2019
# Author: Jeff Williams

class Instruction:

  def __init__(self, val):
    # Turn it into a string
    val_str = str(val)

    # Turn it into 5 digits
    while len(val_str) < 5:
      val_str = "0" + val_str

    # Get the operator
    self.operator = int(val_str[3:5])
    self.modes = []
    self.modes.append(int(val_str[0]))
    self.modes.append(int(val_str[1]))
    self.modes.append(int(val_str[2]))

  def __str__(self):
    line = str(self.modes[0]) + str(self.modes[1]) + str(self.modes[2])
    if (self.operator < 10):
      line += "0"
    line += str(self.operator)
    return line

class Point:

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def equals(self, pos):
    return self.x == pos.x and self.y == pos.y

  def __str__(self):
    return "<" + str(self.x) + "," + str(self.y) + ">"

class Robot:

  def __init__(self, pos, code):
    self.pos = pos
    self.code = code
    self.map = Map()
    self.dir = 0 # 0 = N, 1 = E, 2 = S, 3 = W

  def run(self):
    paint_mode = True

    res = self.code.execute(None)
    while res["mode"] != "done":

      val = None

      if (res["mode"] == "output"):
        if (paint_mode):
          self.paint(self.map, res["value"])
        else:
          self.turn(res["value"])
          self.move()
        paint_mode = False if paint_mode else True
      else:
        val = self.scan(self.map)

      res = self.code.execute(val)

  def scan(self, map):
    return map.get_color(self.pos)

  def paint(self, map, white):
    map.paint(self.pos, white)

  def move(self):
    if (self.dir == 0):
      self.pos = Point(self.pos.x, self.pos.y-1)
    elif (self.dir == 1):
      self.pos = Point(self.pos.x+1, self.pos.y)
    elif (self.dir == 2):
      self.pos = Point(self.pos.x, self.pos.y+1)
    else:
      self.pos = Point(self.pos.x-1, self.pos.y)

  def turn(self, dir):
    # 1 = right, 0 = left
    if (dir == 1):
      self.dir += 1
    else:
      self.dir -= 1

    # If it turned right above 3, set it to 0
    if self.dir > 3:
      self.dir -= 4
    elif self.dir < 0:
      self.dir += 4

  def __str__(self):
    if (self.dir == 0):
      return "^"
    elif (self.dir == 1):
      return ">"
    elif (self.dir == 2):
      return "v"
    else:
      return "<"

  def print(self):
    bounds = self.map.get_bounds()

    print("")

    y_bounds = bounds["y"]
    x_bounds = bounds["x"]

    for y in range(y_bounds[0]-1, y_bounds[1] + 1):
      line = ""
      for x in range(x_bounds[0]-1, x_bounds[1] + 1):
        pos = Point(x,y)
        char = "#" if self.map.get_color(pos) == 1 else "."
        if (self.pos.equals(pos)):
          char = str(self)
        line += char
      print(line)

    print("pos " + str(self.pos))
    input('')


class Map:

  def __init__(self):
    self.white_spots = []
    self.touched_panels = []

  def get_bounds(self):
    x_bounds = [0,0]
    y_bounds = [0,0]

    for pos in self.white_spots:
      x_bounds[0] = pos.x if pos.x < x_bounds[0] else x_bounds[0]
      x_bounds[1] = pos.x if pos.x > x_bounds[1] else x_bounds[1]
      y_bounds[0] = pos.y if pos.y < y_bounds[0] else y_bounds[0]
      y_bounds[1] = pos.y if pos.y > y_bounds[1] else y_bounds[1]

    return {
      "x" : x_bounds,
      "y" : y_bounds
    }

  def get_color(self, pos):
    is_white = False

    for spot in self.white_spots:
      if (spot.equals(pos)):
        is_white = True
        break

    return 1 if is_white else 0

  def paint(self, pos, white):
    # Try to find the position
    found = False
    new_spots = []
    for spot in self.white_spots:
      if (spot.equals(pos)):
        found = True
        # If it's being re-painted white, add it again
        if (white):
          new_spots.append(spot)
      else:
        new_spots.append(spot)

    self.white_spots = new_spots

    # If it wasn't found, and it was being painted white, add it
    if not found and white:
      self.white_spots.append(Point(pos.x, pos.y))

    # If this point wasn't already touched, add it to the list
    touched = False
    for spot in self.touched_panels:
      if (spot.equals(pos)):
        touched = True
        break
    if not touched:
      self.touched_panels.append(pos)

class Code:

  def __init__(self, code):
    self.code = code
    self.i = 0
    self.rel_val = 0

  def get(self, index, mode):
    i = index
    if mode == 0:
      i = self.code[index]
    elif mode == 2:
      i = self.code[index] + self.rel_val

    if i > len(self.code)-1:
      return 0

    return self.code[i]

  def get_idx(self, index, mode):
    i = self.code[index]
    if mode == 2:
      i += self.rel_val

    return i

  def set(self, index, val):
    while index > len(self.code)-1:
      self.code.append(0)

    self.code[index] = val

  def execute(self, input_val):

    result = {
      "mode" : "input",
      "value" : 0
    }

    while True:
      instr = Instruction(self.code[self.i])

      # If it's waiting for an input, and the input is null, refer to the user
      if (instr.operator == 3 and input_val == None):
        result["mode"] = "input"
        result["value"] = None
        return result

      if (instr.operator == 99):
        result["mode"] = "done"
        result["value"] = None
        return result

      if instr.operator == 1:
        a = self.get(self.i + 1, instr.modes[2])
        b = self.get(self.i + 2, instr.modes[1])
        c = self.get_idx(self.i + 3, instr.modes[0])

        self.set(c, (a + b))
        self.i += 4
      elif instr.operator == 2:
        a = self.get(self.i + 1, instr.modes[2])
        b = self.get(self.i + 2, instr.modes[1])
        c = self.get_idx(self.i + 3, instr.modes[0])

        self.set(c, (a * b))
        self.i += 4
      elif instr.operator == 3:
        a = self.get_idx(self.i + 1, instr.modes[2])

        self.set(a, input_val)
        self.i += 2

        # reset the input value
        input_val = None
      elif instr.operator == 4:
        a = self.get(self.i + 1, instr.modes[2])

        result["mode"] = "output"
        result["value"] = a
        self.i += 2
        return result
      elif instr.operator == 5:
        a = self.get(self.i + 1, instr.modes[2])
        b = self.get(self.i + 2, instr.modes[1])

        if (a != 0):
          self.i = b
        else:
          self.i += 3
      elif instr.operator == 6:
        a = self.get(self.i + 1, instr.modes[2])
        b = self.get(self.i + 2, instr.modes[1])

        if (a == 0):
          self.i = b
        else:
          self.i += 3
      elif instr.operator == 7:
        a = self.get(self.i + 1, instr.modes[2])
        b = self.get(self.i + 2, instr.modes[1])
        c = self.get_idx(self.i + 3, instr.modes[0])

        val = 1 if a < b else 0
        self.set(c, val)
        self.i += 4
      elif instr.operator == 8:
        a = self.get(self.i + 1, instr.modes[2])
        b = self.get(self.i + 2, instr.modes[1])
        c = self.get_idx(self.i + 3, instr.modes[0])

        val = 1 if a == b else 0
        self.set(c, val)
        self.i += 4
      elif instr.operator == 9:
        a = self.get(self.i + 1, instr.modes[2])

        self.rel_val += a
        self.i += 2
      else:
        print("ERROR - Tried to execute an operation code of " + str(instr.operator))
        break
          

# Reads in the file
def get_code(filename):
  code = []
  with open(filename, "r") as file:
    line = file.readline().strip()
    codestrs = line.split(',')
   
    for codestr in codestrs:
      code.append(int(codestr.strip()))
  return Code(code)

code = get_code('./input/day11.txt')
robot = Robot(Point(0,0), code)
robot.paint(robot.map, 1)
robot.run()
robot.print()

