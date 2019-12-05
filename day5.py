# Day 5 - Advent of Code 2019
# Author: Jeff Williams

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

# Executes the code
def execute_code(code):

  i = 0
  code_len = len(code)

  while True:

    # Read the instruction as an int
    instr_int = code[i]
    # Get the instruction as an array
    instr_arr = instr_to_array(instr_int)

    operation = instr_arr[-1]
    a_mode = instr_arr[2]
    b_mode = instr_arr[1]
    c_mode = instr_arr[0]

    if (operation not in range(1,9)):
      break

    if (operation == 1):
      a = code[i+1] if a_mode else code[code[i+1]]
      b = code[i+2] if b_mode else code[code[i+2]]

      pos = code[i+3]
      code[pos] = (a+b)
      i = i + 4
    elif(operation == 2):
      a = code[i+1] if a_mode else code[code[i+1]]
      b = code[i+2] if b_mode else code[code[i+2]]
      pos = code[i+3]
      code[pos] = a * b
      i = i + 4
    elif (operation == 3):
      a = code[i+1]
      val = int(input('Please enter a number: '))
      code[a] = val
      i = i + 2
    elif (operation == 4):
      a = code[i+1]
      print(code[a])
      i = i + 2
    elif (operation == 5):
      a = code[i+1] if a_mode else code[code[i+1]]
      b = code[i+2] if b_mode else code[code[i+2]]

      if a:
        i = b
      else:
        i = i + 3
    elif (operation == 6):
      a = code[i+1] if a_mode else code[code[i+1]]
      b = code[i+2] if b_mode else code[code[i+2]]

      if not a:
        i = b
      else:
        i = i + 3
    elif (operation == 7):
      a = code[i+1] if a_mode else code[code[i+1]]
      b = code[i+2] if b_mode else code[code[i+2]]
      pos = code[i+3]

      code[pos] = 1 if (a < b) else 0
      i = i + 4
    elif (operation == 8):
      a = code[i+1] if a_mode else code[code[i+1]]
      b = code[i+2] if b_mode else code[code[i+2]]
      pos = code[i+3]

      code[pos] = 1 if (a == b) else 0
      i = i + 4



  return code

code = get_code('./input/day5.txt')
code = execute_code(code)