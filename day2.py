# Reads in the file
def get_code(filename):
  code = []
  with open(filename, "r") as file:
    line = file.readline().strip()
    codestrs = line.split(',')
   
    for codestr in codestrs:
      code.append(int(codestr))
  return code

def execute_code(code):

  i = 0
  code_len = len(code)

  while True:
    if (code[i] != 1 and code[i] != 2):
      break

    if (code[i] == 1):
      i_a = code[i+1]
      i_b = code[i+2]
      pos = code[i+3]
      code[pos] = (code[i_a]+code[i_b])
      i = i + 4
    elif(code[i] == 2):
      i_a = code[i+1]
      i_b = code[i+2]
      pos = code[i+3]
      code[pos] = code[i_a] * code[i_b]
      i = i + 4

  return code

def copy_code(code):
  new = []
  for num in code:
    new.append(num)
  return new

# Read in the file
base_code = get_code('./input/day2.txt')
target = 19690720

# Try for each number
for a in range(0, 99):
  for b in range(0, 99):
    # copy the code
    code = copy_code(base_code)
    code[1] = a
    code[2] = b
    code = execute_code(code)
    if (code[0] == target):
      print(100 * a + b)