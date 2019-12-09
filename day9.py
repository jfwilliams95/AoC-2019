# Day 9 - Advent of Code 2019
# Author: Jeff Williams

import types

class Code:

  setting = 0
  code = []
  i = 0
  setting_used = False

  def __init__(self, code, setting):
    # copy the code
    self.code = []
    for c in code:
      self.code.append(c)

    self.setting = setting
    self.i = 0
    self.setting_used = False

  def execute(self, val):
    obj = execute_code(self.code, self.setting, val, self.i, self.setting_used)
    self.setting_used = True

    self.code = obj.code
    self.i = obj.index
    return obj

# Reads in the file
def get_code(filename):
  code = []
  with open(filename, "r") as file:
    line = file.readline().strip()
    codestrs = line.split(',')
   
    for codestr in codestrs:
      code.append(int(codestr.strip()))
  return code

def instr_to_array(instr_int):
  instr_str = str(instr_int)

  # Add in leading zeroes
  while len(instr_str) < 5:
    instr_str = "0" + instr_str

  # Break it out
  instr = [int(instr_str[0]), int(instr_str[1]), int(instr_str[2]), int(instr_str[3:5])]
  return instr

def get_value(code, index, mode, relative_value):
  if mode == 0:
    i = code[index]

    if (i > len(code)):
      return 0
    else:
      return code[code[index]]
  elif mode == 1:
    return 0 if index > len(code) else code[index]
  elif mode == 2:
    i = relative_value + code[index]
    if i > len(code):
      return 0
    else:
      return code[relative_value + code[index]]

def assign(code, index, value):
  while index > len(code)-1:
    code.append(0)
  code[index] = value

# Executes the code
def execute_code(code, setting, input_val, index, setting_used):

  # The return object
  return_obj = types.SimpleNamespace()
  return_obj.code = code
  return_obj.index = index
  return_obj.value = 0
  return_obj.finished = False

  relative_value = 0

  i = index
  code_len = len(code)

  output = None
  while True:

    # Read the instruction as an int
    instr_int = code[i]
    # Get the instruction as an array
    instr_arr = instr_to_array(instr_int)

    print("Excuting")

    operation = instr_arr[-1]
    a_mode = instr_arr[2]
    b_mode = instr_arr[1]
    c_mode = instr_arr[0]

    if (operation not in range(1,11)):
      break

    if (operation == 1):
      a = get_value(code, i + 1, a_mode, relative_value)
      b = get_value(code, i + 2, b_mode, relative_value)

      pos = relative_value + code[i+3] if c_mode == 2 else code[i+3]
      assign(code, pos, (a+b))
      i = i + 4
    elif(operation == 2):
      a = get_value(code, i + 1, a_mode, relative_value)
      b = get_value(code, i + 2, b_mode, relative_value)
      pos = relative_value + code[i+3] if c_mode == 2 else code[i+3]
      assign(code,pos, a*b)
      i = i + 4
    elif (operation == 3):
      a = get_value(code, i + 1, a_mode, relative_value)
      
      val = int(input('Please enter a number: '))
      assign(code, a, val)
      i = i + 2
    elif (operation == 4):
      a = get_value(code, i + 1, a_mode, relative_value)
      print(a)
      i = i + 2
    elif (operation == 5):
      a = get_value(code, i + 1, a_mode, relative_value)
      b = get_value(code, i + 2, b_mode, relative_value)

      if a:
        i = b
      else:
        i = i + 3
    elif (operation == 6):
      a = get_value(code, i + 1, a_mode, relative_value)
      b = get_value(code, i + 2, b_mode, relative_value)

      if not a:
        i = b
      else:
        i = i + 3
    elif (operation == 7):
      a = get_value(code, i + 1, a_mode, relative_value)
      b = get_value(code, i + 2, b_mode, relative_value)
      pos = relative_value + code[i+3] if c_mode == 2 else code[i+3]

      assign(code, pos, (1 if (a < b) else 0))
      i = i + 4
    elif (operation == 8):
      a = get_value(code, i + 1, a_mode, relative_value)
      b = get_value(code, i + 2, b_mode, relative_value)
      pos = relative_value + code[i+3] if c_mode == 2 else code[i+3]

      assign(code, pos, (1 if (a == b) else 0))
      i = i + 4
    elif (operation == 9):
      a = get_value(code, i + 1, a_mode, relative_value)
      relative_value += a
      i = i + 2

  print("Finished at " + str(operation))
  return_obj.finished = True
  return return_obj

def execute_set(code, num_set):
  
  # Generate the code array
  code_objs = []
  for num in num_set:
    code_objs.append(Code(code, num))

  finished = False
  val = 0
  i = 0
  while not finished:
    obj = code_objs[i].execute(val)

    if (obj.finished):
      finished = True
    else:
      val = obj.value
      i += 1
      i = i if i < len(code_objs) else 0

  return val

code = get_code('./input/day9.txt')
cobj = Code(code, 1)
cobj.execute(1)