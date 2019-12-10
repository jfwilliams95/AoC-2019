# Day 9 - Advent of Code 2019
# Author: Jeff Williams

import types

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

  def execute(self):

    while True:
      instr = Instruction(self.code[self.i])

      if (instr.operator == 99):
        break

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

        val = int(input("Enter a value: "))
        self.set(a, val)
        self.i += 2
      elif instr.operator == 4:
        a = self.get(self.i + 1, instr.modes[2])

        print(a)
        self.i += 2
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

code = get_code('./input/day9.txt')
code.execute()