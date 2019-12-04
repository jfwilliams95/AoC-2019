# Day 4 - Advent of Code 2019
# Author: Jeff Williams

# Get each digit
def get_digits(input):
  # convert to a string
  as_str = str(input)

  digits = []
  for char in as_str:
    digits.append(int(char))

  return digits

def digits_to_num(digits):
  num_str = ""
  for digit in digits:
    num_str += str(digit)

  return int(num_str)

# Advance the array
def advance_array(digits):

  # Get the number as an int
  orig_num = digits_to_num(digits)

  # Get the length of the array
  digit_len = len(digits)

  # First, ensure all digits are equal or ascending
  last_digit = digits[0]

  for i in range(1, digit_len):
    digit = digits[i]

    if (digit < last_digit):
      digits[i] = last_digit
      # Set all of the consecutive digits to this number
      for j in range(i + 1, digit_len):
        digits[j] = last_digit

    last_digit = digit

  # If the number hasn't changed, increment the last digit
  new_num = digits_to_num(digits)
  i = len(digits) - 1

  if (new_num == orig_num):
    digits[i] += 1

    # If the increment pushes it over 9, feed it upwards
    while digits[i] > 9 and i > 0:
      i -= 1
      digits[i] += 1

      # Set each consecutive digit to be the same
      for j in range(i+1, digit_len):
        digits[j] = digits[i]

  return digits
    
def has_double(digits):
  last_digit = digits[0]
  for i in range(1, len(digits)):
    if (digits[i] == last_digit):
      return True

    last_digit = digits[i]

def has_single_double(digits):
  # Make groups
  groups = []

  cur_group = []
  for digit in digits:
    # If there isn't a group, start one
    if (len(cur_group) == 0):
      cur_group.append(digit)
    # Otherwise, check to see if it's part of the same group
    else:
      # If the digit is the same as the current group, add it in
      if (cur_group[0] == digit):
        cur_group.append(digit)
      else:
        # Otherwise, add in the current group, and start a new one
        groups.append(cur_group)
        cur_group = []
        cur_group.append(digit)

  # Add in the last digit
  groups.append(cur_group)

  # If any of the groupings have two items, return true
  for group in groups:
    if len(group) == 2:
      return True

  return False


# Actual calculations begin here

rng = [353096, 843212]

candidate_count = 0

# Part One Solution
digits = get_digits(rng[0])
digits = advance_array(digits)
num = digits_to_num(digits)

while num <= rng[1]:
  # If there's a double, increase the counter
  if (has_double(digits)):
    candidate_count += 1

  # Advance the digit array
  digits = advance_array(digits)
  num = digits_to_num(digits)

print (candidate_count)

# Part Two Solutions
digits = get_digits(rng[0])
digits = advance_array(digits)
num = digits_to_num(digits)
candidate_count = 0

while num <= rng[1]:
  # If there's a single double, increase the counter
  if (has_single_double(digits)):
    candidate_count += 1

  # Advance the digit array
  digits = advance_array(digits)
  num = digits_to_num(digits)

print (candidate_count)



