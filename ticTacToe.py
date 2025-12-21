import math
import random

board = []

def boardInit():
  rows = 3
  cols = 3
  global board
  board = [['0' for _ in range(cols)] for _ in range(rows)]
boardInit()

def printBoard():
  for entry in board:
    row = '|'
    for entries in entry:
      row = row + f' {entries}' + ' |'
    print(row)
printBoard()