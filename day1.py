# Day One - Advent of Code 2019
# Author: Jeff Williams

import math

def get_required_fuel (mass):
  return math.floor(mass / 3) - 2

def read_input (filename):
  data = []

  with open(filename, "r") as file:
    line = file.readline().strip()

    while line:
      data.append(int(line))
      line = file.readline()

  return data

def calculate_fuel_simple (masses):
  total = 0

  for mass in masses:
    total += get_required_fuel(mass)

  return total

def calculate_total_fuel(masses):
  total = 0

  for mass in masses:
    
    # For each mass, determine the total amount of fuel needed
    fuel = get_required_fuel(mass)
    while fuel > 0:
      total += fuel
      fuel = get_required_fuel(fuel)

  return total

masses = read_input('./input/day1.txt')
fuel = calculate_total_fuel(masses)

print (fuel)
