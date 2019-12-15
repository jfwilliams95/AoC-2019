# Day 15 - Advent of Code
# Author: Jeff Williams

import getch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

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

  def copy(self):
    return Point(self.x, self.y)

  def equals(self, pos):
    return self.x == pos.x and self.y == pos.y

  def __str__(self):
    return "<" + str(self.x) + "," + str(self.y) + ">"

class Robot:

  def __init__(self, pos, code):
    self.pos = pos
    self.code = code
    self.direction = None
    self.map = Map()
    self.map.add_empty(self.pos)
    self.steps = 0

  def copy(self):
    robot = Robot(self.pos.copy(), self.code.copy())
    robot.direction = self.direction
    robot.map = self.map # This doesn't need to be a copy since it's all the same map
    robot.steps = self.steps
    return robot

  def get_pos_facing(self):
    x = self.pos.x
    y = self.pos.y

    if (self.direction == 1):
      y -= 1
    elif (self.direction == 2):
      y += 1
    elif (self.direction == 3):
      x -= 1
    else:
      x += 1

    return Point(x,y)

  def move(self, direction):

    val = direction
    while True:
      self.direction = val
      resp = self.code.execute(self.direction)

      code = -1
      if (resp["mode"] == "output"):
        code = int(resp["value"])
      elif (resp["mode"] == "input"):
        return "AWAITING"

      if (code == -1):
        return "ERROR"
      elif (code == 0):
        # Get the coordinate of the wall
        wall_pos = self.get_pos_facing()
        self.map.add_wall(wall_pos)
        return "STOPPED"
      elif (code == 1):
        next_pos = self.get_pos_facing()
        self.pos = next_pos

        # If it's already been mapped, let the user know
        if (self.map.has_been_mapped(next_pos)):
          return "LOOPED"

        self.map.add_empty(next_pos)
        self.steps += 1
        return "AWAITING"
      elif (code == 2):
        next_pos = self.get_pos_facing()
        self.pos = next_pos
        self.map.add_empty(next_pos)
        self.steps += 1
        return "DONE"

  def print(self):
    bounds = self.map.get_bounds()

    for y in range(bounds["y"][0], bounds["y"][1] + 1):
      line = ""
      for x in range(bounds["x"][0], bounds["x"][1] + 1):
        if (self.pos.equals(Point(x,y))):
          line += "D"
        else:
          line += self.map.get(Point(x,y))
      print(line)

class Map:

  def __init__(self):
    self.walls = []
    self.empty = []
    self.o2 = []

  def copy(self):
    m = Map()
    for w in self.walls:
      m.walls.append(w.copy())
    for e in self.empty:
      m.empty.append(e.copy())
    for o in self.o2:
      m.o2.append(o.copy())
    return m

  def add_wall(self, pos):
    # If it already exists do nothing
    for wall in self.walls:
      if wall.equals(pos):
        return
    self.walls.append(Point(pos.x, pos.y))

  def add_empty(self, pos):
    # If it already exists do nothing
    for e in self.empty:
      if e.equals(pos):
        return
    self.empty.append(Point(pos.x, pos.y))

  def add_o2(self, pos):
    for o in self.o2:
      if o.equals(pos):
        return
    self.o2.append(pos.copy())

  def has_been_mapped(self, pos):
    for w in self.walls:
      if (w.equals(pos)):
        return True
    for e in self.empty:
      if (e.equals(pos)):
        return True

    return False

  def get_bounds(self):
    x_bounds = [0,0]
    y_bounds = [0,0]

    for pos in self.walls:
      x_bounds[0] = pos.x if pos.x < x_bounds[0] else x_bounds[0]
      x_bounds[1] = pos.x if pos.x > x_bounds[1] else x_bounds[1]
      y_bounds[0] = pos.y if pos.y < y_bounds[0] else y_bounds[0]
      y_bounds[1] = pos.y if pos.y > y_bounds[1] else y_bounds[1]

    for pos in self.empty:
      x_bounds[0] = pos.x if pos.x < x_bounds[0] else x_bounds[0]
      x_bounds[1] = pos.x if pos.x > x_bounds[1] else x_bounds[1]
      y_bounds[0] = pos.y if pos.y < y_bounds[0] else y_bounds[0]
      y_bounds[1] = pos.y if pos.y > y_bounds[1] else y_bounds[1]

    return {
      "x" : x_bounds,
      "y" : y_bounds
    }

  def print(self):
    bounds = self.get_bounds()

    for y in range(bounds["y"][0], bounds["y"][1] + 1):
      line = ""
      for x in range(bounds["x"][0], bounds["x"][1] + 1):
        line += self.get(Point(x,y))
      print(line)

  def printwbots(self, bots):
    botpos = []
    for bot in bots:
      botpos.append(bot.pos.copy())
    bounds = self.get_bounds()

    for y in range(bounds["y"][0], bounds["y"][1] + 1):
      line = ""
      for x in range(bounds["x"][0], bounds["x"][1] + 1):
        added = False
        for bp in botpos:
          if (bp.equals(Point(x,y))):
            line += "D"
            added = True
            break
        if not added:
          line += self.get(Point(x,y))
      print(line)

  def get(self, pos):
    for w in self.walls:
      if (w.equals(pos)):
        return "#"
    for o in self.o2:
      if (o.equals(pos)):
        return "O"
    for e in self.empty:
      if (e.equals(pos)):
        return "."
    

    return " "


class Code:

  def __init__(self, code):
    self.code = code
    self.i = 0
    self.rel_val = 0

  def copy(self):
    c = []
    for a in self.code:
      c.append(a)
    code = Code(c)
    code.i = self.i
    code.rel_val = self.rel_val
    return code

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

def ask_dir():
  getch = _GetchWindows()
  d = getch()

  if d == b"w":
    return 1
  elif d == b"s":
    return 2
  elif d == b"a":
    return 3
  elif d == b"d":
    return 4
  else:
    return -1

code = get_code('./input/day15.txt')
bot = Robot(Point(0,0), code)

bots = [bot]

found = False
last_bot = None
steps = 0
o2_pos = None
my_map = None
while len(bots) != 0:
  alive_bots = []
  for bot in bots:
    # Spawn one for each direction
    nbot = bot
    wbot = bot.copy()
    ebot = bot.copy()
    sbot = bot.copy()

    # ask them to go their next direction
    nresp = nbot.move(1)
    sresp = sbot.move(2)
    wresp = wbot.move(3)
    eresp = ebot.move(4)

    if nresp == "AWAITING":
      alive_bots.append(nbot)
    if sresp == "AWAITING":
      alive_bots.append(sbot)
    if wresp == "AWAITING":
      alive_bots.append(wbot)
    if eresp == "AWAITING":
      alive_bots.append(ebot)

    if nresp == "DONE":
      steps = nbot.steps
      o2_pos = nbot.pos.copy()
      found = True
      alive_bots.append(nbot)
    if sresp == "DONE":
      steps = sbot.steps
      o2_pos = sbot.pos.copy()
      found = True
      alive_bots.append(sbot)
    if eresp == "DONE":
      steps = ebot.steps
      o2_pos = ebot.pos.copy()
      found = True
      alive_bots.append(ebot)
    if wresp == "DONE":
      steps = wbot.steps
      o2_pos = wbot.pos.copy()
      found = True
      alive_bots.append(wbot)

  if (len(alive_bots) == 0):
    my_map = bots[0].map.copy()
    for bot in bots:
      bot.print()


  bots = alive_bots
print(steps)
print(o2_pos)
print()

# Part two
my_map.add_o2(o2_pos)
points = [o2_pos.copy()]
mins = 0
while len(points) != 0:
  alive_points = []
  for p in points:
    # Spawn one for each direction
    np = p.copy()
    np.y -= 1
    wp = p.copy()
    wp.x -= 1
    ep = p.copy()
    ep.x += 1
    sp = p.copy()
    sp.y += 1

    new_points = [np, wp, sp, ep]

    for new_p in new_points:
      val = my_map.get(new_p)

      if (val == "."):
        my_map.add_o2(new_p)
        alive_points.append(new_p)

  points = alive_points
  mins += 1

print("mins", mins)
